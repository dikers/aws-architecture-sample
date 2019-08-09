# EMR + Flink 在线数据分析




### 架构图
![Image](https://s3.amazonaws.com/dikers.nwcd/wordcount/arch.jpeg)


本项目是一个基于AWS EMR + Flink 在线数据分析的一个DEMO,步骤：
1. 如图所示前端Web, 收集实时的搜索数据，发送给Api Gateway + lambda. 
2. Lambda 发送数据到kinesis 
3. 然后发给EMR 集群的Flink 做数据分析 
4. 然后Flink 通过Kinesis 发给lambda 保存到 DynamoDB中 
5. 最后前端Web Dashboard 通过lambda 读取DynamoDB 



### 目录说明
```
.
├── README.md                                                   #
├── build.sh                                                    #编译脚本
├── flink-sink-lambda                           
│   ├── README.md
│   └── lambda_function.py                                      # 读取Flink 数据，保存到DynamoDB 的lambda
├── pom.xml
├── src
│   └── main
│       ├── java
│       │   └── com
│       │       └── dikers
│       │           └── emr
│       │               └── flink
│       │                   └── KinesisFlinkDemo.java           # Flink 相关java 代码
├── web-dashboard
│   ├── README.md
│   ├── lambda
│   │   └── lambda_function.py                                  # 读取Dashboard展示所需要数据的 lambda 
│   └── web                                                     # Dashboard web 界面
│       ├── app.js                                              
│       └── index.html
└── web-send-data
    ├── README.md
    ├── lambda
    │   └── lambda_function.py                                  # 处理发送数据相关lambda
    └── web                                                     # 数据收集web 页面
        ├── app.js
        └── index.html

```



### AWS 服务介绍

[EMR https://docs.aws.amazon.com/zh_cn/emr/?id=docs_gateway](https://docs.aws.amazon.com/zh_cn/emr/?id=docs_gateway)

[Kinesis https://docs.aws.amazon.com/zh_cn/kinesis/?id=docs_gateway](https://docs.aws.amazon.com/zh_cn/kinesis/?id=docs_gateway)

[Lambda https://docs.aws.amazon.com/zh_cn/lambda/?id=docs_gateway](https://docs.aws.amazon.com/zh_cn/lambda/?id=docs_gateway)

[DynamoDB https://docs.aws.amazon.com/zh_cn/dynamodb/?id=docs_gateway](https://docs.aws.amazon.com/zh_cn/dynamodb/?id=docs_gateway) 


###  创建EMR集群集群


[EMR 入门文档 ](https://docs.aws.amazon.com/zh_cn/emr/latest/ManagementGuide/emr-gs.html)

```
# 创建集群
aws emr create-cluster --name "Cluster with Flink" --release-label emr-5.25.0 \
--applications Name=Flink --ec2-attributes KeyName=./mykey.pem \
--instance-type m4.large --instance-count 3 --use-default-roles


#输入结果
{
    "ClusterId": "j-1YKE5B1GQZAX9"
}

```




*  创建任务

```

aws emr add-steps --cluster-id j-1YKE5B1GQZAX9  --steps Type=Flink,Name="Flink Test",ActionOnFailure=CONTINUE,Args=[--name,HelloApp,--master,yarn,--deploy-mode,client,--class,com.nwcd.solution.emr.WaterPumpApp,s3://dikers.apjc/emr/test-data/spark-1.0.jar,s3://dikers.iot/data/water_pump_log.txt]

```



* 常用命令
```


# 正在运行的任务
aws emr  list-steps --cluster-id j-27R76Z446VVBS  --step-states="RUNNING"

# 结束任务
aws emr  cancel-steps --cluster-id j-27R76Z446VVBS  --step-ids=s-LS0I0LAAQFDS

#停止集群
aws emr terminate-clusters --cluster-id j-27R76Z446VVBS

 
```