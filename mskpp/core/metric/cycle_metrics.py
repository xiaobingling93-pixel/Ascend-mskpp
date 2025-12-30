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

from mskpp._C import arch

from mskpp.utils import logger
from .metrics_summary import PipeMetricsSummary, InstructionMetricsSummary
from .visualization_tool import DataVisualization
from ..common import Singleton, checker
from ..vec_scope import SimdVf


@Singleton
class CycleMetrics:
    def __init__(self):
        self._summary = {}
        self._total_summary = {
            "cycle": 0  # cycle数目
        }
        self.is_need_instr_log = True

    def cycle_metrics_clear(self):
        self.__init__()

    def set_instr_log(self, instr_log):
        self.is_need_instr_log = instr_log

    def add_event(self, pipe_name, instr_obj):
        if pipe_name not in self._summary.keys():
            self._summary[pipe_name] = CyclePipeMetrics(pipe_name, self.is_need_instr_log)
        cycle = instr_obj.cost_time()
        cycle = SimdVf.update_metrics_cycle_with_task_name(instr_obj.task_name, cycle)
        self._summary[pipe_name].add_event(
            CycleEvent(instr_obj.task_name, cycle))
        self._total_summary["cycle"] += cycle

    def summary(self, output_dir):
        for pipe_name in self._summary.keys():
            self._summary[pipe_name].summary()
        PipeMetricsSummary().update(
            "Total", "Cycle", self._total_summary["cycle"])
        # visualization

        event_names = []
        event_cycles = []
        for pipe_name in self._summary.keys():
            events = list(self._summary[pipe_name].get_cycle_events())
            for event in events:
                event_names.append(event.name)
                event_cycles.append(event.cycle)
        filename = "instruction_cycle_consumption.html"
        html_path = os.path.join(output_dir, filename)
        if checker.check_path_exists(html_path):
            raise Exception("The file {} already exists, cannot generate, please remove it first".format(html_path))
        DataVisualization.cycle_info_visualization(event_names, event_cycles, "Instruction Cycle Consumption",
                                                   html_path)


class CycleEvent:
    def __init__(self, name, cycle):
        self.name = name
        self.cycle = cycle


class CycleEvents:
    '''
    统计每条指令的累积占用cycle数
    '''

    def __init__(self, name):
        self.name = name
        self.cycle = 0
        self.cycle_list = []

    def __str__(self):
        msg = "{} : cycle {}, {}".format(
            self.name, self.cycle, self.cycle_list)
        return msg

    def add_event(self, event):
        self.cycle += event.cycle
        self.cycle_list.append(event.cycle)


class CyclePipeMetrics:
    '''
    统计每条pipeline中的cycle占用信息
    '''

    def __init__(self, name, is_need_instr_log=True):
        self.name = name
        self._detail = {}
        self._summary = {
            "cycle": 0  # cycle数目
        }
        self.is_need_instr_log = is_need_instr_log

    def add_event(self, event):
        if event.name not in self._detail.keys():
            self._detail[event.name] = CycleEvents(event.name)
        self._detail[event.name].add_event(event)
        self._summary["cycle"] += event.cycle

    def summary(self):
        PipeMetricsSummary().update(self.name, "Duration(us)", round(arch.cal_duration(self._summary["cycle"]), 4))
        PipeMetricsSummary().update(self.name, "Cycle", self._summary["cycle"])
        for inst, event in self._detail.items():
            InstructionMetricsSummary().update(inst, "Duration(us)",
                                               round(arch.cal_duration(event.cycle), 4))
            InstructionMetricsSummary().update(inst, "Cycle", event.cycle)
            if self.is_need_instr_log:
                logger.info(f"{inst} CycleList: {str(event.cycle_list)}")

    def get_cycle_events(self):
        return self._detail.values()
