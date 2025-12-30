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

from .metrics_summary import PipeMetricsSummary, InstructionMetricsSummary
from ..common import Singleton


@Singleton
class CalMetrics:
    def __init__(self):
        self._summary = {}
        self._total_summary = {
            "size": 0  # 计算量， 单位：OPS
        }

    def cal_metrics_clear(self):
        self.__init__()

    def add_event(self, pipe_name, instr_obj):
        if pipe_name not in self._summary.keys():
            self._summary[pipe_name] = CalPipeMetrics(pipe_name)
        size = instr_obj.cal_size()
        self._summary[pipe_name].add_event(CalEvent(instr_obj.task_name, size))
        self._total_summary["size"] += size

    def summary(self):
        for pipe_name in self._summary.keys():
            self._summary[pipe_name].summary()
        PipeMetricsSummary().update(
            "Total", "Ops", self._total_summary["size"])


class CalEvent:
    def __init__(self, name, size):
        self.name = name
        self.cal_size = size


class CalEvents:
    '''
    统计每类事件的累积数据
    '''

    def __init__(self, name):
        self.name = name
        self.cal_size = 0

    def __str__(self):
        msg = "{} : size(OPS) {}".format(self.name, self.cal_size)
        return msg

    def add_event(self, event):
        self.cal_size += event.cal_size


class CalPipeMetrics:
    '''
    统计每个pipe的信息
    '''

    def __init__(self, name):
        self.name = name
        self._detail = {}
        self._summary = {
            "size": 0  # 计算量， 单位：OPS
        }

    def add_event(self, event):
        if event.name not in self._detail.keys():
            self._detail[event.name] = CalEvents(event.name)
        self._detail[event.name].add_event(event)
        self._summary["size"] += event.cal_size

    def summary(self):
        PipeMetricsSummary().update(self.name, "Ops", self._summary["size"])
        for inst, event in self._detail.items():
            InstructionMetricsSummary().update(inst, "Ops", event.cal_size)
