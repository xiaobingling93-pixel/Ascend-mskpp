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
#include "init_module.h"
#include "arch/arch_info.h"

using namespace Mskpp;

std::string SubstringBefore(const std::string& str, const std::string& subStr) {
    size_t pos = str.find(subStr);
    if (pos != std::string::npos) {
        return str.substr(0, pos + subStr.size());
    }
    return str;
}

class ProfDataTest : public testing::Test {
protected:
    PyObject *GetmoduleClass(const std::string &className)
    {
        PyObject *profData = InitProfdataModule();
        PyObject *moduleClass = PyObject_GetAttrString(profData, className.c_str());
        return moduleClass;
    }

    void SetUp() override {
        Py_Initialize();
    }

    void TearDown() override {
        Py_Finalize();  // 关闭 Python 解释器
    }

};

TEST_F(ProfDataTest, MmadData_Get_Success)
{
    std::string className = "MmadData";
    auto mmadDataClass = GetmoduleClass(className);
    EXPECT_TRUE(mmadDataClass != NULL);
    EXPECT_TRUE(PyCallable_Check(mmadDataClass));
    PyObject *pInstance = NULL;
    pInstance = PyObject_CallObject(mmadDataClass, NULL);
    EXPECT_TRUE(pInstance != NULL);

    // 从实例中获取get函数
    PyObject *get = PyObject_GetAttrString(pInstance, "get");
    // 检查函数是否存在且可调用
    EXPECT_TRUE(get != NULL);
    EXPECT_TRUE(PyCallable_Check(get));

    // 创建函数参数  MMADInstr->Get(granularity, std::string(instrType))
    PyObject *pArgs = PyTuple_New(2);
    PyObject *granularity = PyLong_FromLong(64);         // size
    PyObject *instrType = PyUnicode_FromString("FP32");  // data type
    PyTuple_SetItem(pArgs, 0, granularity);
    PyTuple_SetItem(pArgs, 1, instrType);

    // 调用get函数性能数据
    PyObject *getRes = PyObject_CallObject(get, pArgs);
    EXPECT_TRUE(getRes != NULL);
    auto res = PyFloat_AsDouble(getRes);
    EXPECT_DOUBLE_EQ(res, 3369.8066640000002);
    Py_DECREF(pInstance);
    Py_DECREF(get);
    Py_DECREF(pArgs);
    Py_DECREF(getRes);
}

