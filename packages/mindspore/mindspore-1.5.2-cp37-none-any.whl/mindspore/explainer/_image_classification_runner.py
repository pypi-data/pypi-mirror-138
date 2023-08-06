# Copyright 2020-2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Image Classification Runner."""
import os
import re
import json
from time import time

import numpy as np
from scipy.stats import beta
from PIL import Image

import mindspore as ms
from mindspore import context
from mindspore import log
import mindspore.dataset as ds
from mindspore.dataset import Dataset
from mindspore.nn import Cell, SequentialCell
from mindspore.ops.operations import ExpandDims
from mindspore.train._utils import check_value_type
from mindspore.train.summary._summary_adapter import _convert_image_format
from mindspore.train.summary.summary_record import SummaryRecord
from mindspore.train.summary_pb2 import Explain
from mindspore.nn.probability.toolbox.uncertainty_evaluation import UncertaintyEvaluation
from mindspore.explainer.benchmark import Localization
from mindspore.explainer.benchmark._attribution.metric import AttributionMetric
from mindspore.explainer.benchmark._attribution.metric import LabelSensitiveMetric
from mindspore.explainer.benchmark._attribution.metric import LabelAgnosticMetric
from mindspore.explainer.explanation import RISE
from mindspore.explainer.explanation._attribution.attribution import Attribution
from mindspore.explainer.explanation._counterfactual import hierarchical_occlusion as hoc
from mindspore.explainer._utils import deprecated_error


_EXPAND_DIMS = ExpandDims()


def _normalize(img_np):
    """Normalize the numpy image to the range of [0, 1]. """
    max_ = img_np.max()
    min_ = img_np.min()
    normed = (img_np - min_) / (max_ - min_).clip(min=1e-10)
    return normed


def _np_to_image(img_np, mode):
    """Convert numpy array to PIL image."""
    return Image.fromarray(np.uint8(img_np * 255), mode=mode)


