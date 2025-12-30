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

import unittest
import json
import os
from mskpp import mmad, Tensor, Chip, Core, vadd, vadds, vsub, vexp, vmul, vmuls, set_flag, wait_flag
from mskpp._C import task_schedule
from test.utils.test_base import TestBase
import math

FORMAT_TYPE_ND = "ND"
FORMAT_TYPE_NZ = "NZ"
FORMAT_TYPE_NC1HWC0 = "NC1HWC0"

seq_split_out = 64
seq_split_in = 256
batch_size, head_num, seq_size, head_dim = 1, 1, 2048, 127
scale_value = 1 / 128
keep_prob = 1.0


def fa_forward_vec_part(gm_temp, gm_atten_mask_split, gm_softmax_log_max_sum_split, shape_info):
    m, n = shape_info
    ub_bmm1_res_loop = Tensor("UB", "FP16", [m, n], format=FORMAT_TYPE_NZ)

    ub_bmm1_res_loop.load(gm_temp, expect_value=1)
    vadds(ub_bmm1_res_loop, scale_value, ub_bmm1_res_loop)()

    ub_atten_mask_loop = Tensor("UB", "FP16", [m, n], format=FORMAT_TYPE_NZ)  # [64, 256]

    ub_atten_mask_loop.load(gm_atten_mask_split)  # [64, 256]
    vadds(ub_atten_mask_loop, -10000, ub_atten_mask_loop)()
    vadd(ub_bmm1_res_loop, ub_atten_mask_loop, ub_bmm1_res_loop)()
    ub_softmax_log_max_sum_loop = Tensor("UB", "FP16", [m, 1], format=FORMAT_TYPE_NZ)  # [64, 1]

    ub_softmax_log_max_sum_loop.load(gm_softmax_log_max_sum_split)  # [64, 1]
    vsub(ub_bmm1_res_loop, ub_softmax_log_max_sum_loop, ub_bmm1_res_loop)()

    ub_bmm1_res_loop_last = Tensor("UB", "FP16", [m, n], format=FORMAT_TYPE_NZ)
    # gm_temp初始化为invalid，gm_temp完成后生成一个值，会通知ub_bmm1_res_loop_last是否为等待值，如果是就设置为就绪状态
    # 这里可以将gm_temp
    vexp(ub_bmm1_res_loop, ub_bmm1_res_loop_last)()
    return ub_bmm1_res_loop_last


def softmax_out_grad_vec_part(gm_temp2, gm_softmax_out_sum_split, ub_bmm1_res_loop_last, shape_info, index):
    """
    这是一个对UB和VEC的行为的包裹，其输入是GM，可以看做一个小型计算核
    """
    m, n = shape_info
    ub_softmax_out_drop_grad_loop = Tensor("UB", "FP16", [m, n], format=FORMAT_TYPE_NZ)
    wait_flag("PIPE-MTE3", "PIPE-MTE2", index)
    ub_softmax_out_drop_grad_loop.load(gm_temp2, expect_value=2)  # [64, 256]
    ub_softmax_out_sum_loop = Tensor("UB", "FP16", [m, 1], format=FORMAT_TYPE_NZ)  # [64, 1]
    ub_softmax_out_sum_loop.load(gm_softmax_out_sum_split)  # [64, 1]
    vsub(ub_softmax_out_drop_grad_loop, ub_softmax_out_sum_loop, ub_softmax_out_drop_grad_loop)()
    vmul(ub_softmax_out_drop_grad_loop, ub_bmm1_res_loop_last, ub_softmax_out_drop_grad_loop)()
    ub_softmax_out_drop_grad_loop_last = Tensor("UB", "FP16", [m, n], format=FORMAT_TYPE_NZ)
    vmuls(ub_softmax_out_drop_grad_loop, scale_value, ub_softmax_out_drop_grad_loop_last)()
    gm_temp2.load(ub_softmax_out_drop_grad_loop_last, set_value=4)
    return gm_temp2