TEST_F(ProfDataTest, MovData_Get_Success)
{
    std::string className = "MovData";
    auto movDataClass = GetmoduleClass(className);
    EXPECT_TRUE(movDataClass != NULL);
    EXPECT_TRUE(PyCallable_Check(movDataClass));
    PyObject *pInstance = NULL;
    pInstance = PyObject_CallObject(movDataClass, NULL);
    EXPECT_TRUE(pInstance != NULL);

    // 从实例中获取get函数
    PyObject *get = PyObject_GetAttrString(pInstance, "get");
    // 检查函数是否存在且可调用
    EXPECT_TRUE(get != NULL);
    EXPECT_TRUE(PyCallable_Check(get));

    // 创建函数参数  MOVInstr->Get(std::string(src), std::string(dst), dataSize, (bool) transEnable)
    PyObject *pArgs = PyTuple_New(4);
    PyObject *src = PyUnicode_FromString("GM");   // src
    PyObject *dst = PyUnicode_FromString("UB");   // dst
    PyObject *dataSize = PyLong_FromLong(128);    // dataSize
    PyObject *transEnable = PyLong_FromLong(0);   // transEnable

    PyTuple_SetItem(pArgs, 0, src);
    PyTuple_SetItem(pArgs, 1, dst);
    PyTuple_SetItem(pArgs, 2, dataSize);
    PyTuple_SetItem(pArgs, 3, transEnable);

    // 调用get函数性能数据
    PyObject *getRes = PyObject_CallObject(get, pArgs);
    EXPECT_TRUE(getRes != NULL);
    auto res = PyFloat_AsDouble(getRes);
    EXPECT_DOUBLE_EQ(res, 4.2336967532011123);
    Py_DECREF(get);
    Py_DECREF(pArgs);
    Py_DECREF(getRes);

    // 从实例中获取get_peak函数
    PyObject *getPeak = PyObject_GetAttrString(pInstance, "get_peak");
    // 检查函数是否存在且可调用
    EXPECT_TRUE(getPeak != NULL);
    EXPECT_TRUE(PyCallable_Check(getPeak));

    // 创建函数参数  movInstr->GetPeak(std::string(src), std::string(dst))
    PyObject *peakArgs = PyTuple_New(2);
    PyObject *peakSrc = PyUnicode_FromString("L1");   // src
    PyObject *peakDst = PyUnicode_FromString("L0A");  // dst
    // 需要将芯片类型设置为910b1保证索引至L1_TO_L0A_910b1
    ArchInfo::instance()->SetChipType("Ascend910B1");
    PyTuple_SetItem(peakArgs, 0, peakSrc);
    PyTuple_SetItem(peakArgs, 1, peakDst);

    // 调用get_peak函数性能数据
    PyObject *getPeakRes = PyObject_CallObject(getPeak, peakArgs);
    EXPECT_TRUE(getPeakRes != NULL);
    auto peakRes = PyFloat_AsDouble(getPeakRes);
    EXPECT_DOUBLE_EQ(peakRes, 253.95445140064865);
    Py_DECREF(getPeak);
    Py_DECREF(peakArgs);
    Py_DECREF(getPeakRes);

    // 从实例中获取get_repeat函数
    PyObject *getRepeat = PyObject_GetAttrString(pInstance, "get_repeat");
    // 检查函数是否存在且可调用
    EXPECT_TRUE(getRepeat != NULL);
    EXPECT_TRUE(PyCallable_Check(getRepeat));

    // 创建函数参数  movInstr->GetRepeat(std::string(src), std::string(dst), repeat)
    PyObject *repeatArgs = PyTuple_New(3);
    PyObject *repeatSrc = PyUnicode_FromString("GM");   // src
    PyObject *repeatDst = PyUnicode_FromString("L0A");  // dst
    PyObject *repeat = PyLong_FromLong(16);             // dataSize

    PyTuple_SetItem(repeatArgs, 0, repeatSrc);
    PyTuple_SetItem(repeatArgs, 1, repeatDst);
    PyTuple_SetItem(repeatArgs, 2, repeat);

    // 调用get_peak函数性能数据
    PyObject *getRepeatRes = PyObject_CallObject(getRepeat, repeatArgs);
    EXPECT_TRUE(getRepeatRes != NULL);
    auto repeatRes = PyFloat_AsDouble(getRepeatRes);
    EXPECT_DOUBLE_EQ(repeatRes, 175.65000000000001);
    Py_DECREF(getRepeat);
    Py_DECREF(repeatArgs);
    Py_DECREF(getRepeatRes);

    Py_DECREF(pInstance);
}

TEST_F(ProfDataTest, Vec_Get_Success)
{
    std::string className = "VbrcbData";
    auto vbrcbClass = GetmoduleClass(className);
    EXPECT_TRUE(vbrcbClass != NULL);
    EXPECT_TRUE(PyCallable_Check(vbrcbClass));
    PyObject *pInstance = NULL;
    pInstance = PyObject_CallObject(vbrcbClass, NULL);
    EXPECT_TRUE(pInstance != NULL);

    // 从实例中获取get函数
    PyObject *get = PyObject_GetAttrString(pInstance, "get");
    // 检查函数是否存在且可调用
    EXPECT_TRUE(get != NULL);
    EXPECT_TRUE(PyCallable_Check(get));

    // 创建函数参数  VBRCBInstr->Get(granularity, std::string(instrType))
    PyObject *pArgs = PyTuple_New(2);
    PyObject *granularity = PyLong_FromLong(16);         // size
    PyObject *instrType = PyUnicode_FromString("UINT16_UINT16");  // data type
    PyTuple_SetItem(pArgs, 0, granularity);
    PyTuple_SetItem(pArgs, 1, instrType);

    ArchInfo::instance()->SetChipType("Ascend910B1");

    // 调用get函数性能数据
    PyObject *getRes = PyObject_CallObject(get, pArgs);
    EXPECT_TRUE(getRes != NULL);
    auto res = PyFloat_AsDouble(getRes);
    EXPECT_DOUBLE_EQ(res, 84.650626034366169);
    Py_DECREF(pInstance);
    Py_DECREF(get);
    Py_DECREF(pArgs);
    Py_DECREF(getRes);
}

