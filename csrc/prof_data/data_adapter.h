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

#ifndef MSKPP_C_DATA_ADAPTER_H
#define MSKPP_C_DATA_ADAPTER_H

#include <cstdlib>
#include <string>
#include <utility>
#include <vector>
#include <map>
#include <set>
#include "resource910b.h"
#include "arch/arch_info.h"

namespace Mskpp {
/***************************define Mov type class data template**************************************/
class MovClass {
public:
    MovClass() = default;
    virtual ~MovClass() = default;
    double Get(std::string src, std::string dst, long dataSize, bool transEnable);
    double GetPeak(std::string src, std::string dst);
    double GetRepeat(const std::string& src, const std::string& dst, uint32_t repeat);
    bool InitOneMovPathData(std::string& movPath);
private:
    std::map<std::string, std::map<uint32_t, double>> movDatasMap; // {$src}2{$dst} or {$src}2{$dst}_TRANS
};

/***************************define MmadType data template**************************************/
class MmadClass {
public:
    MmadClass() = default;
    virtual ~MmadClass() = default;
    double Get(long granularity, std::string instrType);
};

/***************************define vec Type data template**************************************/
class VecClass {
public:
    explicit VecClass(std::string instrName) : instrName(std::move(instrName)) {};
    virtual ~VecClass() = default;
    double Get(long granularity, const std::string& instrType);
private:
    std::string instrName;
};
}

#endif // MSKPP_C_DATA_ADAPTER_H
