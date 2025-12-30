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

import os
from mskpp.utils import logger
from ..common.singleton import Singleton
from ..common import checker
from .mem_metrics import MemMetrics
from .cycle_metrics import CycleMetrics
from .cal_metrics import CalMetrics
from .metrics_summary import PipeMetricsSummary, InstructionMetricsSummary


@Singleton
class Metrics:
    def __init__(self):
        self.is_enable = False
        self.need_instr_log = True

    @staticmethod
    def add_event(task_obj):
        if task_obj.instr_obj.name == "MOV":
            MemMetrics().add_event(task_obj.owner, task_obj.instr_obj)
        else:
            CalMetrics().add_event(task_obj.owner, task_obj.instr_obj)
        CycleMetrics().add_event(task_obj.owner, task_obj.instr_obj)

    @staticmethod
    def summary(output_dir):
        if Metrics().need_instr_log:
            logger.info("Metrics:")
        CycleMetrics().summary(output_dir)
        MemMetrics().summary()
        CalMetrics().summary()
        pipe_csv = os.path.join(output_dir, "Pipe_statistic.csv")
        if checker.check_path_exists(pipe_csv):
            raise Exception("The file {} already exists, cannot generate, please remove it first".format(pipe_csv))
        PipeMetricsSummary().output(pipe_csv)
        instruction_csv = os.path.join(output_dir, "Instruction_statistic.csv")
        if checker.check_path_exists(instruction_csv):
            raise Exception("The file {} already exists, cannot generate, please remove it first".
                            format(instruction_csv))
        InstructionMetricsSummary().output(instruction_csv)
    
    @staticmethod
    def set_total_duration(duration):
        PipeMetricsSummary().set_total_duration(duration)
    
    @staticmethod
    def set_prof_summary_path(file_path):
        PipeMetricsSummary().set_prof_summary_path(file_path)

    def metrics_clear(self):
        self.__init__()
        MemMetrics().mem_metrics_clear()
        CalMetrics().cal_metrics_clear()
        CycleMetrics().cycle_metrics_clear()
        PipeMetricsSummary().pipe_metrics_summary_clear()
        InstructionMetricsSummary().instruction_metrics_summary_clear()

    def set_enable(self, enable):
        self.is_enable = enable

    def disable_instr_log(self):
        CycleMetrics().set_instr_log(False)
        self.need_instr_log = False
