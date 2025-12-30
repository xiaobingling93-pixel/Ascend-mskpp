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

from mskpp import rv_vadd, Tensor, Chip, VecScope, set_flag, wait_flag, Core


def my_vadd(gm_x, gm_y, gm_z, k):
    # 向量Add的基本数据通路：
    # 被加数x：GM-UB
    # 加数y：GM-UB
    # 结果向量z： UB-GM

    # 定义和分配UB上的变量
    src0 = Tensor("UB")
    src1 = Tensor("UB")
    dst = Tensor("UB")

    # 将GM上的数据移动到UB对应内存空间上
    src0.load(gm_x)
    src1.load(gm_y)

    # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
    set_flag("PIPE-MTE2", "PIPE-VEC", k+1)
    wait_flag("PIPE-MTE2", "PIPE-VEC", k+1)
    with VecScope("SIMD" + str(k)) as vec_scope:
        repeat = int(32768 / (32 * 48))
        for _ in range(repeat):
            vreg0 = Tensor("VEC", "FP16", [32, 48])
            vreg1 = Tensor("VEC", "FP16", [32, 48])
            vreg2 = Tensor("VEC", "FP16", [32, 48])
            vreg0.load(src0)
            vreg1.load(src1)
            rv_vadd(vreg0, vreg1, vreg2)()
            dst.load(vreg2)
    set_flag("PIPE-VEC", "PIPE-MTE3", k+2)
    wait_flag("PIPE-VEC", "PIPE-MTE3", k+2)
    # 将UB上的数据移动到GM变量gm_z的地址空间上
    gm_z.load(dst)


if __name__ == '__main__':
    with Chip("Ascend910_95") as chip:
        chip.enable_trace()
        chip.enable_metrics()
        # for j in range(5):
        # 应用算子进行AICORE计算
        in_x = Tensor("GM", "FP16", [32, 48], format="ND")
        in_y = Tensor("GM", "FP16", [32, 48], format="ND")
        in_z = Tensor("GM", "FP16", [32, 48], format="ND")
        with Core("aiv0") as aiv0:
            my_vadd(in_x, in_y, in_z, 0)
