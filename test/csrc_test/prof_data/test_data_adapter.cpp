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
#include "data_adapter.h"

using namespace Mskpp;
TEST(DataAdapter, MovClass_All_Get)
{
    ArchInfo::instance()->SetChipType("Ascend910B1");
    MovClass movClass;
    std::string src = "GM";
    std::string dst = "L1";
    long dataSize = 256;
    bool transEnable = true;
    auto normalRes = movClass.Get(src, dst, dataSize, transEnable);
    EXPECT_DOUBLE_EQ(normalRes, 5.1017246664648646);

    dataSize = 65535;
    auto maxRes = movClass.Get(src, dst, dataSize, transEnable);
    EXPECT_DOUBLE_EQ(maxRes, 77.385824178508102);

    src = "L0C";
    dst = "GM";
    dataSize = 64;
    auto otherRes = movClass.Get(src, dst, dataSize, transEnable);
    EXPECT_DOUBLE_EQ(otherRes, 10.812870368172973);

    src = "GM";
    dst = "GM";
    auto abnormalRes = movClass.Get(src, dst, dataSize, transEnable);
    EXPECT_DOUBLE_EQ(abnormalRes, -1);

    auto peakRes = movClass.GetPeak(src, dst);
    EXPECT_DOUBLE_EQ(peakRes, -1);

    auto repeatRes = movClass.GetRepeat(src, dst, 20);
    EXPECT_DOUBLE_EQ(repeatRes, 0);
}

TEST(DataAdapter, MmadClass_All_Get)
{
    ArchInfo::instance()->SetChipType("Ascend910B1");
    MmadClass mmadClass;
    auto normalRes = mmadClass.Get(65535, "FP16");
    EXPECT_DOUBLE_EQ(normalRes, 7258.3852111999513);
}