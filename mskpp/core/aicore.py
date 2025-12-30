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
from .common import checker

# core type的集合，包含了不重复core类型，如aic0、aiv1等
core_type_list = list()


class Core:
    core_type = None

    def __init__(self, core_type_name):
        self.param_check(core_type_name)
        Core.set_core_type(core_type_name)
        if core_type_name not in core_type_list:
            core_type_list.append(core_type_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_core_type()

    @staticmethod
    def set_core_type(core_type_input):
        Core.core_type = core_type_input

    @staticmethod
    def get_core_type():
        return Core.core_type

    @staticmethod
    def clear_core_type():
        Core.core_type = None

    @staticmethod
    def get_instr_pipe_name(src, dst):
        '''
        :param src: mov instr src tensor
        :param dst: mov instr dst tensor
        :return: pipe name
        '''
        pipe_name = arch.get_pipe_by_io(src, dst)
        return Core.get_aicore_pipe_name(pipe_name)

    @staticmethod
    def get_aicore_pipe_name(pipe_name):
        return pipe_name if Core.core_type is None else (Core.core_type + "-" + pipe_name)

    @staticmethod
    def param_check(core_type_name):
        checker.check_name_valid(core_type_name, "core_type_name")
