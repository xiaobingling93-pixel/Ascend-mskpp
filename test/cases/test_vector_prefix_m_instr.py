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
import unittest
from mskpp import Tensor, Chip, vmaddrelu, vmla
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_16_TYPE = "FP16"
FP_32_TYPE = "FP32"
FORMAT_TYPE = "ND"


def my_vmaddrelu(gm_x, gm_y, gm_z):
    x = Tensor(UB_MEM)
    y = Tensor(UB_MEM)
    z = Tensor(UB_MEM)
    # 将GM上的数据移动到UB对应内存空间上
    x.load(gm_x)
    y.load(gm_y)
    # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
    out = vmaddrelu(x, y, z)()
    # 将UB上的数据移动到GM变量gm_z的地址空间上
    gm_z.load(out[0])


def my_vmla(gm_x, gm_y, gm_z, if_mix=False):
    x = Tensor(UB_MEM)
    y = Tensor(UB_MEM)
    z = Tensor(UB_MEM)
    # 将GM上的数据移动到UB对应内存空间上
    x.load(gm_x)
    y.load(gm_y)
    # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
    out = vmla(x, y, z, if_mix)()
    # 将UB上的数据移动到GM变量gm_z的地址空间上
    gm_z.load(out[0])


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vmaddrelu_fp32_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_fp16 = Tensor(GM_MEM, FP_16_TYPE, [64, 128], format=FORMAT_TYPE)
            in_y_fp16 = Tensor(GM_MEM, FP_16_TYPE, [64, 128], format=FORMAT_TYPE)
            in_z_fp16 = Tensor(GM_MEM, FP_16_TYPE, [64, 128], format=FORMAT_TYPE)
            in_x_fp32 = Tensor(GM_MEM, FP_32_TYPE, [64, 128], format=FORMAT_TYPE)
            in_y_fp32 = Tensor(GM_MEM, FP_32_TYPE, [64, 128], format=FORMAT_TYPE)
            in_z_fp32 = Tensor(GM_MEM, FP_32_TYPE, [64, 128], format=FORMAT_TYPE)
            my_vmaddrelu(in_x_fp16, in_y_fp16, in_z_fp16)
            my_vmaddrelu(in_x_fp32, in_y_fp32, in_z_fp32)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vmla_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_fp16 = Tensor(GM_MEM, FP_16_TYPE, [64, 128], format=FORMAT_TYPE)
            in_y_fp16 = Tensor(GM_MEM, FP_16_TYPE, [64, 128], format=FORMAT_TYPE)
            in_x_fp32 = Tensor(GM_MEM, FP_32_TYPE, [64, 128], format=FORMAT_TYPE)
            in_y_fp32 = Tensor(GM_MEM, FP_32_TYPE, [64, 128], format=FORMAT_TYPE)
            in_z_fp16 = Tensor(GM_MEM, FP_16_TYPE, [64, 128], format=FORMAT_TYPE)
            in_z_fp32 = Tensor(GM_MEM, FP_32_TYPE, [64, 128], format=FORMAT_TYPE)
            my_vmla(in_x_fp32, in_y_fp32, in_z_fp32)
            my_vmla(in_x_fp16, in_y_fp16, in_z_fp16)
            my_vmla(in_x_fp16, in_y_fp16, in_z_fp32, True)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()