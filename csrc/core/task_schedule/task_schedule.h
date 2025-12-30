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

#ifndef __MSKPP_TASK_SCHEDULE__
#define __MSKPP_TASK_SCHEDULE__

#include <string>
#include <utility>
#include <memory>
#include <map>
#include "singleton.h"
#include "raw_task.h"
#include "pipeline.h"
#include "task_generator.h"

namespace Mskpp {
/* [Name]: TaskSchedule
 * [Description]: 离散事件调度模拟类，作为对外能力接口提供。主要功能如下：
 *                1、提供AddTask接口，将任务加入到调度系统中统一管理
 *                2、提供Run接口，调度器会触发所有可调度的任务执行，直至所有任务都执行完或所有剩余任务都阻塞
 *                3、任务执行顺序：同pipe内串行、不同pipe间可并发、任务对象自定义pipe间依赖条件，根据以上条件计算最优调度
 * [Notice]: 1、不支持在run过程中添加事件
 * [Other]: 当前RawTask的定义是关联了一个python对象，若后续需要扩展其他用法，可抽象一个task基类，此处用基类指针+虚函数实现多态
 */

class TaskSchedule : public Singleton<TaskSchedule> {
public:
    TaskSchedule() = default;
    ~TaskSchedule() = default;
    void AddTask(RawTask& task);
    /* return run total duration, negative number for failure */
    int32_t Run();
    void Clear();
    void SetDebugMode(bool mode);
    bool GetDebugMode();

private:
    bool debugMode = false;
};
}
#endif