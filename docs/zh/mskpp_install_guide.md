# MindStudio Kernel Performance Prediction安装指南

# 安装说明
msKPP（MindStudio Kernel Performance Prediction，算子设计）工具是一款性能仿真工具，支持用户输入算子表达，进而预测算子在这一算法实现下的性能上限。本文主要介绍通过安装CANN算子包安装msKPP工具的安装方法。  


# 安装前准备
**配置用户名和秘钥**

为了避免依赖下载过程中反复输入密码，可通过如下命令配置git保存用户密码：
```
git config --global credential.helper store
```

**准备工具**
- 要求构建环境中安装python3.9或以上版本。
- mskpp需要依赖其他python库。通过pip install -r requirement.txt一键式安装依赖库。
- `gcc 版本 > 7.4.0`  
- `3.20.2 <= CMAKE版本 <= 3.31.10`

# 安装步骤

## 软件包构建
要求构建环境中安装`python3.9`或以上版本，构建出的包才能正常运行。
可以通过如下命令构建和打包：
```
mkdir build
cd build
cmake ..
make -j8 install
```
也可以通过一键式脚本来执行：
```
python build.py
```

## 安装软件包
mskpp会以whl包的形式安装在CANN包目录下，source环境变量后即可直接使用，但在工具POC形态不断补充指令的情况下，建议通过如下链接下载，本版本使用说明暂以链接下载zip包的方式进行步骤解读。

```
https://gitcode.com/Ascend/mskpp
```

mskpp需要依赖其他python库。通过`pip install -r requirement.txt`一键式安装依赖库。
依赖库列表如下
```
plotly>=5.11.0
```

### 安装whl包
```
cd output
pip install mskpp-xxxxx.whl
```

# 安装后配置
### CANN包使用
当前CANN包中已集成mskpp。在激活CANN环境，即可在自己的python脚本中使用mskpp
```
source ~/Ascend/cann/set_env.sh
python
>>> import mskpp
>>> ...
```


# 卸载
卸载则通过如下命令卸载：
```
pip uninstall mskpp-xxxxx.whl 
```

# 升级
如需使用whl包替换运行环境原有已安装的whl包，执行如下安装操作：
```
pip install mskpp-xxxxx.whl --force-reinstall
```
安装过程中，若提示是否替换原有安装包：
输入"y"，则安装包会自动完成升级操作。

# UT测试
可以通过一键式脚本来执行（注：python的UT测试，依赖pytest和coverage工具，可通过执行 ```pip install coverage pytest``` 安装）。：
```
python build.py test
```
