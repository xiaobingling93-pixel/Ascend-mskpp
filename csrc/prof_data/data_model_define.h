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

#ifndef MSKPP_PROFDATA_DATA_MODEL_DEFINE
#define MSKPP_PROFDATA_DATA_MODEL_DEFINE
#include <memory>
#include <functional>
#include <utility>
#include "singleton.h"
#include "data_adapter.h"

namespace Mskpp {
/**
 * 数据工厂类，通过map维护对象
 * Register提供工厂的注册方法
 * Create获取存储的对象
 * **/
template<typename T, typename ... Args>
class DataFactory : public Singleton<DataFactory<T, Args...>> {
public:
    void Register(const std::string name, std::function<std::shared_ptr<T>(Args...)> creator)
    {
        creator_[name] = creator;
    }
    std::shared_ptr<T> Create(const std::string name, Args... args)
    {
        return creator_.find(name) == creator_.end() ? std::shared_ptr<T>() : creator_[name](args...);
    }

private:
    std::map<std::string, std::function<std::shared_ptr<T>(Args...)>> creator_;
};


/**
 * DataRegister数据注册类，获取工厂的实例化对象，调用工厂的注册方法
 * **/
template<typename Base, typename Impl, typename... Args>
class DataRegister {
public:
    explicit DataRegister(const std::string &name)
    {
        DataFactory<Base, Args...> *dataFactory = DataFactory<Base, Args...>::instance();
        dataFactory->Register(name, [](Args... args) {
            return std::shared_ptr<Base>(std::make_shared<Impl>(args...));
        });
    }
};

using MovFactory = DataFactory<MovClass>;
using MmadFactory = DataFactory<MmadClass>;
using VecFactory = DataFactory<VecClass, std::string>;

#define INSTR_CLASS_DEFINE_NO_PARA(instrName, baseClass) \
    class instrName##Data : public baseClass##Class, public Singleton<instrName##Data> {}
#define INSTR_CLASS_DEFINE_SINGLE_PARA(instrName, baseClass)                                  \
    class instrName##Data : public baseClass##Class, public Singleton<instrName##Data>        \
    {                                                                                         \
    public:                                                                                   \
        explicit instrName##Data(std::string opName) : baseClass##Class(std::move(opName)) {} \
    }
}

#endif