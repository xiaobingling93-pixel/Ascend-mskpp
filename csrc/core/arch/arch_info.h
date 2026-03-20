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

#ifndef WORKLOAD_ANALYSIS_MSKPP_ARCH_INFO_H
#define WORKLOAD_ANALYSIS_MSKPP_ARCH_INFO_H

#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm>
#include "singleton.h"

namespace Mskpp {

int GetMemoryTypeEnumByName(const std::string& name);
int TheoreticalBandwidth(const std::string& src, const std::string& dst);
int GetDataTypeSizeOf(const std::string& dtype);
std::string GetPipeByIO(const std::string& inputTensorMemType, const std::string& outputTensorMemType);
bool IsSupportType(const std::string& tensorType);
bool IsSupportFormat(const std::string& tensorFormat);

enum class ChipType {
    ASCEND_910_B1 = 0,
    ASCEND_910_B3,
    ASCEND_910_95,
    ASCEND_UNKNOWN
};
using MTE_PAIR = std::pair<std::string, std::string>;

class ArchInfo : public Singleton<ArchInfo> {
public:
    explicit ArchInfo();
    virtual ~ArchInfo() {}

    void SetChipType(std::string inputChipType);
    std::string GetChipType();
    void SetCacheHitRatio(double ratio);
    double GetCacheHitRatio() const;
    bool IsMteIdValid(const std::string& fromType, const std::string& toType) const;
    int GetFreq() const;

private:
    ChipType chipType_;
    double cacheHitRatio_;
    int cubeNum_;
    int vectorNum_;
    std::vector<MTE_PAIR> mte_ = {{"GM", "L1"}, {"L1", "GM"}, {"GM", "UB"}, {"UB", "GM"}, {"UB", "UB"}, {"GM", "L0A"},
                                  {"GM", "L0B"}, {"L0C", "GM"}, {"L1", "L0A"}, {"L1", "L0B"}, {"L1", "L0C"},
                                  {"L0C", "L1"}, {"UB", "VEC"}, {"VEC", "UB"}};
    int freq_ = 1850;
};
}
#endif // WORKLOAD_ANALYSIS_MSKPP_ARCH_INFO_H