TEST_F(ProfDataTest, Vec_Get_All_Success)
{
    std::map<std::string, std::string> vecMap = {
        {"VconvData", "FP16_FP32"}, {"VabsData", "FP16_FP16"}, {"VaddData", "FP16_FP16_FP16"},
        {"VaddreluData", "FP16_FP16_FP16"}, {"VaddreluconvData", "FP32_FP32_FP16"}, {"VandData", "INT16_INT16_INT16"},
        {"VaxpyData", "FP16_FP16_FP16"}, {"VaddsData", "FP16_FP16_FP16"}, {"VbrcbData", "UINT16_UINT16"},
        {"VcaddData", "FP16_FP16"}, {"VcgaddData", "FP16_FP16"}, {"VcgmaxData", "FP16_FP16"},
        {"VcgminData", "FP16_FP16"}, {"VcmaxData", "FP16_FP16"}, {"VcminData", "FP16_FP16"}, {"VcmpData", "FP16_FP16"},
        {"VcmpvData", "FP16_FP16_FP16"}, {"VcmpvsData", "FP16_FP16_FP16"}, {"VconvdeqData", "INT32_FP16"},
        {"VconvvdeqData", "INT16_INT8"}, {"VcopyData", "INT16_INT16"}, {"VcpaddData", "FP16_FP16"},
        {"VdivData", "FP16_FP16_FP16"}, {"VectorDupData", "FP16_FP16"}, {"VexpData", "FP16_FP16"},
        {"VlnData", "FP16_FP16"}, {"VlreluData", "FP16_FP16_FP16"}, {"VmaddData", "FP16_FP16_FP16"},
        {"VmaxData", "FP16_FP16_FP16"}, {"VmaxsData", "FP16_FP16_FP16"}, {"VminData", "FP16_FP16_FP16"},
        {"VminsData", "FP16_FP16_FP16"}, {"VmrgsortData", "FP16_UINT64_FP16"}, {"VmulData", "FP16_FP16_FP16"},
        {"VmulsData", "FP16_FP16_FP16"}, {"VnotData", "INT16_INT16"}, {"VorData", "INT16_INT16_INT16"},
        {"VreluData", "FP16_FP16"}, {"VrecData", "FP16_FP16"}, {"VsubData", "FP16_FP16_FP16"},
        {"VrsqrtData", "FP16_FP16"}, {"VselData", "FP16_FP16_FP16"}, {"VshlData", "INT16_INT16"},
        {"VshrData", "INT16_INT16"}, {"VsqrtData", "FP16_FP16"}, {"VsubReluConvData", "FP32_FP32_FP16"},
        {"VsubReluData", "FP16_FP16_FP16"}, {"VmaddReluData", "FP32_FP32_FP32"}, {"VmlaData", "FP32_FP32_FP32"},
        {"Vreducev2Data", "UINT32_UINT32_UINT32"}, {"VreduceData", "UINT32_UINT32_UINT32"},
        {"VmulconvData", "FP16_FP16_INT8"}, {"VgatherData", "UINT16_UINT16"}, {"VgatherbData", "UINT16_UINT16"},
        {"VconvData1", "FP32_FP16"},
        {"VconvData2", "FP16_INT4"}, {"VconvData3", "FP16_INT8"}, {"VconvData4", "FP16_UINT8"}, {"VconvData5", "INT4_FP16"},
        {"VconvData6", "FP16_INT32"}, {"VconvData7", "FP32_INT32"}, {"VconvData8", "FP16_INT16"}, {"VconvData9", "BF16_FP32"},
        {"VconvData10", "INT32_FP32"}, {"VconvData11", "FP32_INT64"}, {"VconvData12", "INT16_FP16"}, {"VconvData13", "INT16_FP32"},
        {"VconvData14", "INT64_FP32"}, {"VconvData15", "FP32_BF16"}, {"VconvData16", "INT8_FP16"}, {"VconvData17", "UINT8_FP16"}
    };
    std::vector<double> resVec = {
        63.082776430000003, 42.260682379999999, 84.547185420000005, 84.269154360000002, 85.676037480000005,
        83.385585039999995, 84.382205240000005, 84.650626034366169, 36.077374689999999, 36.376114819999998,
        36.12451669, 36.332181159999998, 37.168676099999999, 36.401951490000002, 63.57255404, 36.425907070000001,
        36.37515861, 85.800085800000005, 42.267659960000003, 84.624742158988738, 84.660984018585722, 84.624742158988738,
        84.645447992646424, 84.609219430375049, 84.640270584365027, 84.567853314415672, 84.562685393778025,
        84.043958930000002, 83.845357719999996, 83.967462609999998, 83.972558030000002, 84.650626034366169,
        84.624742158988738, 84.660984018585722, 83.835198340000005, 83.703350099999994, 36.366554989999997,
        84.645447989999994, 63.522942700000002, 31.70616313, 84.384847649999998, 64.570154459999998,
        9.4710948474654284, 23.220575969999999, 64.499874019999993, 84.423389900000004, 42.139709600000003,
        42.427833321593866, 84.038854839999999, 82.409446180000003, 83.335367890000001, 83.290224140000007,
        42.370672212369755, 11.63029209524028, 42.260682379999999, 84.228120018490699, 84.521364759999997,
        63.252904139999998, 84.464614769999997, 63.166284009999998, 84.392497638823201, 18.246094195461286,
        84.604046449999998, 83.657806890000003, 84.567853310000004, 63.232671529999998, 63.555035310000001,
        63.307886529999998, 84.330780899999993, 84.397644779999993, 84.459459460000005,
    };
    int start = 0;
    ArchInfo::instance()->SetChipType("Ascend910B1");
    std::map<std::string, PyObject *> getMap;
    for (const auto &vec : vecMap) {
        // 将vec.first中的数字去除，还原成VxxData
        std::string instrName = SubstringBefore(vec.first, "Data");
        if (getMap.count(instrName) == 0) {
            PyObject *vecClass = GetmoduleClass(instrName.c_str());
            EXPECT_TRUE(vecClass != NULL);
            EXPECT_TRUE(PyCallable_Check(vecClass));
            PyObject *pInstance = PyObject_CallObject(vecClass, NULL);
            EXPECT_TRUE(pInstance != NULL);
            getMap[instrName] = pInstance;
        }

        PyObject *get = PyObject_GetAttrString(getMap[instrName], "get");
        // 检查函数是否存在且可调用
        EXPECT_TRUE(get != NULL);
        EXPECT_TRUE(PyCallable_Check(get));
        // 创建函数参数  VECInstr->Get(granularity, std::string(instrType))
        PyObject *pArgs = PyTuple_New(2);
        PyObject *granularity = PyLong_FromLong(16);         // size
        PyObject *instrType = PyUnicode_FromString(vec.second.c_str());  // data type
        PyTuple_SetItem(pArgs, 0, granularity);
        PyTuple_SetItem(pArgs, 1, instrType);

        // 调用get函数性能数据
        PyObject *getRes = PyObject_CallObject(get, pArgs);
        EXPECT_TRUE(getRes != NULL);
        auto res = PyFloat_AsDouble(getRes);
        EXPECT_DOUBLE_EQ(res, resVec[start++]);
        Py_DECREF(get);
        Py_DECREF(pArgs);
        Py_DECREF(getRes);
    }
    for(auto &getPair : getMap) {
        Py_DECREF(getPair.second);
    }
}
