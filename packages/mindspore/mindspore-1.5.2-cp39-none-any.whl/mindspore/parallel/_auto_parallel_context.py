# Copyright 2020 Huawei Technologies Co., Ltd
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
"""Context of auto parallel"""
import threading

import mindspore.context as context
import mindspore.log as logger
from mindspore.parallel._dp_allreduce_fusion import _set_fusion_strategy_by_idx, _set_fusion_strategy_by_size
from mindspore.parallel._ps_context import _is_role_pserver
from mindspore._c_expression import AutoParallelContext
from mindspore._checkparam import args_type_check, Validator

_MAX_GROUP_NAME_LEN = 127
_DEFAULT_HCCL_FUSION_GROUP_NAME = "hccl_world_groupsum1"
_DEFAULT_NCCL_FUSION_GROUP_NAME = "nccl_world_groupsum1"


class _AutoParallelContext:
    """
    _AutoParallelContext is the environment in which operations are executed

    Note:
        Create a context through instantiating Context object is not recommended.
        Should use auto_parallel_context() to get the context since Context is singleton.
    """
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        self._context_handle = AutoParallelContext.get_instance()
        self._dataset_strategy_using_str = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance_lock.acquire()
            cls._instance = object.__new__(cls)
            cls._instance_lock.release()
        return cls._instance

    def check_context_handle(self):
        """
        Check context handle.

        Raises:
            ValueError: If the context handle is none.
        """
        if self._context_handle is None:
            raise ValueError("Context handle is none in context!!!")

    def set_device_num(self, device_num):
        """
        Set device num for auto parallel.

        Args:
            device_num (int): The device number.

        Raises:
            ValueError: If the device num is not in [1, 4096].
        """
        self.check_context_handle()
        if device_num < 1 or device_num > 4096:
            raise ValueError("Device num must be in [1, 4096], but got {}".format(device_num))
        from mindspore.communication._comm_helper import _HCCL_TEST_AVAILABLE
        self._context_handle.set_hccl_test_avaible(_HCCL_TEST_AVAILABLE)
        self._context_handle.set_device_num(device_num)

    def get_device_num(self):
        """Get device num."""
        self.check_context_handle()
        return self._context_handle.get_device_num()

    def set_global_rank(self, global_rank):
        """
        Set global rank for auto parallel.

        Args:
            global_rank (int): The rank id of current rank.

        Raises:
            ValueError: If the global rank is not in [1, 4096].
        """
        self.check_context_handle()
        if global_rank < 0 or global_rank > 4095:
            raise ValueError("Global rank must be in [0, 4095], but got {}".format(global_rank))
        self._context_handle.set_global_rank(global_rank)

    def get_global_rank(self):
        """Get current rank id."""
        self.check_context_handle()
        return self._context_handle.get_global_rank()

    def set_pipeline_stages(self, stages):
        """Set the stages of the pipeline"""
        if isinstance(stages, bool):
            raise TypeError("The type of pipeline_stage_num must be int, but got bool.")
        if not isinstance(stages, int):
            raise TypeError("The type of pipeline_stage_num must be int.")
        if stages < 1:
            raise ValueError("pipeline_stage_num can't be less than 1.")
        backend = context.get_context("device_target")
        if backend == "GPU" and stages > 1:
            raise RuntimeError("Now GPU don't support pipeline parallel.")
        self.check_context_handle()
        self._context_handle.set_pipeline_stage_split_num(stages)

    def get_pipeline_stages(self):
        """Get the stages of the pipeline"""
        self.check_context_handle()
        return self._context_handle.get_pipeline_stage_split_num()

    def set_gradients_mean(self, gradients_mean):
        """
        Set gradients_mean flag.

        Note:
            If gradients_mean is true, it will insert a div operator after parameter gradients allreduce.

        Args:
            gradients_mean (bool): The gradients_mean flag.
        """
        self.check_context_handle()
        self._context_handle.set_gradients_mean(gradients_mean)

    def get_gradients_mean(self):
        """Get gradients_mean flag."""
        self.check_context_handle()
        return self._context_handle.get_gradients_mean()

    def set_gradient_fp32_sync(self, gradient_fp32_sync):
        """
        Set gradient_fp32_sync.

        Note:
            If gradient_fp32_sync is true,
            it will convert tensor type from fp16 to fp32 before parameter gradients allreduce.

        Args:
            gradient_fp32_sync (bool): The gradient_fp32_sync flag.
        """
        self.check_context_handle()
        self._context_handle.set_gradient_fp32_sync(gradient_fp32_sync)

    def get_gradient_fp32_sync(self):
        """Get gradient_fp32_sync flag."""
        self.check_context_handle()
        return self._context_handle.get_gradient_fp32_sync()

    def set_loss_repeated_mean(self, loss_repeated_mean):
        """
        Set loss_repeated_mean flag.

        Note:
            If loss_repeated_mean is true,
            Distributed automatic differentiation will perform a mean operator
            in backward in the case of repeated calculations.

        Args:
            loss_repeated_mean (bool): The loss_repeated_mean flag.
        """
        if not isinstance(loss_repeated_mean, bool):
            raise TypeError(f"The type of loss_repeated_mean must be bool, but got {type(loss_repeated_mean)}.")
        self.check_context_handle()
        self._context_handle.set_loss_repeated_mean(loss_repeated_mean)

    def get_loss_repeated_mean(self):
        """Get loss_repeated_mean flag."""
        self.check_context_handle()
        return self._context_handle.get_loss_repeated_mean()

    def set_parallel_mode(self, parallel_mode):
        """
        Set parallel mode for auto parallel.

        Args:
            parallel_mode (str): The parallel mode of auto parallel.

        Raises:
            ValueError: If parallel mode is not supported.
        """
        self.check_context_handle()
        run_mode = context.get_context("mode")
        if run_mode == context.PYNATIVE_MODE and parallel_mode not in (
                context.ParallelMode.DATA_PARALLEL, context.ParallelMode.STAND_ALONE):
            raise ValueError(f"Pynative Only support STAND_ALONE and DATA_PARALLEL for ParallelMode, "
                             f"but got {parallel_mode.upper()}.")
        ret = self._context_handle.set_parallel_mode(parallel_mode)
        if ret is False:
            raise ValueError("Parallel mode does not support {}".format(parallel_mode))

    def get_parallel_mode(self):
        """Get parallel mode."""
        self.check_context_handle()
        if _is_role_pserver():
            return context.ParallelMode.STAND_ALONE
        return self._context_handle.get_parallel_mode()

    def set_strategy_search_mode(self, auto_parallel_search_mode):
        """
        Set search mode of strategy.

        Args:
            auto_parallel_search_mode (str): The search mode of strategy.
        """
        self.check_context_handle()
        ret = self._context_handle.set_strategy_search_mode(auto_parallel_search_mode)
        if ret is False:
            raise ValueError("Strategy search mode does not support {}".format(auto_parallel_search_mode))

    def get_strategy_search_mode(self):
        """Get search mode of strategy."""
        self.check_context_handle()
        return self._context_handle.get_strategy_search_mode()

    def set_parameter_broadcast(self, parameter_broadcast):
        """
        Set parameter broadcast.

        Args:
            parameter_broadcast (bool): Parameter broadcast or not.
        """
        self.check_context_handle()
        self._context_handle.set_parameter_broadcast(parameter_broadcast)

    def get_parameter_broadcast(self):
        """Get parameter broadcast flag."""
        self.check_context_handle()
        return self._context_handle.get_parameter_broadcast()

    def set_strategy_ckpt_load_file(self, strategy_ckpt_load_file):
        """
        Set strategy checkpoint load path.

        Args:
            strategy_ckpt_load_file (str): Path to load parallel strategy checkpoint.
        """
        self.check_context_handle()
        self._context_handle.set_strategy_ckpt_load_file(strategy_ckpt_load_file)

    def get_strategy_ckpt_load_file(self):
        """Get strategy checkpoint load path."""
        self.check_context_handle()
        return self._context_handle.get_strategy_ckpt_load_file()

    def set_full_batch(self, full_batch):
        """
        Set whether load full batch on each device.

        Args:
            full_batch (bool): True if load full batch on each device.
        """
        self.check_context_handle()
        self._context_handle.set_full_batch(full_batch)

    def get_full_batch(self):
        """Get whether load full batch on each device."""
        self.check_context_handle()
        if _is_role_pserver():
            return False
        return self._context_handle.get_full_batch()

    def set_dataset_strategy(self, dataset_strategy):
        """
        Set dataset sharding strategy.

        Args:
            dataset_strategy (str or tuple(tuple)): The dataset sharding strategy.
        """
        self.check_context_handle()
        if isinstance(dataset_strategy, str):
            if dataset_strategy not in ("full_batch", "data_parallel"):
                raise ValueError("The dataset_strategy string should be 'full_batch' or 'data_parallel', "
                                 "otherwise, incoming tuple(tuple) type strategy")
            self._context_handle.set_full_batch(dataset_strategy == "full_batch")
            self._dataset_strategy_using_str = True
            return
        if not isinstance(dataset_strategy, tuple):
            raise TypeError(f'strategy must be str or tuple type, but got:{type(dataset_strategy)}')
        for ele in dataset_strategy:
            if not isinstance(ele, tuple):
                raise TypeError(f'The element of strategy must be tuple type, but got:{type(ele)}')
            for dim in ele:
                if not isinstance(dim, int):
                    raise TypeError(f'The dim of each strategy value must be int type, but got:{type(dim)}')
        self._dataset_strategy_using_str = False
        self._context_handle.set_dataset_strategy(dataset_strategy)

    def get_dataset_strategy(self):
        """Get dataset sharding strategy."""
        self.check_context_handle()
        if self._dataset_strategy_using_str:
            if self._context_handle.get_full_batch():
                return "full_batch"
            return "data_parallel"
        return self._context_handle.get_dataset_strategy()

    def set_grad_accumulation_step(self, grad_accumulation_step):
        """
        Set grad accumulation step.

        Args:
            grad_accumulation_step (int): The grad accumulation step.
        """
        self.check_context_handle()
        Validator.check_positive_int(grad_accumulation_step)
        self._context_handle.set_grad_accumulation_step(grad_accumulation_step)

    def get_grad_accumulation_step(self):
        """Get grad accumulation step."""
        self.check_context_handle()
        return self._context_handle.get_grad_accumulation_step()

    def set_strategy_ckpt_save_file(self, strategy_ckpt_save_file):
        """
        Set strategy checkpoint save path.

        Args:
            strategy_ckpt_save_file (bool): Path to save parallel strategy checkpoint.
        """
        self.check_context_handle()
        import os
        dir_path = os.path.dirname(strategy_ckpt_save_file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self._context_handle.set_strategy_ckpt_save_file(strategy_ckpt_save_file)

    def get_strategy_ckpt_save_file(self):
        """Get strategy checkpoint save path."""
        self.check_context_handle()
        return self._context_handle.get_strategy_ckpt_save_file()

    def set_group_ckpt_save_file(self, group_ckpt_save_file):
        """Set group checkpoint save path."""
        self.check_context_handle()
        import os
        dir_path = os.path.dirname(group_ckpt_save_file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self._context_handle.set_group_ckpt_save_file(group_ckpt_save_file)

    def get_parameter_broadcast_is_set(self):
        """Get parameter broadcast is set or not."""
        self.check_context_handle()
        return self._context_handle.get_parameter_broadcast_is_set()

    def set_all_reduce_fusion_split_indices(self, indices, group=""):
        """
        Set allreduce fusion strategy by parameters indices.

        Args:
            indices (list): Indices list.
            group (str): The communication group of hccl/nccl.

        Raises:
            TypeError: If type of indices item is not int.
            TypeError: If group is not a python str.
        """
        self.check_context_handle()
        if not indices:
            raise ValueError('indices can not be empty')

        if isinstance(indices, (list)):
            for index in indices:
                if not isinstance(index, int) or isinstance(index, bool):
                    raise TypeError(f"The type of index must be int, but got {type(index)}.")
        else:
            raise TypeError('indices must be a python list')

        if len(set(indices)) != len(indices):
            raise ValueError('indices has duplicate elements')

        if sorted(indices) != indices:
            raise ValueError('elements in indices must be sorted in ascending order')

        new_group = self._check_and_default_group(group)

        self._context_handle.set_all_reduce_fusion_split_indices(indices, new_group)
        if context.get_context("device_target") == "Ascend" and context.get_context("enable_ge"):
            _set_fusion_strategy_by_idx(indices)

    def get_all_reduce_fusion_split_indices(self, group=""):
        """
        Get allreduce fusion split indices.

        Args:
            group (str): The communication group of hccl/nccl.

        Returns:
            Return split sizes list according to the group.

        Raises:
            TypeError: If group is not a python str.
        """
        self.check_context_handle()
        new_group = self._check_and_default_group(group)
        return self._context_handle.get_all_reduce_fusion_split_indices(new_group)

    def set_all_reduce_fusion_split_sizes(self, sizes, group=""):
        """
        Set allreduce fusion strategy by parameters data sizes.

        Args:
            sizes (list): Sizes list.
            group (str): The communication group of hccl/nccl.

        Raises:
            TypeError: If type of sizes item is not int.
            TypeError: If group is not a python str.
        """
        self.check_context_handle()
        if isinstance(sizes, (list)):
            for size in sizes:
                if not isinstance(size, int) or isinstance(size, bool):
                    raise TypeError(f"The type of size must be int, but got {type(size)}.")
        else:
            raise TypeError('sizes must be a python list')

        new_group = self._check_and_default_group(group)
        self._context_handle.set_all_reduce_fusion_split_sizes(sizes, new_group)
        if context.get_context("device_target") == "Ascend":
            _set_fusion_strategy_by_size(sizes)

    def get_all_reduce_fusion_split_sizes(self, group=""):
        """
        Get allreduce fusion split sizes.

        Args:
            group (str): The communication group of hccl/nccl.

        Returns:
            Return split sizes list according to the group.

        Raises:
            TypeError: If group is not a python str.
        """
        self.check_context_handle()
        new_group = self._check_and_default_group(group)
        return self._context_handle.get_all_reduce_fusion_split_sizes(new_group)

    def set_enable_all_reduce_fusion(self, enable_all_reduce_fusion):
        """
        Set enable/disable all reduce fusion.

        Args:
            enable_all_reduce_fusion (bool): Enable/disable all reduce fusion.
        """
        self.check_context_handle()
        if not isinstance(enable_all_reduce_fusion, bool):
            raise TypeError('enable_all_reduce_fusion is invalid type')
        self._context_handle.set_enable_all_reduce_fusion(enable_all_reduce_fusion)

    def get_enable_all_reduce_fusion(self):
        """Get all reduce fusion flag."""
        self.check_context_handle()
        return self._context_handle.get_enable_all_reduce_fusion()

    def get_device_num_is_set(self):
        """Get device number is set or not."""
        self.check_context_handle()
        return self._context_handle.get_device_num_is_set()

    def get_global_rank_is_set(self):
        """Get global rank is set or not."""
        self.check_context_handle()
        return self._context_handle.get_global_rank_is_set()

    def set_enable_parallel_optimizer(self, enable_parallel_optimizer):
        """
        Set enable/disable parallel optimizer.

        Args:
            set_enable_parallel_optimizer (bool): Enable/disable parallel optimizer.
        """
        self.check_context_handle()
        if not isinstance(enable_parallel_optimizer, bool):
            raise TypeError('enable_parallel_optimizer is invalid type')
        self._context_handle.set_enable_parallel_optimizer(enable_parallel_optimizer)

    def get_enable_parallel_optimizer(self):
        """Get parallel optimizer flag."""
        self.check_context_handle()
        return self._context_handle.get_enable_parallel_optimizer()

    def set_sharding_propagation(self, sharding_propagation):
        """
        Set the value of sharding strategy propagation in AUTO_PARALLEL mode. If True, the strategy-configured operators
        will propagate the strategies to other operators with minimum redistribution cost; otherwise, the algorithm
        will search the desired strategies.
        Default: False.

        Args:
            sharding_propagation (bool): Enable/disable strategy propagation.
        """
        self.check_context_handle()
        if not isinstance(sharding_propagation, bool):
            raise TypeError("'sharding_propagation' is an invalid type.")
        self._context_handle.set_sharding_propagation(sharding_propagation)

    def get_sharding_propagation(self):
        """Get the value of sharding strategy propagation."""
        self.check_context_handle()
        return self._context_handle.get_sharding_propagation()

    def set_enable_alltoall(self, enable_a2a):
        """
        Set the value of enabling AllToAll. If False, AllGather and Split are used to circumvent AllToAll.
        Default: False.

        Args:
            enable_a2a (bool): Enable/disable AllToAll.
        """
        self.check_context_handle()
        if not isinstance(enable_a2a, bool):
            raise TypeError("'enable_a2a' is an invalid type.")
        self._context_handle.set_enable_alltoall(enable_a2a)

    def get_enable_alltoall(self):
        """Get the value of enabling AllToAll."""
        self.check_context_handle()
        return self._context_handle.get_enable_alltoall()

    def set_communi_parallel_mode(self, communi_parallel_mode):
        """
        Set communication parallel mode.

        Args:
            communi_parallel_mode (str): The communication parallel mode.

        Raises:
            ValueError: If parallel mode is not supported.
        """
        if not isinstance(communi_parallel_mode, str):
            raise TypeError(f"The type of communi_parallel_mode must be str, \
                but got {type(communi_parallel_mode)}.")
        self.check_context_handle()
        ret = self._context_handle.set_communi_parallel_mode(communi_parallel_mode)
        if ret is False:
            raise ValueError("Communication parallel mode does not support {}".format(communi_parallel_mode))

    def get_communi_parallel_mode(self):
        """Get communication parallel mode."""
        self.check_context_handle()
        return self._context_handle.get_communi_parallel_mode()

    def set_optimizer_weight_shard_size(self, optimizer_weight_shard_size):
        """
        Set optimizer_weight_shard_size.

        Args:
            optimizer_weight_shard_size (int): Opt shard group size when not globally use parallel
                                               optimizer across devices.
        """
        self.check_context_handle()
        if not isinstance(optimizer_weight_shard_size, int) or isinstance(optimizer_weight_shard_size, bool):
            raise TypeError(f"The type of optimizer_weight_shard_size must be int, \
                but got {type(optimizer_weight_shard_size)}.")
        if optimizer_weight_shard_size <= 1:
            logger.warning("The setting 'optimizer_weight_shard_size' is invalid. "
                           "Please use the integer larger than 1.")
            return
        self._context_handle.set_optimizer_weight_shard_size(optimizer_weight_shard_size)

    def get_optimizer_weight_shard_size(self):
        """Get optimizer_weight_shard_size."""
        self.check_context_handle()
        return self._context_handle.get_optimizer_weight_shard_size()

    def set_optimizer_weight_shard_aggregated_save(self, optimizer_weight_shard_aggregated_save):
        """
        Set optimizer_weight_shard_aggregated_save.

        Args:
            optimizer_weight_shard_aggregated_save (bool): Whether to integrated save weight shard when
                                                           enable parallel optimizer.
        """
        self.check_context_handle()
        if not isinstance(optimizer_weight_shard_aggregated_save, bool):
            raise TypeError('optimizer_weight_shard_aggregated_save is invalid type')
        self._context_handle.set_optimizer_weight_shard_aggregated_save(optimizer_weight_shard_aggregated_save)


    def get_optimizer_weight_shard_aggregated_save(self):
        """Get optimizer_weight_shard_size."""
        self.check_context_handle()
        return self._context_handle.get_optimizer_weight_shard_aggregated_save()


    def reset(self):
        """Reset all settings."""
        self.check_context_handle()
        self._context_handle.reset()


    def _check_and_default_group(self, group):
        """Validate the given group, if group is empty, returns a default fusion group"""
        if isinstance(group, (str)):
            group_len = len(group)
            if group_len > _MAX_GROUP_NAME_LEN:
                raise ValueError('Group name len is out of range {_MAX_GROUP_NAME_LEN}')
        else:
            raise TypeError('Group must be a python str')

        if group == "":
            if context.get_context("device_target") == "Ascend":
                group = _DEFAULT_HCCL_FUSION_GROUP_NAME
            else:
                group = _DEFAULT_NCCL_FUSION_GROUP_NAME
        return group


_auto_parallel_context = None


def auto_parallel_context():
    """
    Get the global _auto_parallel_context, if it is not created, create a new one.

    Returns:
        _AutoParallelContext, the global auto parallel context.
    """
    global _auto_parallel_context
    if _auto_parallel_context is None:
        _auto_parallel_context = _AutoParallelContext()
    return _auto_parallel_context


_set_auto_parallel_context_func_map = {
    "device_num": auto_parallel_context().set_device_num,
    "global_rank": auto_parallel_context().set_global_rank,
    "gradients_mean": auto_parallel_context().set_gradients_mean,
    "gradient_fp32_sync": auto_parallel_context().set_gradient_fp32_sync,
    "loss_repeated_mean": auto_parallel_context().set_loss_repeated_mean,
    "pipeline_stages": auto_parallel_context().set_pipeline_stages,
    "parallel_mode": auto_parallel_context().set_parallel_mode,
    "auto_parallel_search_mode": auto_parallel_context().set_strategy_search_mode,
    "parameter_broadcast": auto_parallel_context().set_parameter_broadcast,
    "strategy_ckpt_load_file": auto_parallel_context().set_strategy_ckpt_load_file,
    "strategy_ckpt_save_file": auto_parallel_context().set_strategy_ckpt_save_file,
    "group_ckpt_save_file": auto_parallel_context().set_group_ckpt_save_file,
    "full_batch": auto_parallel_context().set_full_batch,
    "dataset_strategy": auto_parallel_context().set_dataset_strategy,
    "enable_parallel_optimizer": auto_parallel_context().set_enable_parallel_optimizer,
    "grad_accumulation_step": auto_parallel_context().set_grad_accumulation_step,
    "all_reduce_fusion_config": auto_parallel_context().set_all_reduce_fusion_split_indices,
    "communi_parallel_mode": auto_parallel_context().set_communi_parallel_mode,
    "optimizer_weight_shard_size": auto_parallel_context().set_optimizer_weight_shard_size,
    "optimizer_weight_shard_aggregated_save": auto_parallel_context().set_optimizer_weight_shard_aggregated_save,
    "sharding_propagation": auto_parallel_context().set_sharding_propagation,
    "enable_alltoall": auto_parallel_context().set_enable_alltoall}


_get_auto_parallel_context_func_map = {
    "device_num": auto_parallel_context().get_device_num,
    "global_rank": auto_parallel_context().get_global_rank,
    "gradients_mean": auto_parallel_context().get_gradients_mean,
    "gradient_fp32_sync": auto_parallel_context().get_gradient_fp32_sync,
    "loss_repeated_mean": auto_parallel_context().get_loss_repeated_mean,
    "pipeline_stages": auto_parallel_context().get_pipeline_stages,
    "parallel_mode": auto_parallel_context().get_parallel_mode,
    "auto_parallel_search_mode": auto_parallel_context().get_strategy_search_mode,
    "parameter_broadcast": auto_parallel_context().get_parameter_broadcast,
    "strategy_ckpt_load_file": auto_parallel_context().get_strategy_ckpt_load_file,
    "strategy_ckpt_save_file": auto_parallel_context().get_strategy_ckpt_save_file,
    "full_batch": auto_parallel_context().get_full_batch,
    "dataset_strategy": auto_parallel_context().get_dataset_strategy,
    "enable_parallel_optimizer": auto_parallel_context().get_enable_parallel_optimizer,
    "grad_accumulation_step": auto_parallel_context().get_grad_accumulation_step,
    "all_reduce_fusion_config": auto_parallel_context().get_all_reduce_fusion_split_indices,
    "communi_parallel_mode": auto_parallel_context().get_communi_parallel_mode,
    "optimizer_weight_shard_size": auto_parallel_context().get_optimizer_weight_shard_size,
    "optimizer_weight_shard_aggregated_save": auto_parallel_context().get_optimizer_weight_shard_aggregated_save,
    "sharding_propagation": auto_parallel_context().get_sharding_propagation,
    "enable_alltoall": auto_parallel_context().get_enable_alltoall}


@args_type_check(device_num=int, global_rank=int, gradients_mean=bool, gradient_fp32_sync=bool,
                 loss_repeated_mean=bool, parallel_mode=str, auto_parallel_search_mode=str,
                 parameter_broadcast=bool, strategy_ckpt_load_file=str,
                 strategy_ckpt_save_file=str, full_batch=bool, enable_parallel_optimizer=bool,
                 grad_accumulation_step=int, all_reduce_fusion_config=list, group_ckpt_save_file=str,
                 communi_parallel_mode=str, optimizer_weight_shard_size=int,
                 optimizer_weight_shard_aggregated_save=bool,
                 sharding_propagation=bool, enable_alltoall=bool)

def _set_auto_parallel_context(**kwargs):
    """
    Set auto parallel context.

    Note:
        Attribute name is required for setting attributes.

    Args:
        device_num (int): Available device number, the value must be in [1, 4096]. Default: 1.
        global_rank (int): Global rank id, the value must be in [0, 4095]. Default: 0.
        gradients_mean (bool): Whether to perform mean operator after all-reduce of mirror. Default: False.
        loss_repeated_mean (bool): Whether to perform mean operator in backward in the case of repeated
                        calculations. Default: True.
        gradient_fp32_sync (bool): Gradients allreduce by fp32 even though gradients is fp16 if this flag is True.
                        Default: True.
        parallel_mode (str): There are five kinds of parallel modes, "stand_alone", "data_parallel",
                     "hybrid_parallel", "semi_auto_parallel" and "auto_parallel". Default: "stand_alone".

                     - stand_alone: Only one processor working.

                     - data_parallel: Distributing the data across different processors.

                     - hybrid_parallel: Achieving data parallelism and model parallelism manually.

                     - semi_auto_parallel: Achieving data parallelism and model parallelism by
                       setting parallel strategies.

                     - auto_parallel: Achieving parallelism automatically.
        auto_parallel_search_mode (str): There are two kinds of search modes, "recursive_programming"
                     and "dynamic_programming". Default: "dynamic_programming".

                     - recursive_programming: Recursive programming search mode.

                     - dynamic_programming: Dynamic programming search mode.
        parameter_broadcast (bool): Indicating whether to broadcast parameters before training.
                       "stand_alone", "semi_auto_parallel" and "auto_parallel" do not support parameter
                       broadcast. Default: False.
        strategy_ckpt_load_file (str): The path to load parallel strategy checkpoint. Default: ''
        strategy_ckpt_save_file (str): The path to save parallel strategy checkpoint. Default: ''
        group_ckpt_save_file (str): The path to save parallel group checkpoint. Default: ''
        full_batch (bool): Whether to load the whole batch on each device. Default: False.
        dataset_strategy Union[str, tuple]: Dataset sharding strategy. Default: "data_parallel".
        enable_parallel_optimizer (bool): Enable using optimizer segmentation or not. Default: False.
        all_reduce_fusion_config (list): Set allreduce fusion strategy by parameters indices.
        pipeline_stages (int): Set the stage information for pipeline parallel. This indicates how
                        the devices are distributed alone the pipeline. The total devices will be divided into
                        'pipeline_stags' stages. This currently could only be used when
                        parallel mode semi_auto_parallel is enabled. Default: 0
        communi_parallel_mode (str): There are tree kinds of communication parallel modes, "all_group_parallel",
                     "same_server_group_parallel" and "no_group_parallel". Default: "all_group_parallel".

                     - all_group_parallel: All communication groups are in parallel.

                     - same_server_group_parallel: Only the communication groups within the same server are parallel.

                     - no_group_parallel: All communication groups are not parallel.
        optimizer_weight_shard_size (int): Set optimizer shard group size when not fully use parallel optimizer.
                                    It should be larger than one and less than or equal with the data parallel size.
                                    Default: -1, which means fully use parallel optimizer in data parallel dimension.
        optimizer_weight_shard_aggregated_save (bool): Whether to integrated save weight shard when enable parallel
                                                       optimizer. Default: False.
        sharding_propagation (bool): Set the value of sharding strategy propagation in AUTO_PARALLEL mode. If True,
                                    the strategy-configured operators will propagate the strategies to other
                                    operators with minimum redistribution cost; otherwise, the algorithm will
                                    search the desired strategies. Default: False.
        enable_alltoall (bool): Set the value of enabling AllToAll. If False, AllGather and Split are used to
                                circumvent AllToAll. Default: False.

    Raises:
        ValueError: If input key is not attribute in auto parallel context.
    """
    for key, value in kwargs.items():
        if key not in _set_auto_parallel_context_func_map:
            raise ValueError("Set context keyword %s is not recognized!" % key)
        set_func = _set_auto_parallel_context_func_map[key]
        set_func(value)


def _get_auto_parallel_context(attr_key):
    """
    Get auto parallel context attribute value according to the key.

    Args:
        attr_key (str): The key of the attribute.

    Returns:
        Return attribute value according to the key.

    Raises:
        ValueError: If input key is not attribute in auto parallel context.
    """
    if attr_key not in _get_auto_parallel_context_func_map:
        raise ValueError("Get context keyword %s is not recognized!" % attr_key)
    get_func = _get_auto_parallel_context_func_map[attr_key]
    return get_func()


def _reset_auto_parallel_context():
    """
    Reset auto parallel context attributes to the default values:

    - device_num: 1.
    - global_rank: 0.
    - gradients_mean: False.
    - gradient_fp32_sync: True.
    - parallel_mode: "stand_alone".
    - parameter_broadcast: False.
    - strategy_ckpt_load_file: ""
    - strategy_ckpt_save_file: ""
    - enable_parallel_optimizer: False
    - auto_parallel_search_mode: dynamic_programming
    - pipeline_stages: 0
    """
    auto_parallel_context().reset()