def batch_dot(out, a, b, shape_info, tensor_value):
    """
    这其实是一个对L0,MMAD的行为包裹，其输入是L1的内容，可以作为一个小型计算核
    """
    m, k, n = shape_info
    l0a_n = Tensor("L0A", "FP16", [m, k], format=FORMAT_TYPE_NZ)  # [64, 256]
    l0b_n = Tensor("L0B", "FP16", [k, n], format=FORMAT_TYPE_NZ)  # [256, 128]
    l0c_n = Tensor("L0C", "FP16", [m, n], format=FORMAT_TYPE_NZ)  # [64, 128]
    l0a_n.load(a)
    l0b_n.load(b)
    mmad_out = mmad(l0a_n, l0b_n, l0c_n, True)()
    out.load(mmad_out[0], set_value=tensor_value)
    # 是在这一次的调度时，需要标记一个值
    # 某块内存在被某次调度时，设置特定的值
    # out调度时，将任务id传入，标识是这一次的任务执行
    # out自己也记录这一次的任务ID和需要写入的值
    # 这里out计算完成后，需要将自己的值设置为一个数(不需要给所有在等待的tensor发消息，因为通过调度系统确保刚好调度到依赖项目)
    return out


def flash_attention_grad(gm_q, gm_k, gm_v, gm_atten_mask, gm_attention_out_grad, gm_softmax_out_sum,
                         gm_softmax_log_max_sum, gm_q_grad, gm_k_grad, gm_v_grad):
    seq_out_loop_times = seq_size // seq_split_out  # 2048 // 64 = 32
    seq_in_loop_times = seq_size // seq_split_in    # 2048 // 256 = 8
    index = 0

    for batch_index in range(batch_size):
        for head_index in range(head_num):
            for seq_out_index in range(seq_out_loop_times):
                seq_out_start_index = seq_out_index * seq_split_out
                seq_out_end_index = seq_out_start_index + seq_split_out
                for seq_in_index in range(seq_in_loop_times):
                    seq_in_start_index = seq_in_index * seq_split_in
                    seq_in_end_index = seq_in_start_index + seq_split_in
                    '''对一次处理的内存切块，满足L1或者UB的要求，此处不属于Core的范围，所以处理GM的内存。'''
                    gm_q_split = gm_q[batch_index, head_index, seq_out_start_index:seq_out_end_index, :]
                    gm_attention_out_grad_split = gm_attention_out_grad[batch_index, head_index,
                                                                        seq_out_start_index:seq_out_end_index, :]
                    gm_k_split = gm_k[batch_index, head_index, seq_in_start_index:seq_in_end_index, :]
                    gm_v_split = gm_v[batch_index, head_index, seq_in_start_index:seq_in_end_index, :]
                    gm_atten_mask_split = gm_atten_mask[seq_out_start_index:seq_out_end_index,
                                                        seq_in_start_index:seq_in_end_index]
                    gm_softmax_log_max_sum_split = gm_softmax_log_max_sum[batch_index, head_index,
                                                                          seq_out_start_index:seq_out_end_index]
                    gm_softmax_out_sum_split = gm_softmax_out_sum[batch_index, head_index,
                                                                  seq_out_start_index:seq_out_end_index]

                    '''对于需要用于核间同步的GM内存最好单独管理，在这个作用域创建，保证不同循环间的gm是不一样的，这样相互不影响'''
                    gm_temp = Tensor("GM", "FP16", [seq_split_out, seq_split_in], format=FORMAT_TYPE_NZ)
                    gm_temp2 = Tensor("GM", "FP16", [seq_split_out, seq_split_in], format=FORMAT_TYPE_NZ)

                    with Core("AIC1") as aic:
                        '''在这个作用域下，仅处理：
                          1. L1的创建和对(CUBE，L0)联合对象函数的处理，L1的新建请尽量靠近计算本身，减少理解难度
                          2. 与AIV的同步
                        '''

                        # task 1.1： 前向计算 AIC 部分
                        l1_q_loop = Tensor("L1", "FP16", [seq_split_out, head_dim], format=FORMAT_TYPE_NZ)  # [64, 128]
                        l1_k_loop = Tensor("L1", "FP16", [seq_split_in, head_dim], format=FORMAT_TYPE_NZ)  # [256, 128]
                        l1_q_loop.load(gm_q_split)  # [64, 128]
                        l1_k_loop.load(gm_k_split)  # [256, 128]
                        gm_temp = batch_dot(gm_temp, l1_q_loop, l1_k_loop, (seq_split_out, head_dim, seq_split_in), 1)

                        # task 2.1: softmax_out_grad计算 AIC 部分
                        l1_v_loop = Tensor("L1", "FP16", [seq_split_in, head_dim], format=FORMAT_TYPE_NZ)  # [256, 128]
                        l1_attention_out_loop = Tensor("L1", "FP16", [seq_split_out, head_dim], format=FORMAT_TYPE_NZ)
                        l1_v_loop.load(gm_v_split)  # [256, 128]
                        l1_attention_out_loop.load(gm_attention_out_grad_split)  # [64, 128]
                        gm_temp2 = batch_dot(gm_temp2, l1_attention_out_loop, l1_v_loop, (seq_split_out, head_dim,
                                                                                          seq_split_in), 2)
                        # 这里会第一次写入gm_temp2，写入后立即触发task2.2
                        
                        # task 3：反向计算 AIC, 依赖task2.2
                        l1_softmax_out_loop = Tensor("L1", "FP16", [seq_split_out, seq_split_in], format=FORMAT_TYPE_NZ)
                        l1_softmax_out_loop.load(gm_temp2, expect_value=4)
                        gm_q_grad = batch_dot(gm_q_grad, l1_attention_out_loop, l1_softmax_out_loop,
                                              (seq_split_out, head_dim, seq_split_in), -1)
                        
                        # gm_temp.load(ub_bmm1_res_loop_last)
                        gm_k_grad = batch_dot(gm_k_grad, l1_q_loop, l1_softmax_out_loop,
                                              (seq_split_out, head_dim, seq_split_in), -1)
                        
                        l1_softmax_out_loop.load(gm_temp, expect_value=3)
                        gm_v_grad = batch_dot(gm_v_grad, l1_softmax_out_loop, l1_k_loop,
                                              (seq_split_out, seq_split_in, head_dim), -1)
                        
                        with Core("AIV0") as aiv:
                            '''在这个作用域下，仅处理：与AIC的同步'''
                            # task 1.2： 前向计算 AIC 部分, 依赖task1.1
                            ub_bmm1_res_loop_last = fa_forward_vec_part(gm_temp, gm_atten_mask_split,
                                                                        gm_softmax_log_max_sum_split,
                                                                        (seq_split_out, seq_split_in))
                            gm_temp.load(ub_bmm1_res_loop_last, set_value=3)
                            set_flag("PIPE-MTE3", "PIPE-MTE2", index)
                        
                            # task 2.2: softmax_out_grad计算 AIV 部分, 依赖 task2.1(重点关注) 和 task1.2(不用管)
                            gm_temp2 = softmax_out_grad_vec_part(gm_temp2, gm_softmax_out_sum_split,
                                                                 ub_bmm1_res_loop_last, (seq_split_out, seq_split_in),
                                                                 index)
                            index += 1


