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

namespace Mskpp {
void TaskGenerator::AddTask(RawTask& task)
{
    std::shared_ptr<Pipeline> p;
    auto it = pipesAll.find(task.GetOwner());
    if (it == pipesAll.end()) {
        p = std::make_shared<Pipeline>(task.GetOwner());
        pipesAll[task.GetOwner()] = p;
    } else {
        p = it->second;
    }
    p->AddTask(task);
}

void TaskGenerator::InitPipeQueue()
{
    /* move all pipes to schedule queue */
    auto it = pipesAll.begin();
    while (it != pipesAll.end()) {
        if (it->second->IsBlockingReleased()) {
            pipesActive.push(it->second);
        } else {
            pipesBlocked.push_back(it->second);
        }
        it = pipesAll.erase(it);
    }
}

void TaskGenerator::RefreshPipesStatus()
{
    /* if nothing returned in last time, nothing to be refreshed */
    if (lastReturnedPipe == nullptr) {
        return;
    }

    /* Traverse blocked pipes, find those that are unblocked */
    uint64_t timeToUnblocked = lastReturnedPipe->GetLastExecTime();
    auto it = pipesBlocked.begin();
    while (it != pipesBlocked.end()) {
        if ((*it)->IsBlockingReleased()) {
            (*it)->UpdateTime(timeToUnblocked);
            pipesActive.push(*it);
            it = pipesBlocked.erase(it);
        } else {
            it++;
        }
    }

    /* Process last retuened pipe */
    if (!lastReturnedPipe->IsFinished()) {
        if (lastReturnedPipe->IsBlocked()) {
            pipesBlocked.push_back(lastReturnedPipe);
        } else {
            pipesActive.push(lastReturnedPipe);
        }
    }
    lastReturnedPipe.reset();
}

std::shared_ptr<Pipeline> TaskGenerator::GetNextPipe()
{
    if (!initialized) {
        InitPipeQueue();
        initialized = true;
    }

    /* Generator don't care whether scheduler does something with last
       returned pipeline, so refresh the status. */
    RefreshPipesStatus();

    if (pipesActive.empty()) {
        return nullptr;
    }

    lastReturnedPipe = pipesActive.top();
    pipesActive.pop();

    return lastReturnedPipe;
}

bool TaskGenerator::IsAllPipesFinished() const
{
    return (pipesAll.empty() && pipesBlocked.empty() && pipesActive.empty());
}

void TaskGenerator::DumpBlockedPipesInfo() const
{
    for (const auto& pipe : pipesBlocked) {
        std::cout << "[DEBUG] Pipe " << pipe->GetName() << " " << pipe->GetFirstTaskName() << " is blocked."
        << std::endl;
    }
}

void TaskGenerator::Clear()
{
    pipesAll.clear();
    pipesBlocked.clear();
    while (!pipesActive.empty()) {
        pipesActive.pop();
    }
    lastReturnedPipe.reset();
    initialized = false;
}
}