class _Verifier:
    """Verification of dataset and settings of ImageClassificationRunner."""
    ALL = 0xFFFFFFFF
    REGISTRATION = 1
    DATA_N_NETWORK = 1 << 1
    SALIENCY = 1 << 2
    HOC = 1 << 3
    ENVIRONMENT = 1 << 4

    def _verify(self, flags):
        """
        Verify datasets and settings.

        Args:
            flags (int): Verification flags, use bitwise or '|' to combine multiple flags.
                Possible bitwise flags are shown as follow.

                - ALL: Verify everything.
                - REGISTRATION: Verify explainer module registration.
                - DATA_N_NETWORK: Verify dataset and network.
                - SALIENCY: Verify saliency related settings.
                - HOC: Verify HOC related settings.
                - ENVIRONMENT: Verify the runtime environment.

        Raises:
                ValueError: Be raised for any data or settings' value problem.
                TypeError: Be raised for any data or settings' type problem.
                RuntimeError: Be raised for any runtime problem.
        """
        if flags & self.ENVIRONMENT:
            device_target = context.get_context('device_target')
            if device_target not in ("Ascend", "GPU"):
                raise RuntimeError(f"Unsupported device_target: '{device_target}', "
                                   f"only 'Ascend' or 'GPU' is supported. "
                                   f"Please call context.set_context(device_target='Ascend') or "
                                   f"context.set_context(device_target='GPU').")
        if flags & (self.ENVIRONMENT | self.SALIENCY):
            if self._is_saliency_registered:
                mode = context.get_context('mode')
                if mode != context.PYNATIVE_MODE:
                    raise RuntimeError("Context mode: GRAPH_MODE is not supported, "
                                       "please call context.set_context(mode=context.PYNATIVE_MODE).")

        if flags & self.REGISTRATION:
            if self._is_uncertainty_registered and not self._is_saliency_registered:
                raise ValueError("Function register_uncertainty() is called but register_saliency() is not.")
            if not self._is_saliency_registered and not self._is_hoc_registered:
                raise ValueError(
                    "No explanation module was registered, user should at least call register_saliency() "
                    "or register_hierarchical_occlusion() once with proper arguments.")

        if flags & (self.DATA_N_NETWORK | self.SALIENCY | self.HOC):
            self._verify_data()

        if flags & self.DATA_N_NETWORK:
            self._verify_network()

        if flags & self.SALIENCY:
            self._verify_saliency()

    def _verify_labels(self):
        """Verify labels."""
        label_set = set()
        if not self._labels:
            raise ValueError(f"The label list provided is empty.")
        for i, label in enumerate(self._labels):
            if label.strip() == "":
                raise ValueError(f"Label [{i}] is all whitespaces or empty. Please make sure there is "
                                 f"no empty label.")
            if label in label_set:
                raise ValueError(f"Duplicated label:{label}! Please make sure all labels are unique.")
            label_set.add(label)

    def _verify_ds_inputs_shape(self, sample, inputs, labels):
        """Verify a dataset sample's input shape."""

        if len(inputs.shape) > 4 or len(inputs.shape) < 3 or inputs.shape[-3] not in [1, 3, 4]:
            raise ValueError(
                "Image shape {} is unrecognizable: the dimension of image can only be CHW or NCHW.".format(
                    inputs.shape))
        if len(inputs.shape) == 3:
            log.warning(
                "Image shape {} is 3-dimensional. All the data will be automatically unsqueezed at the 0-th"
                " dimension as batch data.".format(inputs.shape))
        if len(sample) > 1:
            if len(labels.shape) > 2 and (np.array(labels.shape[1:]) > 1).sum() > 1:
                raise ValueError(
                    "Labels shape {} is unrecognizable: outputs should not have more than two dimensions"
                    " with length greater than 1.".format(labels.shape))

        if self._is_hoc_registered:
            if inputs.shape[-3] != 3:
                raise ValueError(
                    "Hierarchical occlusion is registered, images must be in 3 channels format, but "
                    "{} channel(s) is(are) encountered.".format(inputs.shape[-3]))
            short_side = min(inputs.shape[-2:])
            if short_side < hoc.AUTO_IMAGE_SHORT_SIDE_MIN:
                raise ValueError(
                    "Hierarchical occlusion is registered, images' short side must be equals to or greater then "
                    "{}, but {} is encountered.".format(hoc.AUTO_IMAGE_SHORT_SIDE_MIN, short_side))

    def _verify_ds_sample(self, sample):
        """Verify a dataset sample."""
        if len(sample) not in [1, 2, 3]:
            raise ValueError("The dataset should provide [images] or [images, labels], [images, labels, bboxes]"
                             " as columns.")

        if len(sample) == 3:
            inputs, labels, bboxes = sample
            if bboxes.shape[-1] != 4:
                raise ValueError("The third element of dataset should be bounding boxes with shape of "
                                 "[batch_size, num_ground_truth, 4].")
        else:
            if self._benchmarkers is not None:
                if any([isinstance(bench, Localization) for bench in self._benchmarkers]):
                    raise ValueError("The dataset must provide bboxes if Localization is to be computed.")

            if len(sample) == 2:
                inputs, labels = sample
            if len(sample) == 1:
                inputs = sample[0]

        self._verify_ds_inputs_shape(sample, inputs, labels)

    def _verify_data(self):
        """Verify dataset and labels."""
        self._verify_labels()

        try:
            sample = next(self._dataset.create_tuple_iterator())
        except StopIteration:
            raise ValueError("The dataset provided is empty.")

        self._verify_ds_sample(sample)

    def _verify_network(self):
        """Verify the network."""
        next_element = next(self._dataset.create_tuple_iterator())
        inputs, _, _ = self._unpack_next_element(next_element)
        prop_test = self._full_network(inputs)
        check_value_type("output of network in explainer", prop_test, ms.Tensor)
        if prop_test.shape[1] != len(self._labels):
            raise ValueError("The dimension of network output does not match the no. of classes. Please "
                             "check labels or the network in the explainer again.")

    def _verify_saliency(self):
        """Verify the saliency settings."""
        if self._explainers:
            explainer_classes = []
            for explainer in self._explainers:
                if explainer.__class__ in explainer_classes:
                    raise ValueError(f"Repeated {explainer.__class__.__name__} explainer! "
                                     "Please make sure all explainers' class is distinct.")
                if explainer.network is not self._network:
                    raise ValueError(f"The network of {explainer.__class__.__name__} explainer is different "
                                     "instance from network of runner. Please make sure they are the same "
                                     "instance.")
                explainer_classes.append(explainer.__class__)
        if self._benchmarkers:
            benchmarker_classes = []
            for benchmarker in self._benchmarkers:
                if benchmarker.__class__ in benchmarker_classes:
                    raise ValueError(f"Repeated {benchmarker.__class__.__name__} benchmarker! "
                                     "Please make sure all benchmarkers' class is distinct.")
                if isinstance(benchmarker, LabelSensitiveMetric) and benchmarker.num_labels != len(self._labels):
                    raise ValueError(f"The num_labels of {benchmarker.__class__.__name__} benchmarker is different "
                                     "from no. of labels of runner. Please make them are the same.")
                benchmarker_classes.append(benchmarker.__class__)


