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
from mskpp import vabs, vaddreluconv, vaddrelu, vand, vaxpy, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase


UB_MEM = "UB"
GM_MEM = "GM"
INT_8_TYPE = "INT8"
FP_16_TYPE = "FP16"
FP_32_TYPE = "FP32"
INT_16_TYPE = "INT16"
FORMAT_TYPE = "ND"


def my_vabs(gm_x):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vabs(ub_x, ub_y)()
    z = out[0]
    return z


def my_vaddreluconv(gm_x, gm_y):
    ub_x, ub_y, ub_z = Tensor(UB_MEM), Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vaddreluconv(ub_x, ub_y, ub_z)()
    return out[0]


def my_vaddrelu(gm_x, gm_y):
    ub_x, ub_y, ub_z = Tensor(UB_MEM), Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vaddrelu(ub_x, ub_y, ub_z)()
    return out[0]


def my_vand(gm_x, gm_y):
    ub_x, ub_y, ub_z = Tensor(UB_MEM), Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vand(ub_x, ub_y, ub_z)()
    return out[0]


def my_vaxpy_mix(gm_x, gm_y):
    ub_x, ub_y, ub_z = Tensor(UB_MEM), Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vaxpy(ub_x, ub_y, ub_z, if_mix=True)()
    return out[0]


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vabs_fp16_fp32_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_x_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vabs(in_x_f16)
            out_y2 = my_vabs(in_x_f32)
            in_y_f16.load(out_y1)
            in_y_f32.load(out_y2)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vaddreluconv_fp322fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vaddreluconv(in_x_f32, in_y_f32)
            in_z_f16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vaddreluconv_s162s8_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_s8 = Tensor(GM_MEM, INT_8_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vaddreluconv(in_x_s16, in_y_s16)
            in_z_s8.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vaddreluconv_f162s8_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_s8 = Tensor(GM_MEM, INT_8_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vaddreluconv(in_x_f16, in_y_f16)
            in_z_s8.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vaddrelu_fp16_fp32_s16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_x_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_x_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vaddrelu(in_x_f16, in_y_f16)
            out_y2 = my_vaddrelu(in_x_f32, in_y_f32)
            out_y3 = my_vaddrelu(in_x_s16, in_y_s16)
            in_z_f16.load(out_y1)
            in_z_f32.load(out_y2)
            in_z_s16.load(out_y3)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vand_s16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_s16 = Tensor(GM_MEM, INT_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vand(in_x_s16, in_y_s16)
            in_z_s16.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vaxpy_mix_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_f16 = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_z_f32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            out_y1 = my_vaxpy_mix(in_x_f16, in_y_f16)
            in_z_f32.load(out_y1)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
