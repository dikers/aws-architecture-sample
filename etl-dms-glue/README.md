#  DMS
--------------------------------------------


### 1. 使用RDS mysql 数据库

补图


###  2. DMS 介绍





![Image](https://docs.aws.amazon.com/zh_cn/dms/latest/userguide/images/datarep-Welcome.png)

![Image](https://docs.aws.amazon.com/zh_cn/dms/latest/userguide/images/datarep-intro-rep-instance1.png)

**运行 AWS DMS 过程的完整步骤**

* 要开始迁移项目，请确定您的源和目标数据存储。这些数据存储可以驻留在上述任何数据引擎上。

* 对于源和目标，请配置 AWS DMS 内指定到数据库的连接信息的终端节点。这些终端节点使用适当的 ODBC 驱动程序与您的源和目标进行通信。

* 预置复制实例，这是 AWS DMS 使用复制软件自动配置的服务器。

* 创建复制任务，该任务指定要迁移的实际数据表和应用的转换规则。AWS DMS 管理复制任务运行并提供有关迁移过程的状态。


### 3. 