class TestDifferentMmad(TestBase):
    TRACE_FILE = 'trace.json'
    HTML_FILE = 'instruction_cycle_consumption.html'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_tensor_slice_mmad(self):
        with Chip("Ascend910B1", debug_mode=False) as chip:
            chip.enable_trace()
            chip.enable_metrics()
            # init input gm.
            gm_q = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim], format=FORMAT_TYPE_NZ)
            gm_k = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim], format=FORMAT_TYPE_NZ)
            gm_v = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim], format=FORMAT_TYPE_NZ)
            gm_atten_mask = Tensor("GM", "FP16", [seq_size, seq_size], format=FORMAT_TYPE_NZ)
            gm_attention_out_grad = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim],
                                           format=FORMAT_TYPE_NZ)
            gm_softmax_out_sum = Tensor("GM", "FP16", [batch_size, head_num, seq_size], format=FORMAT_TYPE_NZ)
            gm_softmax_log_max_sum = Tensor("GM", "FP16", [batch_size, head_num, seq_size], format=FORMAT_TYPE_NZ)

            # init output gm.
            gm_q_grad = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim], format=FORMAT_TYPE_NZ)
            gm_k_grad = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim], format=FORMAT_TYPE_NZ)
            gm_v_grad = Tensor("GM", "FP16", [batch_size, head_num, seq_size, head_dim], format=FORMAT_TYPE_NZ)

            flash_attention_grad(gm_q, gm_k, gm_v, gm_atten_mask, gm_attention_out_grad, gm_softmax_out_sum,
                                 gm_softmax_log_max_sum, gm_q_grad, gm_k_grad, gm_v_grad)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
