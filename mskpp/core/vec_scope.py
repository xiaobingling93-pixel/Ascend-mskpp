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
from .aicore import Core


class NumberGeneration:
    def __init__(self, max_num):
        if max_num <= 0:
            raise ValueError("Resource num should >= 0")
        self.max_num = max_num
        self.cur_num = 0

    def get_next(self):
        num = self.cur_num % self.max_num
        self.cur_num += 1
        return num


class VecScope:
    scope_name = None
    ld_num = None
    ex_num = None

    def __init__(self, vec_scope_name):
        VecScope.set_scope_name(vec_scope_name)

    def __enter__(self):
        VecScope.ld_num = NumberGeneration(2)
        VecScope.ex_num = NumberGeneration(2)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        VecScope.ld_num = None
        VecScope.ex_num = None
        self.clear_scope_name()

    @staticmethod
    def set_scope_name(scope_name_input):
        VecScope.scope_name = scope_name_input

    @staticmethod
    def get_scope_name():
        return VecScope.scope_name

    @staticmethod
    def get_scope_name_with_core():
        res = VecScope.scope_name
        if res is not None:
            res = res if Core.core_type is None else (Core.core_type + "-" + res)
        return res

    @staticmethod
    def clear_scope_name():
        VecScope.scope_name = None


class SimdVf:
    @staticmethod
    def update_vec_scope(trace_pipe_vec_list, start_time, end_time):
        if len(trace_pipe_vec_list) != 2:
            return [None, None]
        if trace_pipe_vec_list[0] is None:
            trace_pipe_vec_list[0] = start_time
        else:
            trace_pipe_vec_list[0] = min(trace_pipe_vec_list[0], start_time)

        if trace_pipe_vec_list[1] is None:
            trace_pipe_vec_list[1] = end_time
        else:
            trace_pipe_vec_list[1] = max(trace_pipe_vec_list[1], end_time)
        return trace_pipe_vec_list

    @staticmethod
    def is_simd_vec_out(mem_type):
        return mem_type == "VEC"

    @staticmethod
    def is_simd_vec_in(input_mem_type, output_mem_type):
        return input_mem_type == "UB" and output_mem_type == "VEC"

    @staticmethod
    def adjust_task_name_by_mem_type(input_mem_type, output_mem_type, task_name):
        if SimdVf.is_simd_vec_in(input_mem_type, output_mem_type):
            task_name = "RV_VLD"
        elif SimdVf.is_simd_vec_out(input_mem_type):
            task_name = "RV_VST"
        return task_name

    @staticmethod
    def get_simd_vec_cost(input_mem_type, output_mem_type):
        if SimdVf.is_simd_vec_in(input_mem_type, output_mem_type) or SimdVf.is_simd_vec_out(input_mem_type):
            return 2  # actually simd vf mov instr cycle is 1.assignment 2 is for trace display,metrics will rewrite 1
        return None

    @staticmethod
    def update_metrics_cycle_with_task_name(task_name, cycle):
        if task_name == "RV_VLD" or task_name == "RV_VST":
            cycle = 1  # simd vf mov instr is 1
        if task_name in ["RV_VADD", "RV_VSUB", "RV_VMAX", "RV_VMIN", "RV_VABSDIF", "RV_VADDS"]:
            cycle = 3  # should get diff simd vf compute instr cycle
        return cycle

    @staticmethod
    def consume_exu_instr():
        pipe_name = "RVECEX" + str(VecScope.ex_num.get_next())
        pipe_name = pipe_name if Core.core_type is None else (Core.core_type + "-" + pipe_name)
        return pipe_name

    @staticmethod
    def consume_ldu_instr(input_mem_type, output_mem_type):
        if input_mem_type == "UB" and output_mem_type == "VEC":
            pipe_name = "RVECLD" + str(VecScope.ld_num.get_next())
            pipe_name = pipe_name if Core.core_type is None else (Core.core_type + "-" + pipe_name)
            return pipe_name
        return None
