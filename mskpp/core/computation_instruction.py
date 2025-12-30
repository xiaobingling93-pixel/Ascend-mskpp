#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------
# This file is part of the MindStudio project.
# Copyright (c) 2025 Huawei Technologies Co.,Ltd.
#
# MindStudio is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
# -------------------------------------------------------------------------

from abc import abstractmethod
from .instruction_base import InstructionBase
from .common.checker import is_required_type
from .tensor import Tensor
from .vec_scope import VecScope, SimdVf
from .aicore import Core


class ComputationInstruction(InstructionBase):
    def __init__(self, name, inputs, outputs, attr=None, instr_type=None):
        super(ComputationInstruction, self).__init__(name, inputs, outputs, attr)
        self.task_name = name  # 当这个指令任务执行时，使用task_name
        self.instr_type = instr_type
        self.init_param_check()
        self.scope_name_with_core = VecScope.get_scope_name_with_core()

    @abstractmethod
    def infer_shape(self, inputs, outputs, attr):
        '''
        由输入的Tensor信息推断输出的Tensor
        :return:
        '''
        raise NotImplementedError("infer_shape should impl.")

    def get_prof_data_obj(self):
        from .prof_data import ProfDataRegister
        prof_data_by_name = ProfDataRegister.get(self.name)
        if prof_data_by_name is None:
            raise Exception("computational instruction {} didn't be register".format(self.name))
        return prof_data_by_name(self.inputs, self.outputs)

    def instr_check(self, inputs, outputs, attr):
        self.infer_shape(inputs, outputs, attr)

    def init_param_check(self):
        for tensor in self.inputs:
            if not is_required_type(tensor, Tensor):
                raise Exception("Computational instruction inputs should be Tensor, but got {}".format(type(tensor)))
            if not tensor.is_complete():
                raise Exception("{}'s input(Tensor:{}) is not complete.".format(self.task_name, tensor))
        for tensor in self.outputs:
            if not is_required_type(tensor, Tensor):
                raise Exception("Computational instruction output should be Tensor, but got {}".format(type(tensor)))

    def cal_size(self):
        prof_data_obj = self.get_prof_data_obj()
        return prof_data_obj.size()

    def cost_time(self):
        '''
        依据表格查询具体耗时
        :return:
        '''
        prof_data_obj = self.get_prof_data_obj()
        return prof_data_obj.time()

    def launch(self, inputs, outputs, attr):
        from mskpp.core.instr_task import InstrTask
        from mskpp._C import task_schedule
        from .prof_data import ProfDataRegister
        pipe_name = ProfDataRegister.get(self.name)(self.inputs, self.outputs).pipe_name()
        if self.inputs[0].mem_type == "VEC":
            pipe_name = SimdVf.consume_exu_instr()
        task = InstrTask(pipe_name, self)
        task_schedule.Schedule().add_task(task)
