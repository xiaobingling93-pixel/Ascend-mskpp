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

#ifndef __MSKPP_TASK_GENERATOR__
#define __MSKPP_TASK_GENERATOR__

#include <string>
#include <utility>
#include <memory>
#include <map>
#include "singleton.h"
#include "raw_task.h"
#include "pipeline.h"

namespace Mskpp {
/* [Name]: TaskGenerator
 * [Description]: 提供调度管道数据的统一管理能力。主要功能如下：
 *                1、提供AddTask接口，将任务加入到生成器统一管理
 *                2、提供GetNextPipe接口，每次返回调度优先级最高的pipeline
 * [Notice]: 1、若调度结束后仍有部分管道阻塞，建议在导出诊断信息后调Clear()清理，以免对后续使用产生影响
 *           2、不支持在调度过程中添加事件
 *           3、若存在相同优先级的pipeline，其模拟层面的调度顺序无法保证
 */

class TaskGenerator : public Singleton<TaskGenerator> {
public:
    TaskGenerator() = default;
    ~TaskGenerator() = default;
    void AddTask(RawTask& task);
    /* return highest-priority pipe, while return nullptr when no pipe can be scheduled */
    std::shared_ptr<Pipeline> GetNextPipe();
    bool IsAllPipesFinished();
    void DumpBlockedPipesInfo();
    void Clear();

private:
    void InitPipeQueue();
    /* aux func, scheduler may do something with returned pipe, process it */
    void RefreshPipesStatus();

private:
    struct PipePtrCmp {
        bool operator()(std::shared_ptr<Pipeline> p1, std::shared_ptr<Pipeline> p2)
        {
            return p1->GetPriority() > p2->GetPriority();
        }
    };

    /* pipesAll: Temporary variables used during initialization */
    std::map<std::string, std::shared_ptr<Pipeline>> pipesAll;
    std::priority_queue<std::shared_ptr<Pipeline>, std::vector<std::shared_ptr<Pipeline>>, PipePtrCmp> pipesActive;
    std::vector<std::shared_ptr<Pipeline>> pipesBlocked;
    std::shared_ptr<Pipeline> lastReturnedPipe;
    bool initialized = false;
};
}
#endif