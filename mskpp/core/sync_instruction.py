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

from .instruction_base import InstructionBase
from .trace import pipes
from .common import checker
from .chip import sync_instr_dict, event_id_dict
from .aicore import Core


class SyncInstruction(InstructionBase):
    def __init__(self, task_name, pipe_src, pipe_dst, flag, event_id, src_core, dst_core):
        SyncInstruction.init_param_check(task_name, pipe_src, pipe_dst, flag, event_id)
        instr_name = self.gen_instr_name(pipe_src, pipe_dst, event_id, src_core, dst_core)
        sync_instr_dict[task_name].append(instr_name)
        super(SyncInstruction, self).__init__(instr_name, pipe_src, pipe_dst)
        self.task_name = task_name  # 当这个指令任务执行时，使用task_name
        self.pipe_src = pipe_src
        self.pipe_dst = pipe_dst
        self.keys = self.gen_keys(pipe_src, pipe_dst, event_id, src_core, dst_core)
        event_id_dict[self.keys] = None
        self.event_id = event_id
        self.pipe_type = self.pipe_src if flag is True else self.pipe_dst
        self.scope_name_with_core = None

    @classmethod
    def gen_instr_name(cls, pipe_src, pipe_dst, event_id, src_core, dst_core):
        def get_pipe_name(pipe_ori_name):
            if "PIPE" in pipe_ori_name:
                return pipe_ori_name[5:]
            else:
                return pipe_ori_name
        if src_core is None:
            instr_name = "PIPE:{},TRIGGERPIPE:{},FLAGID:{}".format(get_pipe_name(pipe_src),
                                                                   get_pipe_name(pipe_dst), event_id)
            instr_name = instr_name if (Core.get_core_type() is None) else ("{}:".format(Core.get_core_type()) +
                                                                            instr_name)
        else:
            instr_name = "PIPE:{}_{},TRIGGERPIPE:{}_{},FLAGID:{}".format(src_core, get_pipe_name(pipe_src),
                                                                         dst_core, get_pipe_name(pipe_dst), event_id)
        return instr_name

    @classmethod
    def gen_keys(cls, pipe_src, pipe_dst, event_id, src_core, dst_core):
        if src_core is None:
            keys = pipe_src + "_TO_" + pipe_dst + "_" + str(event_id)
            keys = keys if (Core.get_core_type() is None) else "{}:".format(Core.get_core_type()) + keys
        else:
            keys = src_core + "_" + pipe_src + "_TO_" + dst_core + "_" + pipe_dst + "_" + str(event_id)
        return keys

    @classmethod
    def init_param_check(cls, task_name, pipe_src, pipe_dst, flag, event_id):
        if task_name not in ["SET_FLAG", "WAIT_FLAG"]:
            raise Exception("Parameter task_name is invalid, should be SET_FLAG or WAIT_FLAG")
        if pipe_src not in pipes.keys() or pipe_dst not in pipes.keys():
            raise Exception("Parameter pipe is invalid, should be {}".format(pipes.keys()))
        if not checker.is_required_type(flag, bool):
            raise Exception("flag should be bool, but got {}".format(type(flag)))
        if not checker.is_int_type(event_id):
            raise Exception("event_id should be int, but got {}".format(type(event_id)))
        if event_id < 0 or event_id > 65535:
            raise Exception("event_id should be in range [0, 65535]")

    def instr_check(self, inputs, outputs, attr):
        pass

    def is_ready(self):
        # is_ready用于判断当前任务是够可执行，如果是wait_flag，那么应该被阻塞；如果是set_flag，那么应该可执行
        if self.task_name == "WAIT_FLAG":
            if event_id_dict[self.keys] != self.event_id:
                return False
        return True

    def schedule_post(self):
        # 对于set指令结束之后，设置对应的event_id，让wait_flag感知到
        if self.task_name == "SET_FLAG":
            event_id_dict[self.keys] = self.event_id

    def cal_size(self):
        return 0

    def cost_time(self):
        return 1  # 对于wait来说，耗时是阻塞时长；对于set来说，耗时是1，仅做显示使用

    def launch(self, inputs, outputs, attr):
        from mskpp.core.instr_task import InstrTask
        from mskpp._C import task_schedule
        pipe_name = self.pipe_type
        if Core.core_type is not None:
            pipe_name = Core.core_type + "-" + self.pipe_type
        task = InstrTask(pipe_name, self, self.event_id)
        task_schedule.Schedule().add_task(task)


def core_decomposition(pipe_src, pipe_dst):
    if "PIPE-VEC" in pipe_src:
        pipe_src = pipe_src.replace("PIPE-VEC", "RVECST")
    if "PIPE-VEC" in pipe_dst:
        pipe_dst = pipe_dst.replace("PIPE-VEC", "RVECLD0")

    def decomposition(pipe_name):
        if '_' not in pipe_name:
            return None, pipe_name
        pipe_list = pipe_name.split('_')
        if len(pipe_list) != 2:
            return None, pipe_name
        checker.check_name_valid(pipe_list[0])
        return pipe_list[0], pipe_list[1]
    src_core, src_pipe = decomposition(pipe_src)
    dst_core, dst_pipe = decomposition(pipe_dst)
    if not isinstance(src_core, type(dst_core)):
        raise Exception("pipe_src should have same format with pipe_dst")
    return src_core, src_pipe, dst_core, dst_pipe


def set_flag(pipe_src, pipe_dst, event_id):
    src_core, src_pipe, dst_core, dst_pipe = core_decomposition(pipe_src, pipe_dst)
    # pipe_src完成调度后，pipe_dst解除阻塞
    set_flag_instr = SyncInstruction("SET_FLAG", src_pipe, dst_pipe, True, event_id, src_core, dst_core)
    set_flag_instr()


def wait_flag(pipe_src, pipe_dst, event_id):
    src_core, src_pipe, dst_core, dst_pipe = core_decomposition(pipe_src, pipe_dst)
    # pipe_dst等待pipe_src完成后调度
    wait_flag_instr = SyncInstruction("WAIT_FLAG", src_pipe, dst_pipe, False, event_id, src_core, dst_core)
    wait_flag_instr()
