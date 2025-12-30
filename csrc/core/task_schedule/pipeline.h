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

#ifndef __MSKPP_TASKSCHEDULE_PIPELINE__
#define __MSKPP_TASKSCHEDULE_PIPELINE__

#include <string>
#include <queue>
#include "raw_task.h"

namespace Mskpp {
/* [Name]: Pipeline
 * [Description]: 任务流水线，用于管理本流水线的任务数据和调度。主要功能如下：
 *                1、提供AddTask接口，将任务加入到本流水线
 *                2、提供Step接口，若队首任务可执行，对其执行；task是调度的最小执行单元
 *                3、同流水线内的任务先进先出
 * [Notice]: pipeline调度优先级的计算规则为：lastExecTime + 队首任务的耗时，该值越小，优先级越高；
 *                                         该计算规则可以保证所有任务按结束时间从早到迟执行
 */

class Pipeline {
public:
    explicit Pipeline(std::string pipeName) : name(pipeName) {};
    ~Pipeline() = default;
    std::string GetName();
    void AddTask(RawTask& task);
    void Step();
    uint64_t GetLastExecTime() const;
    /* UpdateTime shall be call when blocking is releaseed */
    void UpdateTime(uint64_t time);
    /* IsBlocked will not re-judge blocking status, while IsBlockingReleased will */
    bool IsBlocked() const;
    bool IsBlockingReleased();
    bool IsFinished();
    uint64_t GetPriority() const;
    std::string GetFirstTaskName();
    void DumpTasksInfo();

private:
    std::string name;
    bool blocked = true;
    uint64_t lastExecTime = 0;
    std::queue<RawTask> tasks;
};
}
#endif