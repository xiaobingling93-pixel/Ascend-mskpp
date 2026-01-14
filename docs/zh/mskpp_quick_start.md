# **MindStudio Kernel Performance Prediction快速入门**

# 简介

MindStudio算子开发工具包含多个工具，如msKPP、msOpGen、msOpST、msSanitizer、msDebug和msProf等，本文档以一个简单样例介绍msKPP快速入门。

样例以单算子API调用方式为例，介绍如何使用算子开发工具进行算子设计。

**环境准备**

- 准备Atlas A2 训练系列产品/Atlas A2 推理系列产品的服务器，并安装对应的驱动和固件，具体安装过程请参见《[CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_quick.html?Mode=PmIns&InstallType=local&OS=openEuler&Software=cannToolKit)》中的“安装NPU驱动和固件”章节。
- 安装配套版本的CANN Toolkit开发套件包和ops算子包并配置CANN环境变量，请参见《[CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_quick.html?Mode=PmIns&InstallType=local&OS=openEuler&Software=cannToolKit)》。
- 若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见《[MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/82RC1/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》的“安装与卸载”章节。
- 在安装昇腾AI处理器的服务器执行**npu-smi info**命令进行查询，获取**Chip Name**信息。实际配置值为AscendChip Name，例如**Chip Name**取值为_xxxyy_，实际配置值为Ascend_xxxyy。_当Ascendxxxyy为代码样例路径时，需要配置Ascend_xxxyy_。

# 操作步骤

msKPP工具用于算子开发之前，帮助开发者在秒级时间内获取算子性能建模结果，可快速验证算子的实现方案。

1. 参考上述环境准备，完成msKPP工具相关配置。

2. 使用msKPP接口进行指令级别算子建模，模拟AscendC实现的add算子，示例如下：

    ```
    # 导入add算子建模需要的msKPP接口
    from mskpp import vadd, Tensor, Chip
    
    # 参照add算子在aicore内的指令实现，进行数据搬入->数据计算->数据搬出的过程建模
    def my_vadd(gm_x, gm_y, gm_z):
        # 向量Add的基本数据通路:
        #被加数x: GM-UB
        #加数y: GM-UB
        #结果向量z: UB-GM
     
        #定义和分配UB上的变量
        x = Tensor("UB")
        y = Tensor("UB")
        z = Tensor("UB")
    
        # 将GM上的数据移动到UB对应内存空间上
        x.load(gm_x)
        y.load(gm_y)
    
        # 当前数据已加载到UB上,调用指令进行计算,结果保存在UB上
        out = vadd(x, y, z)()
    
        # 将UB上的数据移动到GM变量gm_z的地址空间上 
        gm_z.load(out[0])
    
    if __name__== '__main__':
        with Chip("Ascendxxxyy") as chip:  # xxxyy为用户实际使用的具体芯片类型，可以使用命令npu-smi info进行查询
            chip.enable_trace()
            chip.enable_metrics()
    
            # 应用算子进行AI Core计算
            in_x = Tensor("GM", "FP16", [32, 48], format="ND") 
            in_y = Tensor("GM", "FP16", [32, 48], format="ND")
            in_z = Tensor("GM", "FP16", [32, 48], format="ND")
            my_vadd(in_x, in_y, in_z)
    ```

    >\> [!NOTE] 说明  
    > add算子介绍请参见[基础矢量算子](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/opdevg/Ascendcopdevg/atlas_ascendc_10_0033.html)。

3. 通过python3 xxx.py命令执行步骤2的Python.py脚本，将会在当前目录生成以下结果目录。目录中文件展现的具体内容请参见《[MindStudio Kernel Performance Prediction用户指南](./mskpp_user_guide.md)》中的“算子计算搬运规格分析、极限性能分析及算子Tiling初步设计”章节。

   ```
   MSKPP{timestamp}/
   ├── instruction_cycle_consumption.html
   ├── Instruction_statistic.csv
   ├── Pipe_statistic.csv
   └── trace.json
   ```

   **表 1**  建模结果文件

   | 文件名称                                           | 功能                                                         |
   | -------------------------------------------------- | ------------------------------------------------------------ |
   | 搬运流水统计（Pipe_statistic.csv）                 | 以PIPE维度统计搬运数据量大小、操作数个数以及耗时信息。       |
   | 指令信息统计（Instruction_statistic.csv）          | 统计不同指令维度的总搬运数据量大小、操作数个数以及耗时信息，能够发现指令层面上的瓶颈。 |
   | 指令占比饼图（instruction_cycle_consumption.html） | 以指令维度统计耗时信息，并以饼图形式展示。                   |
   | 指令流水图（trace.json）                           | 以指令维度展示耗时信息，并进行可视化展示。                   |

   


