
# MindStudio Kernel Performance Prediction

# 最新消息
- [2025.12.30]：MindStudio Kernel Performance Prediction项目首次上线 


# 简介
MindStudio Kernel Performance Prediction（算子设计，msKPP）是一款性能仿真工具，支持用户输入算子表达，进而预测算子在这一算法实现下的性能上限。相较于cycle级仿真器，其仿真速度有数量级的提升。由于本身针对性能的预测不需要进行真实的计算，仅需要依据输入和输出的规模，给出对应算法的执行时间，故而，可以在秒级给出性能结果。  


# 目录结构  
├── docs  // 项目文档介绍  
├── mskpp// python代码目录  
│      ├──\_\_init\_\_.py  
│      └── ....  
├── csrc  // CPP源码目录  
│     └── CMakeList.txt  // c代码用的cmake  
├── example  // 工具样例存放目录  
│     └── README.md  // 工具样例说明  
├── setup.py  // 打包脚本  
├── test  // 测试部分，需提供覆盖率统计脚本  
│     └── build_test.py  // 用于进行测试场景的构建，此时不打wheel包  
├── output  // 脚本生成，存放编译生成的交付件  
├── build.py  // 端到端构建脚本  
├── CMakeLists.txt  // 构建总配置  
├── requirements.txt  // python依赖  
└── README.md  // 整体仓代码说明


# 环境部署
## 环境依赖
- 硬件环境请参见《[昇腾产品形态说明](https://www.hiascend.com/document/detail/zh/AscendFAQ/ProduTech/productform/hardwaredesc_0001.html)》。
- 工具的使用运行需要提前获取并安装CANN开源版本，当前CANN开源版本正在发布中，敬请期待。
## 工具安装
介绍msKPP工具的环境依赖及安装方式，具体请参见[msKPP安装指南](./docs/zh/mskpp_install_guide.md)。


#  快速入门
msKPP工具详细的快速入门请参见[msKPP快速入门](https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0003.html?framework=mindspore)。



# 工具限制与注意事项
- 使用msKPP库实现算子仿真，注意事项包括：
    + 实现模拟算子建模前，需要从mskpp库导入Tensor, Chip, 以及算子实现所必要的指令（统一以小写命名）。
    + 参照工程中的样例`sample_vadd.py`或`sample_mmad.py`，以with语句开启算子实现代码的入口，enable_trace和enable_metrics两个接口可使能trace打点图和指令统计功能。
- 二次开发请保证输入数据可信安全。


# 功能介绍

- [算子特性建模](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0009.html)：基于msKPP提供的接口模拟出算子耗时。
- [算子计算搬运规格分析](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0010.html)：生成搬运流水统计文件和指令信息统计文件，可查看msKPP建模结果。
- [极限性能分析](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0011.html)：生成文件指令流水图和指令占比饼图，可查看msKPP建模结果。
-  [算子tiling初步设计](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0011.html)：能够快速筛选出几种较优的tiling策略。



# API参考
msKPP工具分为基础功能接口和指令接口两种接口类型。具体内容请参见[msKPP对外接口使用说明](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0001.html)。

# 免责声明
## 致msKPP使用者
- 本工具仅供调试和开发之用，使用者需自行承担使用风险，并理解以下内容：
    - 数据处理及删除：用户在使用本工具过程中产生的数据属于用户责任范畴。建议用户在使用完毕后及时删除相关数据，以防信息泄露。
    - 数据保密与传播：使用者了解并同意不得将通过本工具产生的数据随意外发或传播。对于由此产生的信息泄露、数据泄露或其他不良后果，本工具及其开发者概不负责。
    - 用户输入安全性：用户需自行保证输入的命令行的安全性，并承担因输入不当而导致的任何安全风险或损失。对于由于输入命令行不当所导致的问题，本工具及其开发者概不负责。
- 免责声明范围：本免责声明适用于所有使用本工具的个人或实体。使用本工具即表示您同意并接受本声明的内容，并愿意承担因使用该功能而产生的风险和责任，如有异议请停止使用本工具。
- 在使用本工具之前，请谨慎阅读并理解以上免责声明的内容。对于使用本工具所产生的任何问题或疑问，请及时联系开发者。
## 致数据所有者
如果您不希望您的模型或数据集等信息在msKPP中被提及，或希望更新msKPP中有关的描述，请在Gitcode提交issue，我们将根据您的issue要求删除或更新您相关描述。衷心感谢您对msKPP的理解和贡献。

# License

msKPP产品的使用许可证，具体请参见[LICENSE](./LICENSE)文件。  
msKPP工具docs目录下的文档适用CC-BY 4.0许可证，具体请参见[LICENSE](./docs/LICENSE)。


# 贡献声明
1. 提交错误报告：如果您在msKPP中发现了一个不存在安全问题的漏洞，请在msKPP仓库中的Issues中搜索，以防该漏洞已被提交，如果找不到漏洞可以创建一个新的Issues。如果发现了一个安全问题请不要将其公开，请参阅安全问题处理方式。提交错误报告时应该包含完整信息。
2. 安全问题处理：本项目中对安全问题处理的形式，请通过邮箱通知项目核心人员确认编辑。
3. 解决现有问题：通过查看仓库的Issues列表可以发现需要处理的问题信息, 可以尝试解决其中的某个问题。
4. 如何提出新功能：请使用Issues的Feature标签进行标记，我们会定期处理和确认开发。
5. 开始贡献：  
    1. Fork本项目的仓库。  
    2. Clone到本地。  
    3. 创建开发分支。  
    4. 本地测试：提交前请通过所有单元测试，包括新增的测试用例。  
    5. 提交代码。  
    6. 新建Pull Request。  
    7. 代码检视，您需要根据评审意见修改代码，并重新提交更新。此流程可能涉及多轮迭代。  
    8. 当您的PR获得足够数量的检视者批准后，Committer会进行最终审核。  
    9. 审核和测试通过后，CI会将您的PR合并入到项目的主干分支。


# 建议与交流

欢迎大家为社区做贡献。如果有任何疑问或建议，请提交[Issues](https://gitcode.com/Ascend/mskpp/issues)，我们会尽快回复。感谢您的支持。

#  致谢

msKPP由华为公司的下列部门联合贡献：

- 计算产品线

感谢来自社区的每一个PR，欢迎贡献msKPP。