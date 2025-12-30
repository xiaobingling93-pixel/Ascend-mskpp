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
import json
from collections import defaultdict
from mskpp._C import arch
from mskpp.utils import logger
from .common.singleton import Singleton
from .common import checker
from .metric.output_tool import SAVE_DATA_FILE_AUTHORITY, OPEN_FLAGS
from .aicore import core_type_list
from .vec_scope import SimdVf


pipes = {
    "PIPE-MTE1": 0,
    "PIPE-MTE2": 1,
    "PIPE-MTE3": 2,
    "PIPE-FIX": 3,
    "PIPE-M": 4,
    "PIPE-V": 5,
    "PIPE-S": 6,
    "PIPE-VEC": 7,
    "RVECLD": 8,
    "RVECEX": 9,
    "RVECLD0": 10,
    "RVECLD1": 11,
    "RVECEX0": 12,
    "RVECEX1": 13,
    "RVECLNQ": 14,
    "RVECST": 15,
}


class TraceEvent:
    def __init__(self, pipe_type, pipe_name, task_name, start_time, end_time, size, event_id=-1):
        self.pipe_type = pipe_type
        self.start_time = start_time
        self.dur = end_time - start_time
        self.size = size
        self.pipe_name = pipe_name         # eg:aic0-PIPE-MTE1
        self.task_name = task_name
        self.args = self.gen_args()
        self.core_type = str()
        self.pipe_id = int()
        self.gen_pipe_info()
        self.event_id = event_id

    def gen_pipe_info(self):
        def parse_core_type(core_type_input):
            if core_type_input in pipes.keys():
                return [None, core_type_input]
            pipe_name_list = core_type_input.split("-")
            if len(pipe_name_list) < 2:  # pipe name按照-分割,至少有2个基本单元
                raise Exception("Invalid pipe(The pipe name({}) is not support)".format(core_type_input))
            if pipe_name_list[0] == "PIPE":
                return [None, core_type_input]
            if pipe_name_list[1] in pipes.keys():  # eg:aic0-RVECLD0
                return [pipe_name_list[0], pipe_name_list[1]]
            if len(pipe_name_list) != 3:  # 带core信息的pipe name按照-分割,至少有3个基本单元
                raise Exception("Invalid pipe(The pipe name({}) is not support)".format(core_type_input))
            return [pipe_name_list[0], pipe_name_list[1] + "-" + pipe_name_list[2]]
        self.core_type = parse_core_type(self.pipe_name)[0]
        pipe_name = parse_core_type(self.pipe_name)[1]
        pipe_id = pipes.get(pipe_name, None)
        if pipe_id is None:
            raise Exception(
                "Unsupport event(The pipe({}) is not support)".format(pipe_name))
        self.pipe_id = pipe_id

    def gen_args(self):
        args_map = {"Cycle": self.dur}
        args_map["Cycle"] = SimdVf.update_metrics_cycle_with_task_name(self.task_name, args_map["Cycle"])
        if "FLAG" in self.task_name:
            args_map["Task Type"] = self.task_name
            args_map["Detail"] = self.pipe_type
            return args_map
        if self.pipe_type == "MOV":
            size_gbyte = self.size / 1024 / 1024 / 1024
            bandwidth_gbyte_per_second = 0 if arch.cal_duration(self.dur) == 0 else \
                (size_gbyte / arch.cal_duration(self.dur) * 1000000)
            args_map["Size(B)"] = self.size
            args_map["Bandwidth(GB/s)"] = round(bandwidth_gbyte_per_second, 2)
        else:
            args_map["Task Type"] = "AI_CORE"
            args_map["Ops"] = self.size
            args_map["Ops/Cycle"] = 0 if (self.dur == 0) else (self.size / self.dur)
        return args_map