@deprecated_error
class ImageClassificationRunner(_Verifier):
    """
    A high-level API for users to generate and store results of the explanation methods and the evaluation methods.

    Update in 2020.11: Adjust the storage structure and format of the data. Summary files generated by previous version
    will be deprecated and will not be supported in MindInsight of current version.

    Args:
        summary_dir (str): The directory path to save the summary files which store the generated results.
        data (tuple[Dataset, list[str]]): Tuple of dataset and the corresponding class label list. The dataset
            should provides [images], [images, labels] or [images, labels, bboxes] as columns. The label list must
            share the exact same length and order of the network outputs.
        network (Cell): The network(with logit outputs) to be explained.
        activation_fn (Cell): The activation layer that transforms logits to prediction probabilities. For
            single label classification tasks, `nn.Softmax` is usually applied. As for multi-label classification
            tasks, `nn.Sigmoid` is usually be applied. Users can also pass their own customized `activation_fn` as long
            as when combining this function with network, the final output is the probability of the input.

    Raises:
        TypeError: Be raised for any argument type problem.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> from mindspore.explainer import ImageClassificationRunner
        >>> from mindspore.explainer.explanation import GuidedBackprop, Gradient
        >>> from mindspore.explainer.benchmark import Faithfulness
        >>> from mindspore.nn import Softmax
        >>> from mindspore.train.serialization import load_checkpoint, load_param_into_net
        >>> from mindspore import context
        >>>
        >>> context.set_context(mode=context.PYNATIVE_MODE)
        >>> # The detail of AlexNet is shown in model_zoo.official.cv.alexnet.src.alexnet.py
        >>> net = AlexNet(10)
        >>> # Load the checkpoint
        >>> param_dict = load_checkpoint("/path/to/checkpoint")
        >>> load_param_into_net(net, param_dict)
        []
        >>>
        >>> # Prepare the dataset for explaining and evaluation.
        >>> # The detail of create_dataset_cifar10 method is shown in model_zoo.official.cv.alexnet.src.dataset.py
        >>>
        >>> dataset = create_dataset_cifar10("/path/to/cifar/dataset", 1)
        >>> labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        >>>
        >>> activation_fn = Softmax()
        >>> gbp = GuidedBackprop(net)
        >>> gradient = Gradient(net)
        >>> explainers = [gbp, gradient]
        >>> faithfulness = Faithfulness(len(labels), activation_fn, "NaiveFaithfulness")
        >>> benchmarkers = [faithfulness]
        >>>
        >>> runner = ImageClassificationRunner("./summary_dir", (dataset, labels), net, activation_fn)
        >>> runner.register_saliency(explainers=explainers, benchmarkers=benchmarkers)
        >>> runner.run()
    """

    # datafile directory names
    _DATAFILE_DIRNAME_PREFIX = "_explain_"
    _ORIGINAL_IMAGE_DIRNAME = "origin_images"
    _HEATMAP_DIRNAME = "heatmap"
    # specfial filenames
    _MANIFEST_FILENAME = "manifest.json"
    # max. no. of sample per directory
    _SAMPLE_PER_DIR = 1000
    # seed for fixing the iterating order of the dataset
    _DATASET_SEED = 58
    # printing spacer
    _SPACER = "{:120}\r"
    # datafile directory's permission
    _DIR_MODE = 0o700
    # datafile's permission
    _FILE_MODE = 0o400

    def __init__(self,
                 summary_dir,
                 data,
                 network,
                 activation_fn):

        check_value_type("data", data, tuple)
        if len(data) != 2:
            raise ValueError("Argument data is not a tuple with 2 elements")
        check_value_type("data[0]", data[0], Dataset)
        check_value_type("data[1]", data[1], list)
        if not all(isinstance(ele, str) for ele in data[1]):
            raise ValueError("Argument data[1] is not list of str.")

        check_value_type("summary_dir", summary_dir, str)
        check_value_type("network", network, Cell)
        check_value_type("activation_fn", activation_fn, Cell)

        self._summary_dir = summary_dir
        self._dataset = data[0]
        self._labels = data[1]
        self._network = network
        self._explainers = None
        self._benchmarkers = None
        self._uncertainty = None
        self._hoc_searcher = None
        self._summary_timestamp = None
        self._sample_index = -1
        self._manifest = None

        self._full_network = SequentialCell([self._network, activation_fn])
        self._full_network.set_train(False)

        self._verify(_Verifier.DATA_N_NETWORK | _Verifier.ENVIRONMENT)

    def register_saliency(self,
                          explainers,
                          benchmarkers=None):
        """
        Register saliency explanation instances.

        .. warning::
            This function can not be invoked more than once on each runner.

        Args:
            explainers (list[Attribution]): The explainers to be evaluated,
                see `mindspore.explainer.explanation`. All explainers' class must be distinct and their network
                must be the exact same instance of the runner's network.
            benchmarkers (list[AttributionMetric], optional): The benchmarkers for scoring the explainers,
                see `mindspore.explainer.benchmark`. All benchmarkers' class must be distinct.

        Raises:
            ValueError: Be raised for any data or settings' value problem.
            TypeError: Be raised for any data or settings' type problem.
            RuntimeError: Be raised if this function was invoked before.
        """
        check_value_type("explainers", explainers, list)
        if not all(isinstance(ele, Attribution) for ele in explainers):
            raise TypeError("Argument explainers is not list of mindspore.explainer.explanation .")

        if not explainers:
            raise ValueError("Argument explainers is empty.")

        if benchmarkers is not None:
            check_value_type("benchmarkers", benchmarkers, list)
            if not all(isinstance(ele, AttributionMetric) for ele in benchmarkers):
                raise TypeError("Argument benchmarkers is not list of mindspore.explainer.benchmark .")

        if self._explainers is not None:
            raise RuntimeError("Function register_saliency() was invoked already.")

        self._explainers = explainers
        self._benchmarkers = benchmarkers

        try:
            self._verify(_Verifier.SALIENCY | _Verifier.ENVIRONMENT)
        except (ValueError, TypeError):
            self._explainers = None
            self._benchmarkers = None
            raise

    def register_hierarchical_occlusion(self):
        """
        Register hierarchical occlusion instances.

        .. warning::
            This function can not be invoked more than once on each runner.

        Note:
            Input images are required to be in 3 channels formats and the length of side short must be equals to or
            greater than 56 pixels.

        Raises:
            ValueError: Be raised for any data or settings' value problem.
            RuntimeError: Be raised if the function was called already.
        """
        if self._hoc_searcher is not None:
            raise RuntimeError("Function register_hierarchical_occlusion() was invoked already.")

        self._hoc_searcher = hoc.Searcher(self._full_network)

        try:
            self._verify(_Verifier.HOC | _Verifier.ENVIRONMENT)
        except ValueError:
            self._hoc_searcher = None
            raise

    def register_uncertainty(self):
        """
        Register uncertainty instance to compute the epistemic uncertainty base on the Bayes' theorem.

        .. warning::
            This function can not be invoked more than once on each runner.

        Note:
            Please refer to the documentation of mindspore.nn.probability.toolbox.uncertainty_evaluation for the
            details. The actual output is standard deviation of the classification predictions and the corresponding
            95% confidence intervals. Users have to invoke register_saliency() as well for the uncertainty results are
            going to be shown on the saliency map page in MindInsight.

        Raises:
            RuntimeError: Be raised if the function was called already.
        """
        if self._uncertainty is not None:
            raise RuntimeError("Function register_uncertainty() was invoked already.")

        self._uncertainty = UncertaintyEvaluation(model=self._full_network,
                                                  train_dataset=None,
                                                  task_type='classification',
                                                  num_classes=len(self._labels))

    def run(self):
        """
        Run the explain job and save the result as a summary in summary_dir.

        Note:
            User should call register_saliency() once before running this function.

        Raises:
            ValueError: Be raised for any data or settings' value problem.
            TypeError: Be raised for any data or settings' type problem.
            RuntimeError: Be raised for any runtime problem.
        """
        self._verify(_Verifier.ALL)
        self._manifest = {"saliency_map": False,
                          "benchmark": False,
                          "uncertainty": False,
                          "hierarchical_occlusion": False}
        with SummaryRecord(self._summary_dir, raise_exception=True) as summary:
            print("Start running and writing......")
            begin = time()

            self._summary_timestamp = self._extract_timestamp(summary.file_info['file_name'])
            if self._summary_timestamp is None:
                raise RuntimeError("Cannot extract timestamp from summary filename!"
                                   " It should contains a timestamp after 'summary.' .")

            self._save_metadata(summary)

            imageid_labels = self._run_inference(summary)
            sample_count = self._sample_index
            if self._is_saliency_registered:
                self._run_saliency(summary, imageid_labels)
                if not self._manifest["saliency_map"]:
                    raise RuntimeError(
                        f"No saliency map was generated in {sample_count} samples. "
                        f"Please make sure the dataset, labels, activation function and network are properly trained "
                        f"and configured.")

            if self._is_hoc_registered and not self._manifest["hierarchical_occlusion"]:
                raise RuntimeError(
                    f"No Hierarchical Occlusion result was found in {sample_count} samples. "
                    f"Please make sure the dataset, labels, activation function and network are properly trained "
                    f"and configured.")

            self._save_manifest()

            print("Finish running and writing. Total time elapsed: {:.3f} s".format(time() - begin))

    @property
    def _is_hoc_registered(self):
        """Check if HOC module is registered."""
        return self._hoc_searcher is not None

    @property
    def _is_saliency_registered(self):
        """Check if saliency module is registered."""
        return bool(self._explainers)

    @property
    def _is_uncertainty_registered(self):
        """Check if uncertainty module is registered."""
        return self._uncertainty is not None

    def _save_metadata(self, summary):
        """Save metadata of the explain job to summary."""
        print("Start writing metadata......")

        explain = Explain()
        explain.metadata.label.extend(self._labels)

        if self._is_saliency_registered:
            exp_names = [exp.__class__.__name__ for exp in self._explainers]
            explain.metadata.explain_method.extend(exp_names)
            if self._benchmarkers is not None:
                bench_names = [bench.__class__.__name__ for bench in self._benchmarkers]
                explain.metadata.benchmark_method.extend(bench_names)

        summary.add_value("explainer", "metadata", explain)
        summary.record(1)

        print("Finish writing metadata.")

    def _run_inference(self, summary, threshold=0.5):
        """
        Run inference for the dataset and write the inference related data into summary.

        Args:
            summary (SummaryRecord): The summary object to store the data.
            threshold (float): The threshold for prediction.

        Returns:
            dict, The map of sample d to the union of its ground truth and predicted labels.
        """
        sample_id_labels = {}
        self._sample_index = 0
        ds.config.set_seed(self._DATASET_SEED)
        for j, batch in enumerate(self._dataset):
            now = time()
            self._infer_batch(summary, batch, sample_id_labels, threshold)
            self._spaced_print("Finish running and writing {}-th batch inference data."
                               " Time elapsed: {:.3f} s".format(j, time() - now))
        return sample_id_labels

    def _infer_batch(self, summary, batch, sample_id_labels, threshold):
        """
        Infer a batch.

        Args:
            summary (SummaryRecord): The summary object to store the data.
            batch (tuple): The next dataset sample.
            sample_id_labels (dict): The sample id to labels dictionary.
            threshold (float): The threshold for prediction.
        """
        inputs, labels, _ = self._unpack_next_element(batch)
        prob = self._full_network(inputs).asnumpy()

        if self._uncertainty is not None:
            prob_var = self._uncertainty.eval_epistemic_uncertainty(inputs)
        else:
            prob_var = None

        for idx, inp in enumerate(inputs):
            gt_labels = labels[idx]
            gt_probs = [float(prob[idx][i]) for i in gt_labels]

            if prob_var is not None:
                gt_prob_vars = [float(prob_var[idx][i]) for i in gt_labels]
                gt_itl_lows, gt_itl_his, gt_prob_sds = \
                    self._calc_beta_intervals(gt_probs, gt_prob_vars)

            data_np = _convert_image_format(np.expand_dims(inp.asnumpy(), 0), 'NCHW')
            original_image = _np_to_image(_normalize(data_np), mode='RGB')
            original_image_path = self._save_original_image(self._sample_index, original_image)

            predicted_labels = [int(i) for i in (prob[idx] > threshold).nonzero()[0]]
            predicted_probs = [float(prob[idx][i]) for i in predicted_labels]

            if prob_var is not None:
                predicted_prob_vars = [float(prob_var[idx][i]) for i in predicted_labels]
                predicted_itl_lows, predicted_itl_his, predicted_prob_sds = \
                    self._calc_beta_intervals(predicted_probs, predicted_prob_vars)

            union_labs = list(set(gt_labels + predicted_labels))
            sample_id_labels[str(self._sample_index)] = union_labs

            explain = Explain()
            explain.sample_id = self._sample_index
            explain.image_path = original_image_path
            summary.add_value("explainer", "sample", explain)

            explain = Explain()
            explain.sample_id = self._sample_index
            explain.ground_truth_label.extend(gt_labels)
            explain.inference.ground_truth_prob.extend(gt_probs)
            explain.inference.predicted_label.extend(predicted_labels)
            explain.inference.predicted_prob.extend(predicted_probs)

            if prob_var is not None:
                explain.inference.ground_truth_prob_sd.extend(gt_prob_sds)
                explain.inference.ground_truth_prob_itl95_low.extend(gt_itl_lows)
                explain.inference.ground_truth_prob_itl95_hi.extend(gt_itl_his)
                explain.inference.predicted_prob_sd.extend(predicted_prob_sds)
                explain.inference.predicted_prob_itl95_low.extend(predicted_itl_lows)
                explain.inference.predicted_prob_itl95_hi.extend(predicted_itl_his)

                self._manifest["uncertainty"] = True

            summary.add_value("explainer", "inference", explain)
            summary.record(1)

            if self._is_hoc_registered:
                self._run_hoc(summary, self._sample_index, inputs[idx], prob[idx])

            self._sample_index += 1

    def _run_explainer(self, summary, sample_id_labels, explainer):
        """
        Run the explainer.

        Args:
            summary (SummaryRecord): The summary object to store the data.
            sample_id_labels (dict): A dict that maps the sample id and its union labels.
            explainer (_Attribution): An Attribution object to generate saliency maps.
        """
        for idx, next_element in enumerate(self._dataset):
            now = time()
            self._spaced_print("Start running {}-th explanation data for {}......".format(
                idx, explainer.__class__.__name__))
            saliency_dict_lst = self._run_exp_step(next_element, explainer, sample_id_labels, summary)
            self._spaced_print(
                "Finish writing {}-th batch explanation data for {}. Time elapsed: {:.3f} s".format(
                    idx, explainer.__class__.__name__, time() - now))

            if not self._benchmarkers:
                continue

            for bench in self._benchmarkers:
                now = time()
                self._spaced_print(
                    "Start running {}-th batch {} data for {}......".format(
                        idx, bench.__class__.__name__, explainer.__class__.__name__))
                self._run_exp_benchmark_step(next_element, explainer, bench, saliency_dict_lst)
                self._spaced_print(
                    "Finish running {}-th batch {} data for {}. Time elapsed: {:.3f} s".format(
                        idx, bench.__class__.__name__, explainer.__class__.__name__, time() - now))

    def _run_saliency(self, summary, sample_id_labels):
        """Run the saliency explanations."""

        for explainer in self._explainers:
            explain = Explain()
            if self._benchmarkers:
                for bench in self._benchmarkers:
                    bench.reset()
            print(f"Start running and writing explanation for {explainer.__class__.__name__}......")
            self._sample_index = 0
            start = time()
            ds.config.set_seed(self._DATASET_SEED)
            self._run_explainer(summary, sample_id_labels, explainer)

            if not self._benchmarkers:
                continue

            for bench in self._benchmarkers:
                benchmark = explain.benchmark.add()
                benchmark.explain_method = explainer.__class__.__name__
                benchmark.benchmark_method = bench.__class__.__name__

                benchmark.total_score = bench.performance
                if isinstance(bench, LabelSensitiveMetric):
                    benchmark.label_score.extend(bench.class_performances)

            self._spaced_print("Finish running and writing explanation and benchmark data for {}. "
                               "Time elapsed: {:.3f} s".format(explainer.__class__.__name__, time() - start))
            summary.add_value('explainer', 'benchmark', explain)
            summary.record(1)

    def _run_hoc(self, summary, sample_id, sample_input, prob):
        """
        Run HOC search for a sample image, and then save the result to summary.

        Args:
            summary (SummaryRecord): The summary object to store the data.
            sample_id (int): The sample ID.
            sample_input (Union[Tensor, np.ndarray]): Sample image tensor in CHW or NCWH(N=1).
            prob (Union[Tensor, np.ndarray]): List of sample's classification prediction output, HOC will run for
                labels with prediction output strictly larger then HOC searcher's threshold(0.5 by default).
        """
        if isinstance(sample_input, ms.Tensor):
            sample_input = sample_input.asnumpy()
        if len(sample_input.shape) == 3:
            sample_input = np.expand_dims(sample_input, axis=0)

        explain = None
        str_mask = hoc.auto_str_mask(sample_input)
        compiled_mask = None

        for label_idx, label_prob in enumerate(prob):
            if label_prob <= self._hoc_searcher.threshold:
                continue
            if compiled_mask is None:
                compiled_mask = hoc.compile_mask(str_mask, sample_input)
            try:
                edit_tree, layer_outputs = self._hoc_searcher.search(sample_input, label_idx, compiled_mask)
            except hoc.NoValidResultError:
                log.warning(f"No Hierarchical Occlusion result was found in sample#{sample_id} "
                            f"label:{self._labels[label_idx]}, skipped.")
                continue

            if explain is None:
                explain = Explain()
                explain.sample_id = sample_id

            self._add_hoc_result_to_explain(label_idx, str_mask, edit_tree, layer_outputs, explain)

        if explain is not None:
            summary.add_value("explainer", "hoc", explain)
            summary.record(1)
            self._manifest['hierarchical_occlusion'] = True

    @staticmethod
    def _add_hoc_result_to_explain(label_idx, str_mask, edit_tree, layer_outputs, explain):
        """
        Add HOC result to Explain record.

        Args:
            label_idx (int): The label index.
            str_mask (str): The mask string.
            edit_tree (EditStep): The result HOC edit tree.
            layer_outputs (list[float]): The network output confident of each layer.
            explain (Explain): The Explain record.
        """
        hoc_rec = explain.hoc.add()
        hoc_rec.label = label_idx
        hoc_rec.mask = str_mask
        layer_count = edit_tree.max_layer + 1
        for layer in range(layer_count):
            steps = edit_tree.get_layer_or_leaf_steps(layer)
            layer_output = layer_outputs[layer]
            hoc_layer = hoc_rec.layer.add()
            hoc_layer.prob = layer_output
            for step in steps:
                hoc_layer.box.extend(list(step.box))

    def _add_exp_step_samples(self, explainer, sample_label_sets, batch_saliency_full, summary):
        """
        Add explanation results of samples to summary record.

        Args:
            explainer (Attribution): The explainer to be run.
            sample_label_sets (list[list[int]]): The label sets of samples.
            batch_saliency_full (Tensor): The saliency output from explainer.
            summary (SummaryRecord): The summary record.
        """
        saliency_dict_lst = []
        has_saliency_rec = False
        for idx, label_set in enumerate(sample_label_sets):
            saliency_dict = {}
            explain = Explain()
            explain.sample_id = self._sample_index
            for k, lab in enumerate(label_set):
                saliency = batch_saliency_full[idx:idx + 1, k:k + 1]
                saliency_dict[lab] = saliency

                saliency_np = _normalize(saliency.asnumpy().squeeze())
                saliency_image = _np_to_image(saliency_np, mode='L')
                heatmap_path = self._save_heatmap(explainer.__class__.__name__, lab,
                                                  self._sample_index, saliency_image)

                explanation = explain.explanation.add()
                explanation.explain_method = explainer.__class__.__name__
                explanation.heatmap_path = heatmap_path
                explanation.label = lab

                has_saliency_rec = True

            summary.add_value("explainer", "explanation", explain)
            summary.record(1)

            self._sample_index += 1
            saliency_dict_lst.append(saliency_dict)

        return saliency_dict_lst, has_saliency_rec

    def _run_exp_step(self, next_element, explainer, sample_id_labels, summary):
        """
        Run the explanation for each step and write explanation results into summary.

        Args:
            next_element (Tuple): Data of one step
            explainer (_Attribution): An Attribution object to generate saliency maps.
            sample_id_labels (dict): A dict that maps the sample id and its union labels.
            summary (SummaryRecord): The summary object to store the data.

        Returns:
            list, List of dict that maps label to its corresponding saliency map.
        """
        inputs, labels, _ = self._unpack_next_element(next_element)
        sample_index = self._sample_index
        sample_label_sets = []
        for _ in range(len(labels)):
            sample_label_sets.append(sample_id_labels[str(sample_index)])
            sample_index += 1

        batch_label_sets = self._make_label_batch(sample_label_sets)

        if isinstance(explainer, RISE):
            batch_saliency_full = explainer(inputs, batch_label_sets)
        else:
            batch_saliency_full = []
            for i in range(len(batch_label_sets[0])):
                batch_saliency = explainer(inputs, batch_label_sets[:, i])
                batch_saliency_full.append(batch_saliency)
            concat = ms.ops.operations.Concat(1)
            batch_saliency_full = concat(tuple(batch_saliency_full))

        saliency_dict_lst, has_saliency_rec = \
            self._add_exp_step_samples(explainer, sample_label_sets, batch_saliency_full, summary)

        if has_saliency_rec:
            self._manifest['saliency_map'] = True

        return saliency_dict_lst

    def _run_exp_benchmark_step(self, next_element, explainer, benchmarker, saliency_dict_lst):
        """Run the explanation and evaluation for each step and write explanation results into summary."""
        inputs, labels, _ = self._unpack_next_element(next_element)
        for idx, inp in enumerate(inputs):
            inp = _EXPAND_DIMS(inp, 0)
            self._manifest['benchmark'] = True
            if isinstance(benchmarker, LabelAgnosticMetric):
                res = benchmarker.evaluate(explainer, inp)
                benchmarker.aggregate(res)
                continue
            saliency_dict = saliency_dict_lst[idx]
            for label, saliency in saliency_dict.items():
                if isinstance(benchmarker, Localization):
                    _, _, bboxes = self._unpack_next_element(next_element, True)
                    if label in labels[idx]:
                        res = benchmarker.evaluate(explainer, inp, targets=label, mask=bboxes[idx][label],
                                                   saliency=saliency)
                        benchmarker.aggregate(res, label)
                elif isinstance(benchmarker, LabelSensitiveMetric):
                    res = benchmarker.evaluate(explainer, inp, targets=label, saliency=saliency)
                    benchmarker.aggregate(res, label)
                else:
                    raise TypeError('Benchmarker must be one of LabelSensitiveMetric or LabelAgnosticMetric, but'
                                    'receive {}'.format(type(benchmarker)))

    @staticmethod
    def _calc_beta_intervals(means, variances, prob=0.95):
        """Calculate confidence interval of beta distributions."""
        if not isinstance(means, np.ndarray):
            means = np.array(means)
        if not isinstance(variances, np.ndarray):
            variances = np.array(variances)
        with np.errstate(divide='ignore'):
            coef_a = ((means ** 2) * (1 - means) / variances) - means
            coef_b = (coef_a * (1 - means)) / means
            itl_lows, itl_his = beta.interval(prob, coef_a, coef_b)
            sds = np.sqrt(variances)
        for i in range(itl_lows.shape[0]):
            if not np.isfinite(sds[i]) or not np.isfinite(itl_lows[i]) or not np.isfinite(itl_his[i]):
                itl_lows[i] = means[i]
                itl_his[i] = means[i]
                sds[i] = 0
        return itl_lows, itl_his, sds

    def _transform_bboxes(self, inputs, labels, bboxes, ifbbox):
        """
        Transform the bounding boxes.
        Args:
            inputs (Tensor): the image data
            labels (Tensor): the labels
            bboxes (Tensor): the boudnding boxes data
            ifbbox (bool): whether to preprocess bboxes. If True, a dictionary that indicates bounding boxes w.r.t
                label id will be returned. If False, the returned bboxes is the the parsed bboxes.

         Returns:
            bboxes (Union[list[dict], None, Tensor]): the bounding boxes
        """
        input_len = len(inputs)
        if bboxes is None or not ifbbox:
            return bboxes
        bboxes = ms.Tensor(bboxes, ms.int32)
        masks_lst = []
        labels = labels.asnumpy().reshape([input_len, -1])
        bboxes = bboxes.asnumpy().reshape([input_len, -1, 4])
        for idx, label in enumerate(labels):
            height, width = inputs[idx].shape[-2], inputs[idx].shape[-1]
            masks = {}
            for j, label_item in enumerate(label):
                target = int(label_item)
                if not -1 < target < len(self._labels):
                    continue
                if target not in masks:
                    mask = np.zeros((1, 1, height, width))
                else:
                    mask = masks[target]
                x_min, y_min, x_len, y_len = bboxes[idx][j].astype(int)
                mask[:, :, x_min:x_min + x_len, y_min:y_min + y_len] = 1
                masks[target] = mask
            masks_lst.append(masks)
        bboxes = masks_lst
        return bboxes

    def _transform_data(self, inputs, labels, bboxes, ifbbox):
        """
        Transform the data from one iteration of dataset to a unifying form for the follow-up operations.

        Args:
            inputs (Tensor): the image data
            labels (Tensor): the labels
            bboxes (Tensor): the boudnding boxes data
            ifbbox (bool): whether to preprocess bboxes. If True, a dictionary that indicates bounding boxes w.r.t
                label id will be returned. If False, the returned bboxes is the the parsed bboxes.

        Returns:
            inputs (Tensor): the image data, unified to a 4D Tensor.
            labels (list[list[int]]): the ground truth labels.
            bboxes (Union[list[dict], None, Tensor]): the bounding boxes
        """
        inputs = ms.Tensor(inputs, ms.float32)
        if len(inputs.shape) == 3:
            inputs = _EXPAND_DIMS(inputs, 0)
            if isinstance(labels, ms.Tensor):
                labels = ms.Tensor(labels, ms.int32)
                labels = _EXPAND_DIMS(labels, 0)
            if isinstance(bboxes, ms.Tensor):
                bboxes = ms.Tensor(bboxes, ms.int32)
                bboxes = _EXPAND_DIMS(bboxes, 0)

        bboxes = self._transform_bboxes(inputs, labels, bboxes, ifbbox)

        labels = ms.Tensor(labels, ms.int32)
        if len(labels.shape) == 1:
            labels_lst = [[int(i)] for i in labels.asnumpy()]
        else:
            labels = labels.asnumpy().reshape([len(inputs), -1])
            labels_lst = []
            for item in labels:
                labels_lst.append(list(set(int(i) for i in item if -1 < int(i) < len(self._labels))))
        labels = labels_lst
        return inputs, labels, bboxes

    def _unpack_next_element(self, next_element, ifbbox=False):
        """
        Unpack a single iteration of dataset.

        Args:
            next_element (Tuple): a single element iterated from dataset object.
            ifbbox (bool): whether to preprocess bboxes in self._transform_data.

        Returns:
            tuple, a unified Tuple contains image_data, labels, and bounding boxes.
        """
        if len(next_element) == 3:
            inputs, labels, bboxes = next_element
        elif len(next_element) == 2:
            inputs, labels = next_element
            bboxes = None
        else:
            inputs = next_element[0]
            labels = [[] for _ in inputs]
            bboxes = None
        inputs, labels, bboxes = self._transform_data(inputs, labels, bboxes, ifbbox)
        return inputs, labels, bboxes

    @staticmethod
    def _make_label_batch(labels):
        """
        Unify a List of List of labels to be a 2D Tensor with shape (b, m), where b = len(labels) and m is the max
        length of all the rows in labels.

        Args:
            labels (List[List]): the union labels of a data batch.

        Returns:
            2D Tensor.
        """
        max_len = max([len(label) for label in labels])
        batch_labels = np.zeros((len(labels), max_len))

        for idx, _ in enumerate(batch_labels):
            length = len(labels[idx])
            batch_labels[idx, :length] = np.array(labels[idx])

        return ms.Tensor(batch_labels, ms.int32)

    def _save_manifest(self):
        """Save manifest.json underneath datafile directory."""
        if self._manifest is None:
            raise RuntimeError("Manifest not yet be initialized.")
        path_tokens = [self._summary_dir,
                       self._DATAFILE_DIRNAME_PREFIX + str(self._summary_timestamp)]
        abs_dir_path = self._create_subdir(*path_tokens)
        save_path = os.path.join(abs_dir_path, self._MANIFEST_FILENAME)
        fd = os.open(save_path, os.O_WRONLY | os.O_CREAT, mode=self._FILE_MODE)
        file = os.fdopen(fd, "w")
        try:
            json.dump(self._manifest, file, indent=4)
        except IOError:
            log.error(f"Failed to save manifest as {save_path}!")
            raise
        finally:
            file.flush()
            os.close(fd)
        os.chmod(save_path, self._FILE_MODE)

    def _save_original_image(self, sample_id, image):
        """Save an image to summary directory."""
        id_dirname = self._get_sample_dirname(sample_id)
        path_tokens = [self._summary_dir,
                       self._DATAFILE_DIRNAME_PREFIX + str(self._summary_timestamp),
                       self._ORIGINAL_IMAGE_DIRNAME,
                       id_dirname]

        abs_dir_path = self._create_subdir(*path_tokens)
        filename = f"{sample_id}.jpg"
        save_path = os.path.join(abs_dir_path, filename)
        image.save(save_path)
        os.chmod(save_path, self._FILE_MODE)
        return os.path.join(*path_tokens[1:], filename)

    def _save_heatmap(self, explain_method, class_id, sample_id, image):
        """Save heatmap image to summary directory."""
        id_dirname = self._get_sample_dirname(sample_id)
        path_tokens = [self._summary_dir,
                       self._DATAFILE_DIRNAME_PREFIX + str(self._summary_timestamp),
                       self._HEATMAP_DIRNAME,
                       explain_method,
                       id_dirname]

        abs_dir_path = self._create_subdir(*path_tokens)
        filename = f"{sample_id}_{class_id}.jpg"
        save_path = os.path.join(abs_dir_path, filename)
        image.save(save_path, optimize=True)
        os.chmod(save_path, self._FILE_MODE)
        return os.path.join(*path_tokens[1:], filename)

    def _create_subdir(self, *args):
        """Recursively create subdirectories."""
        abs_path = None
        for token in args:
            if abs_path is None:
                abs_path = os.path.realpath(token)
            else:
                abs_path = os.path.join(abs_path, token)
            # os.makedirs() don't set intermediate dir permission properly, we mkdir() one by one
            try:
                os.mkdir(abs_path, mode=self._DIR_MODE)
                # In some platform, mode may be ignored in os.mkdir(), we have to chmod() again to make sure
                os.chmod(abs_path, mode=self._DIR_MODE)
            except FileExistsError:
                pass
        return abs_path

    @classmethod
    def _get_sample_dirname(cls, sample_id):
        """Get the name of parent directory of the image id."""
        return str(int(sample_id / cls._SAMPLE_PER_DIR) * cls._SAMPLE_PER_DIR)

    @staticmethod
    def _extract_timestamp(filename):
        """Extract timestamp from summary filename."""
        matched = re.search(r"summary\.(\d+)", filename)
        if matched:
            return int(matched.group(1))
        return None

    @classmethod
    def _spaced_print(cls, message):
        """Spaced message printing."""
        # workaround to print logs starting new line in case line width mismatch.
        print(cls._SPACER.format(message))
