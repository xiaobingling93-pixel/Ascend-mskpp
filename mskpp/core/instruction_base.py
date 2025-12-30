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
from abc import ABC, abstractmethod

from mskpp.utils import logger
from .chip import Chip


class InstructionBase(ABC):
    instr_num = 0

    def __init__(self, name, inputs, outputs, attr=None):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.attr = attr if attr else None
        InstructionBase.instr_num += 1

    def __call__(self, *args, **kwargs):
        self.instr_check(self.inputs, self.outputs, self.attr)
        self.trace_info(self.inputs, self.outputs, self.attr)
        self.launch(self.inputs, self.outputs, self.attr)
        return self.outputs

    @abstractmethod
    def launch(self, inputs, outputs, attr=None):
        '''
        此处仅需要执行指令，检测由instr_check完成
        :param inputs:
        :param outputs:
        :return:
        '''
        raise NotImplementedError("inner_exec should impl.")

    @abstractmethod
    def instr_check(self, inputs, outputs, attr):
        '''
        对于指令执行前的参数内容进行检测，如果指令信息本身不全，需要在此补齐
        :return:
        '''
        raise NotImplementedError("instr_check should impl.")

    def trace_info(self, inputs, outputs, attr):
        if Chip.need_instr_log is False:
            return
        io = inputs + outputs
        if isinstance(inputs, str):
            logger.info("{}".format(self.name))
            return
        msg = "{} ".format(self.name)
        msgs = []
        for item in io:
            msgs.append("{}".format(item))
        msg += ', '.join(msgs)
        logger.info(msg)

    def is_ready(self):
        for tensor in self.inputs:
            if tensor.father_tensor and tensor.father_tensor.is_valid():
                return True
            if not tensor.is_valid():
                return False
        return True

    @abstractmethod
    def cost_time(self):
        pass

    def schedule_post(self):
        '''
        该内容用于调度控制使用
        :return:
        '''
        for tensor in self.outputs:
            tensor.set_valid()