@Singleton
class Trace:
    time_unit = "ns"  # only ms or ns

    def __init__(self):
        self.is_enable = False
        self.context_before = []
        self.context_after = []
        self.pipe_end_time = defaultdict(lambda: 0)
        self.pipe_vec = defaultdict(lambda: [None, None])  # store pipe_vec begin and end time stamp

    def trace_clear(self):
        self.__init__()

    def set_enable(self, enable):
        self.is_enable = enable

    def add_event(self, trace_event):
        if trace_event.task_name in ["SET_FLAG", "WAIT_FLAG"]:
            if trace_event.pipe_id == 10 or trace_event.pipe_id == 15:
                return
        index = 0
        if len(core_type_list) != 0:
            index = core_type_list.index(trace_event.core_type)
        ts = trace_event.start_time
        dur = trace_event.dur
        ts, dur = self._update_sync_event_dur(trace_event, ts, dur)
        event = {
            "pid": index,
            "ph": "X",
            "ts": arch.cal_duration(ts),  # 开始时间是pipe内上一个任务的结束时间
            "dur": arch.cal_duration(dur),
            "tid": trace_event.pipe_id,
            "id": trace_event.event_id,
            "name": trace_event.task_name,
            "args": trace_event.args
        }
        self.context_after.append(event)

    def dump(self, output_dir):
        self._add_pipe_vec()
        self._add_head()
        self.context_after = self.context_before + self.context_after
        trace_file = os.path.join(output_dir, "trace.json")
        if checker.check_path_exists(trace_file):
            raise Exception("The file {} already exists, cannot generate, please remove it first".format(trace_file))
        trace_obj = {
            "displayTimeUnit": self.time_unit,
            "traceEvents": self.context_after
        }
        with os.fdopen(os.open(trace_file, OPEN_FLAGS, SAVE_DATA_FILE_AUTHORITY), 'w') as f:
            data = json.dumps(trace_obj)
            f.truncate()
            f.write(data)
            logger.info("The trace is save at {}".format(trace_file))
        self.trace_clear()

    def gen_head(self, base_args, core_type_index):
        p_head = {
            "args": {"name": base_args},
            "name": "process_name",
            "ph": "M",
            "pid": core_type_index
        }
        self.context_before.append(p_head)
        for name, tid in pipes.items():
            t_head = {
                "args": {"name": name},
                "name": "thread_name",
                "ph": "M",
                "pid": core_type_index,
                "tid": tid
            }
            self.context_before.append(t_head)

    def _update_sync_event_dur(self, trace_event, ts, dur):
        if trace_event.task_name == "WAIT_FLAG":
            ts = self.pipe_end_time[trace_event.pipe_name]
            end_time = trace_event.start_time
            dur = end_time - ts + 1
        self.pipe_end_time[trace_event.pipe_name] = (dur + ts)
        if trace_event.task_name == "SET_FLAG" or (trace_event.task_name == "WAIT_FLAG" and dur == 1):
            dur = 2  # dur set 2 is for trace display.
        return ts, dur

    def _add_head(self):
        if len(core_type_list) == 0:
            core_type_list.append("")  # 添加空串保证for循环至少可以进入一次
        base_args = "kernel perf prediction"
        for index, core_type in enumerate(core_type_list):
            base_args = base_args if (core_type == "") else core_type
            self.gen_head(base_args, index)
            base_args = ""
        core_type_list.clear()  # 生成trace.json前清空，避免老的Chip信息影响下一次的with Chip()

    def _add_pipe_vec(self):
        def add_pipe_vec_wait(wait_begin_time, begin_time, pid_index, event_pid):
            ts = wait_begin_time
            dur = begin_time - ts
            if dur <= 0:
                return
            # add wait event before pipe vec
            event = {
                "pid": pid_index,
                "ph": "X",
                "ts": arch.cal_duration(ts),  # 开始时间是pipe内上一个任务的结束时间
                "dur": arch.cal_duration(dur),
                "tid": 7,
                "id": event_pid,
                "name": "WAIT_FLAG",
            }
            self.context_after.append(event)
        wait_begin = 0
        event_id = 0  # split diff scope pipe vec
        for scope in self.pipe_vec:
            if None in self.pipe_vec[scope]:
                continue
            begin = min(self.pipe_vec[scope])
            end = max(self.pipe_vec[scope])
            index = 0  # allow pipe vec display in self core
            if len(core_type_list) != 0 and '-' in scope:  # eg: scope is aiv0-SIMT0
                index = core_type_list.index(scope.split('-')[0])
            event_all_b = {
                "name": "PIPE-VEC",
                "ph": "B",
                "cat": "vec",
                "id": event_id,
                "pid": index,
                "tid": 7,
                "ts": arch.cal_duration(begin)
            }
            event_all_e = {
                "name": "PIPE-VEC",
                "ph": "E",
                "cat": "vec",
                "id": event_id,
                "pid": index,
                "tid": 7,
                "ts": arch.cal_duration(end)
            }
            event_id += 1
            add_pipe_vec_wait(wait_begin, begin, index, event_id)
            wait_begin = end
            self.context_after.append(event_all_b)
            self.context_after.append(event_all_e)
