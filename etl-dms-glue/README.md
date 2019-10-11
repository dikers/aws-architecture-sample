#  DMS
--------------------------------------------
本项目是一个DMS + Glue 是入门教程， 将RDS 中的数据通过DMS导入到S3中， 然后通过Glue处理， 再写入到S3中。 



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

- 选择  Source endpoint
- 选择  RDS DB instance
- 填写数据库 url  用户名 密码

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/005.png?raw=true)


### 5. 创建目标节点 Target Endpoints

* 选择 目标终端节点
* 注意 服务访问角色ARN  必须赋予DMS有写入s3的权限


![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/0051.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/0052.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/0053.png?raw=true)



![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/006.png?raw=true)




### 6. 创建任务

**点击右上方 创建按钮**
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/012.png?raw=true)



- 填写名称
- 填写复制实例
- 填写 源
- 填写 目标
- 填写 复制方式

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/013.png?raw=true)


**添加选择规则**

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/014.png?raw=true)


**添加转换规则**

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/015.png?raw=true)


### 7. 查看结果

在对应的s3中查看结果
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/016.png?raw=true)




#  Glue
---------------------------------------------------


###  Glue 简介



### 爬网程序

#### 设置Role   
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/100.png?raw=true)


![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/101.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/102.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/103.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/104.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/105.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/106.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/107.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/108.png?raw=true)

####  运行爬网程序
在这里需要点击立即运行 
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/109.png?raw=true)





### 创建作业


[官方文档](https://docs.aws.amazon.com/zh_cn/glue/latest/dg/author-job.html)

![Image](https://docs.aws.amazon.com/zh_cn/glue/latest/dg/images/AuthorJob-overview.png)

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/120.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/121.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/122.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/123.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/124.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/125.png?raw=true)
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/126.png?raw=true)


需要修改最后三行代码， 将数据保存到s3中， 供后续处理。 

```
# 需要修改的s3 文件路径  connection_options = {"path":"s3://你自己的s3桶名称/dms/glue/jobTest01.json"}

# 新加这行代码
datasink4 = glueContext.write_dynamic_frame.from_options(frame = resolvechoice3, connection_type = "s3", connection_options = {"path":"s3://dikers.nwcd/dms/glue/jobTest01.json"}, format = "json",  transformation_ctx = "datasink4")

# 注释掉下面这行代码
## datasink4 = glueContext.write_dynamic_frame.from_catalog(frame = resolvechoice3, database = "demo_db", table_name = "load00000001_csv", transformation_ctx = "datasink4")

job.commit()

```



###  查看输出结果
![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/127.png?raw=true)



### 将csv 文件导入到Redshift 中

```
# 1  在redshift 中新建表
create table tb_user (id int, name varchar, age int , sex int);


# 2  使用copy 导入csv 文件
copy tb_user from 's3://dikers.nwcd/dms/demo/demo_db/tb_user/LOAD00000001.csv'
credentials 'aws_access_key_id=<Your-Access-Key-ID>;aws_secret_access_key=<Your-Secret-Access-Key>'  
csv

# 3  查询数据
select * from tb_user;
```

![Image](https://github.com/dikers/aws-architecture-sample/blob/master/etl-dms-glue/image/300.png?raw=true)
