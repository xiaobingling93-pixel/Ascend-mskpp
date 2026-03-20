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

#include <iostream>
#include "task_generator.h"
#include "task_schedule.h"

namespace Mskpp {
void TaskSchedule::AddTask(RawTask& task)
{
    return TaskGenerator::instance()->AddTask(task);
}

int32_t TaskSchedule::Run()
{
    uint64_t totalDuration = 0;
    std::shared_ptr<Pipeline> pipe = TaskGenerator::instance()->GetNextPipe();
    while (pipe != nullptr) {
        pipe->Step();
        /* time start with 0, so last schedule-time is total duration */
        totalDuration = pipe->GetLastExecTime();
        pipe = TaskGenerator::instance()->GetNextPipe();
    }

    if (!TaskGenerator::instance()->IsAllPipesFinished()) {
        std::cout << "\n[WARNING] Scheduler stops and some tasks have not executed." << std::endl;
        if (debugMode) {
            TaskGenerator::instance()->DumpBlockedPipesInfo();
        }
        TaskGenerator::instance()->Clear();
        return -1;
    }
    TaskGenerator::instance()->Clear();
    return static_cast<int32_t>(totalDuration);
}

void TaskSchedule::Clear()
{
    TaskGenerator::instance()->Clear();
    debugMode = false;
}

void TaskSchedule::SetDebugMode(bool mode)
{
    debugMode = mode;
}

bool TaskSchedule::GetDebugMode() const
{
    return debugMode;
}
}