#  DMS
--------------------------------------------

###  1. DMS 介绍


![Image](https://docs.aws.amazon.com/zh_cn/dms/latest/userguide/images/datarep-Welcome.png)
**运行 AWS DMS 过程的完整步骤**

* 要开始迁移项目，请确定您的源和目标数据存储。这些数据存储可以驻留在上述任何数据引擎上。

* 对于源和目标，请配置 AWS DMS 内指定到数据库的连接信息的终端节点。这些终端节点使用适当的 ODBC 驱动程序与您的源和目标进行通信。

* 预置复制实例，这是 AWS DMS 使用复制软件自动配置的服务器。

* 创建复制任务，该任务指定要迁移的实际数据表和应用的转换规则。AWS DMS 管理复制任务运行并提供有关迁移过程的状态。



![Image](https://docs.aws.amazon.com/zh_cn/dms/latest/userguide/images/datarep-intro-rep-instance1.png)

**使用 AWS DMS 时您需要执行以下操作：**

* 创建复制服务器。
* 创建源和目标终端节点，它们具有有关您的数据存储的连接信息。
* 创建一个或多个迁移任务以在源和目标数据存储之间迁移数据。




### 2. 使用RDS mysql 数据库

使用RDS 创建数据库 demo_db, 以及表tb_user, 如下图

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/001.png?raw=true)


### 3. 创建复制服务器

打开AWS Database Migration Service 服务， 新建复制服务器 （Replication instances）如图： 

点击右上方 创建按钮
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/002.png?raw=true)

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/003.png?raw=true)


### 4. 创建源节点 Source Endpoints

点击右上方 创建按钮
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/004.png?raw=true)

- 1. 选择  Source endpoint
- 2. 选择  RDS DB instance
- 3. 填写数据库 url  用户名 密码

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/005.png?raw=true)


### 5. 创建目标节点 Target Endpoints

* 选择 目标终端节点
* 注意 服务访问角色ARN  必须有写入s3的权限
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/006.png?raw=true)




### 6. 创建任务

**点击右上方 创建按钮**
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/012.png?raw=true)



- 1. 填写名称
- 2. 填写复制实例
- 3. 填写 源
- 4. 填写 目标
- 5. 填写 复制方式

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/013.png?raw=true)


**添加选择规则**

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/014.png?raw=true)


**添加转换规则**

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/015.png?raw=true)


### 7. 查看结果

在对应的s3中查看结果
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/016.png?raw=true)