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
from mskpp import Tensor, Chip, vreducev2, vreduce
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_32_TYPE = "FP32"
UINT_32_TYPE = "UINT32"
FORMAT_TYPE = "ND"


def my_vreducev2(gm_x, gm_y, gm_z, reserve_num):
    x = Tensor(UB_MEM)
    y = Tensor(UB_MEM)
    z = Tensor(UB_MEM)
    # 将GM上的数据移动到UB对应内存空间上
    x.load(gm_x)
    y.load(gm_y)
    # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
    out = vreducev2(x, y, z, reserve_num)()
    # 将UB上的数据移动到GM变量gm_z的地址空间上
    gm_z.load(out[0])
    return out[0]


def my_vreduce(gm_x, gm_y, gm_z, reserve_num):
    x = Tensor(UB_MEM)
    y = Tensor(UB_MEM)
    z = Tensor(UB_MEM)
    # 将GM上的数据移动到UB对应内存空间上
    x.load(gm_x)
    y.load(gm_y)
    # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
    out = vreduce(x, y, z, reserve_num)()
    # 将UB上的数据移动到GM变量gm_z的地址空间上
    gm_z.load(out[0])
    return out[0]


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vreducev2_uint32_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor(GM_MEM, UINT_32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_y = Tensor(GM_MEM, UINT_32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_z = Tensor(GM_MEM, UINT_32_TYPE, [32, 64], format=FORMAT_TYPE)
            out = my_vreducev2(in_x, in_y, in_z, 24)
            self.assertEqual(out.size[0], 24)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vreduce_uint32_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor(GM_MEM, UINT_32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_y = Tensor(GM_MEM, UINT_32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_z = Tensor(GM_MEM, UINT_32_TYPE, [32, 64], format=FORMAT_TYPE)
            out = my_vreduce(in_x, in_y, in_z, 48)
            self.assertEqual(out.size[0], 48)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()