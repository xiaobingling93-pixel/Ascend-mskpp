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

from mskpp._C import arch
from .instruction_base import InstructionBase
from .prof_data import ProfDataRegister
from .vec_scope import VecScope, SimdVf


class MemoryInstruction(InstructionBase):
    def __init__(self, src, dst, trans_enable, repeat, set_value_input=-1, expect_value_input=-1):
        super(MemoryInstruction, self).__init__("MOV", (src,), (dst,))
        self.task_name = "{}-{}_TO_{}".format("MOV", src.mem_type, dst.mem_type)
        self.task_name = SimdVf.adjust_task_name_by_mem_type(self.inputs[0].mem_type, self.outputs[0].mem_type,
                                                             self.task_name)
        self.trans_enable = trans_enable
        self.repeat = repeat
        self.set_value = set_value_input
        self.expect_value = expect_value_input
        self.scope_name_with_core = VecScope.get_scope_name_with_core()
        self.prof_data_name = self.task_name if ProfDataRegister.is_prof_data_exist(self.task_name) else self.name
        self.prof_data_obj = ProfDataRegister.get(self.prof_data_name)(self.inputs, self.outputs, self.trans_enable,
                                                                       self.repeat)
        self.para_check()

    def para_check(self):
        if self.prof_data_name is None:
            raise Exception("prof data name is None")
        if self.prof_data_obj is None:
            raise Exception("prof data obj is None")

    def launch(self, inputs, outputs, attr):
        from .instr_task import InstrTask
        from mskpp._C import task_schedule
        pipe_name = SimdVf.consume_ldu_instr(self.inputs[0].mem_type, self.outputs[0].mem_type)
        if pipe_name is None:
            pipe_name = self.prof_data_obj.pipe_name()
        task = InstrTask(pipe_name, self)
        task_schedule.Schedule().add_task(task)

    def cost_time(self):
        res = SimdVf.get_simd_vec_cost(self.inputs[0].mem_type, self.outputs[0].mem_type)
        if res is None:
            return self.prof_data_obj.time()
        else:
            return res

    def move_size(self):
        return self.prof_data_obj.size()

    def instr_check(self, inputs, outputs, attr):
        if self.prof_data_name == self.name:
            src = inputs[0]
            dst = outputs[0]
            if not arch.mte_is_valid(src.mem_type, dst.mem_type):
                raise Exception("chip is not support move data from {} to {}".format(src.mem_type, dst.mem_type))

    def is_ready(self):
        # is_ready用于判断tensor是否处于valid状态
        # 如果有tensor依赖其他tensor，需要去查询依赖的tensor是否是自己期望的值
        # 判断MOV指令input的tensor的值是否符合预期
        if self.inputs[0].tensor_value != self.expect_value:
            return False
        return super().is_ready()

    def schedule_post(self):
        # 对于MOV指令task结束之后，给输出的tensor设置值
        if self.set_value != -1:
            self.outputs[0].tensor_value = self.set_value
        super().schedule_post()
