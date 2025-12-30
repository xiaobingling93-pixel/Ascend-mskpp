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
from mskpp import vcgadd, vcgmin, vcmin, vcmp, vcmpv, vcmpvs, vcopy, vcpadd, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_16_TYPE = "FP16"
FP_32_TYPE = "FP32"
INT_16_TYPE = "INT16"
FORMAT_TYPE = "ND"


def my_vcgadd(gm_x, reduce_num):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcgadd(ub_x, ub_y, reduce_num)()
    z = out[0]
    return z


def my_vcgmin(gm_x, reduce_num):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcgmin(ub_x, ub_y, reduce_num)()
    z = out[0]
    return z


def my_vcmin(gm_x, reduce_num):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcmin(ub_x, ub_y, reduce_num)()
    z = out[0]
    return z


def my_vcmp(gm_x):
    ub_x, ub_y = Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcmp(ub_x, ub_y)()
    return out[0]


def my_vcmpv(gm_x, gm_y):
    ub_x, ub_y, ub_z = Tensor(UB_MEM), Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vcmpv(ub_x, ub_y, ub_z)()
    return out[0]


def my_vcmpvs(gm_x):
    ub_x, ub_y = Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcmpvs(ub_x, 1, ub_y)()
    return out[0]


def my_vcopy(gm_x):
    ub_x, ub_y = Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcopy(ub_x, ub_y)()
    return out[0]


def my_vcpadd(gm_x, reduce_num):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcpadd(ub_x, ub_y, reduce_num)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vcgadd_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcgadd(in_x_f16, 64)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcgmin_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcgmin(in_x_f16, 64)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcmin_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcmin(in_x_f16, 64)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcmp_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcmp(in_x_f16)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcmpv_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcmpv(in_x_f16, in_y_f16)
            in_z_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcmpvs_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcmpvs(in_x_f16)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcopy_int16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcopy(in_x_f16)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcpadd_fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vcpadd(in_x_f16, 2)
            in_y_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()