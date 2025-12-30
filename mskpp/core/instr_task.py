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

import sys
from abc import ABC, abstractmethod
from .metric import Metrics
from .trace import Trace, TraceEvent
from .vec_scope import SimdVf


class RawTask(ABC):
    '''
    裸事件信息，主要用于承载调度内容信息
    '''
    def __init__(self, pipe_name, name):
        '''
        :param pipe_name: 对应的管道
        :param name:
        '''
        self.name = name
        self.owner = pipe_name

    def __str__(self):
        return "Task({} - {})".format(self.owner, self.name)

    @abstractmethod
    def cost_time(self):
        raise NotImplementedError("this function(cost_time) need to impl.")

    @abstractmethod
    def is_ready(self):
        '''
        检查任务的依赖是否已经ok
        :return:
        '''
        raise NotImplementedError("this function(is_ready) need to impl.")

    @abstractmethod
    def pre_func(self):
        raise NotImplementedError("this function(pre_func) need to impl.")

    @abstractmethod
    def post_func(self):
        raise NotImplementedError("this function(post_func) need to impl.")


class InstrTask(RawTask):
    bar_index = 0  # 指令调度进度条计数，每调度一条指令+1
    '''
    该类继承了task schedule模块中的标准类接口，需要实现指令到标准任务的转换
    '''
    def __init__(self, pipe_name, instr_obj, event_id=-1):
        '''
        :param pipe_name:  标准资源名
        :param name:       指令名称
        '''
        self.task_check(pipe_name, instr_obj)
        super(InstrTask, self).__init__(pipe_name, instr_obj.name)
        self.name = instr_obj.task_name   # eg:MOV-GM_TO_UB
        self.owner = pipe_name            # eg:aic0-PIPE-MTE1
        self.instr_obj = instr_obj
        self.start_time = 0
        self.end_time = 0
        self.event_id = event_id

    @staticmethod
    def task_check(pipe_name, instr_obj):
        if pipe_name is None:
            raise Exception("task pipe name is None.")
        if instr_obj is None:
            raise Exception("instr obj task is None.")

    def cost_time(self):
        return self.instr_obj.cost_time()
    
    def size(self):
        if self.instr_obj.name == "MOV":
            return self.instr_obj.move_size()
        return self.instr_obj.cal_size()

    def is_ready(self):
        return self.instr_obj.is_ready()

    def pre_func(self):
        pass

    def post_func(self):
        from mskpp._C import task_schedule
        if not task_schedule.Schedule().get_debug_mode() and self.start_time == self.end_time:
            raise Exception("Pipe %s instruction %s do not run at %s",
                            self.owner, self.name, self.start_time)
        if Trace().is_enable:
            trace_event = TraceEvent(self.instr_obj.name, self.owner, self.name, self.start_time, self.end_time,
                                     self.size(), self.event_id)
            Trace().add_event(trace_event)
        if Metrics().is_enable and (self.name not in ["SET_FLAG", "WAIT_FLAG"]):
            Metrics().add_event(self)
        self.instr_obj.schedule_post()
        if self.instr_obj.scope_name_with_core is not None:
            Trace().pipe_vec[self.instr_obj.scope_name_with_core] = (
                SimdVf.update_vec_scope(Trace().pipe_vec[self.instr_obj.scope_name_with_core], self.start_time,
                                        self.end_time))
        if self.instr_obj.instr_num == 0:
            return
        stream = sys.stdout
        # 计算进度百分比
        progress = (InstrTask.bar_index + 1) / self.instr_obj.instr_num
        bar_length = 100  # 进度条长度（字符数）100
        filled = int(bar_length * progress)
        bar = '█' * filled + '-' * (bar_length - filled)
        InstrTask.bar_index += 1
        stream.write(f'\r[{bar}] {progress:.0%}')
        stream.flush()  # 强制刷新输出缓冲区
        if InstrTask.bar_index == self.instr_obj.instr_num:
            stream.write("\n")
