/* -------------------------------------------------------------------------
 * This file is part of the MindStudio project.
 * Copyright (c) 2025 Huawei Technologies Co.,Ltd.
 *
 * MindStudio is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *          http://license.coscl.org.cn/MulanPSL2
 *
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 * ------------------------------------------------------------------------- */

#include <gtest/gtest.h>
#include "mockcpp/mockcpp.hpp"
#include "linearInterpolate.h"

using namespace Mskpp;


TEST(LinearInterpolateTest, LinearInterpolate_All)
{
    // curves为空时返回0.0
    const std::map<uint32_t, double> curvesEmpty = {};
    double res = LinearInterpolate(curvesEmpty, 0);
    EXPECT_EQ(res, 0.0);

    const std::map<uint32_t, double> curves = { {1, 3.5}, {2, 5.1}, {4, 4.1}, {5, 14.1}, {6, 12.4}, {7, 5.9} };
    // 输入x大于等于最大横坐标，返回最大横坐标对应的值
    res = LinearInterpolate(curves, 8);
    EXPECT_EQ(res, 5.9);

    // 输入x小于等于最小横坐标，返回最小横坐标对应的值
    res = LinearInterpolate(curves, 0);
    EXPECT_EQ(res, 3.5);

    // 输入x数据处于范围返回结果
    res = LinearInterpolate(curves, 3);
    EXPECT_EQ(res, 4.6);
}