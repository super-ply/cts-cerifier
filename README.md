# 杜康B
# 项目简介
背景：现有XTS测试下发任务时，项目管理人员因无法实时查看资源池导致无法合理下发测试任务，且测试过程中人工操作步骤多，影响测试效率，需要自动化方案来解决这些问题。
目的：通过软硬件开发，建设XTS工作站，利于项目管理组根据资源池空缺合理下发测试任务，并实现测试过程全自动化，节约人力，提高测试效率。

# 项目功能
* 可自由选择配置xts测试项
* 测试过程log日志可实时查看
* 测试报告自动保存并可自动上传至测试服务器
* 接口开放，可提供给设备及系统端调用

# 环境依赖
* python3.*
* mysql
* ftpserver

# 更新记录
2021/5/27 ： 【CSZX2019-1293】【feat】：测试用例管理模块搭建完成

# 项目结构
```
project
│   README.md                        // 辅助文档
│   LICENSE.txt                      // 许可说明  
└───testcases
│   └───camera                       // 具体模块 
│        	│   camera_01.py         // 具体测试用例
│           │   camera_02.py         // 具体测试用例
│           │   camera_03.py         // 具体测试用例  
│           │   ...
│	...

│   └───report                       // 报告存放地址
│           │   report_xxx      	 // 具体报告  
│           │   report_xxx       	 // 具体报告 
│           │   ...
│   
└───docs                             // 参考文档
    │   unittest_master                    // unittest 参考文档
    │   ...
│
│
└───utils                             // 辅助方法模块 
    │ 
    │   ...
│
└───runtimelog                       // 运行日志
    │ 
    │   ...

```