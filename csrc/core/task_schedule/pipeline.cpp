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

#include "pipeline.h"

namespace Mskpp {
void Pipeline::AddTask(RawTask& task)
{
    tasks.push(task);
}

void Pipeline::Step()
{
    if (blocked || tasks.empty()) {
        return;
    }

    RawTask& curTask = tasks.front();
    curTask.SetDuration(lastExecTime, lastExecTime + curTask.GetCostTime());
    curTask.Run();
    lastExecTime += curTask.GetCostTime();
    tasks.pop();

    if (tasks.empty()) {
        return;
    }

    RawTask& nextTask = tasks.front();
    if (!nextTask.IsReady()) {
        blocked = true;
    }
}

bool Pipeline::IsBlockingReleased()
{
    if (tasks.empty()) {
        return false;
    }
    if (!blocked) {
        return true;
    }

    RawTask& curTask = tasks.front();
    if (curTask.IsReady()) {
        blocked = false;
        return true;
    }
    return false;
}

uint64_t Pipeline::GetLastExecTime() const
{
    return lastExecTime;
}

void Pipeline::UpdateTime(uint64_t time)
{
    lastExecTime = time;
}

bool Pipeline::IsBlocked() const
{
    return blocked;
}

bool Pipeline::IsFinished() const
{
    return tasks.empty();
}

uint64_t Pipeline::GetPriority() const
{
    if (blocked || tasks.empty()) {
        return UINT_MAX;
    }

    return lastExecTime + tasks.front().GetCostTime();
}

std::string Pipeline::GetFirstTaskName()
{
    if (tasks.empty()) {
        return "";
    }
    auto first = tasks.front();
    return first.GetName();
}


std::string Pipeline::GetName()
{
    return name;
}
}