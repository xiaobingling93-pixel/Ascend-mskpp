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

from mskpp import mmad, Tensor, Chip, Core, vadd, set_flag, wait_flag, VecScope, rv_vadd


def my_vadd(src0, src1, dst, k):
    # 向量Add的基本数据通路：
    # 被加数x：GM-UB
    # 加数y：GM-UB
    # 结果向量z： UB-GM

    # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
    set_flag("PIPE-MTE2", "PIPE-VEC", k+1)
    wait_flag("PIPE-MTE2", "PIPE-VEC", k+1)
    with VecScope("SIMD" + str(k)) as vec_scope:
        repeat = int(32768 / (32 * 48))
        for _ in range(repeat):
            vreg0 = Tensor("VEC", "FP32")
            vreg1 = Tensor("VEC", "FP32")
            vreg2 = Tensor("VEC", "FP32")
            vreg0.load(src0)
            vreg1.load(src1)
            rv_vadd(vreg0, vreg1, vreg2)()
            dst.load(vreg2)
    set_flag("PIPE-VEC", "PIPE-MTE3", k+2)
    wait_flag("PIPE-VEC", "PIPE-MTE3", k+2)
    # 将UB上的数据移动到GM变量gm_z的地址空间上
    return dst


def sync_in_diff_core(loops):
    with Core("aic0") as aic0:
        # GM->L1->L0B
        l1_x = Tensor("L1")
        l1_x.load(gm_x)
        x = Tensor("L0A")
        wait_flag("PIPE-MTE2", "PIPE-MTE1", 200 + loops)
        x.load(l1_x)
        # GM->L1->L0B
        l1_y = Tensor("L1")
        l1_y.load(gm_y)
        y = Tensor("L0B")  # L0B
        y.load(l1_y)
        set_flag("PIPE-MTE2", "PIPE-MTE1", 200 + loops)
        # L0C
        b = Tensor("L0C", "FP32", [128, 512], format="NC1HWC0")
        # mmad
        out = mmad(x, y, b, True)()
        gm_out.load(out[0])
        set_flag("aic0_PIPE-FIX", "aiv0_PIPE-MTE2", 100 + loops)
    with Core("aiv0") as aiv0:
        # 定义和分配UB上的变量
        x = Tensor("UB")
        y = Tensor("UB")
        z = Tensor("UB")

        # 将GM上的数据移动到UB对应内存空间上
        wait_flag("aic0_PIPE-FIX", "aiv0_PIPE-MTE2", 100 + loops)
        x.load(gm_z)
        y.load(gm_out)

        # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
        vec_out = my_vadd(x, y, z, loops)

        # 将UB上的数据移动到GM变量gm_z的地址空间上
        gm_vec.load(vec_out)


if __name__ == '__main__':
    with Chip("Ascend910_95") as chip:
        chip.enable_trace()
        chip.enable_metrics()
        chip.disable_instr_log()
        gm_x = Tensor("GM", "FP16", [128, 256], format="ND")
        gm_y = Tensor("GM", "FP16", [256, 512], format="ND")
        gm_out = Tensor("GM")
        gm_z = Tensor("GM", "FP32", [128, 512], format="NC1HWC0")
        gm_vec = Tensor("GM")
        for j in range(5):
            sync_in_diff_core(j)
