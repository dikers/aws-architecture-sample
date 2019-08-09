# Flink 作业相关



###  项目创建

```
curl https://flink.apache.org/q/quickstart.sh | bash

```


### 介绍
```
aws emr create-cluster --release-label emr-5.25.0 \
--applications Name=Flink \
--configurations file://./configurations.json \
--region us-east-1 \
--log-uri s3://myLogUri \
--instance-type m4.large \
--instance-count 2 \
--service-role EMR_DefaultRole \ 
--ec2-attributes KeyName=MyKeyName,InstanceProfile=EMR_EC2_DefaultRole \
--steps Type=CUSTOM_JAR,Jar=command-runner.jar,Name=Flink_Long_Running_Session,\
Args="flink-yarn-session -n 2 -d"


```



###  创建集群

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




### 创建任务

```

aws emr add-steps --cluster-id j-1YKE5B1GQZAX9  --steps Type=Flink,Name="Flink Test",ActionOnFailure=CONTINUE,Args=[--name,HelloApp,--master,yarn,--deploy-mode,client,--class,com.nwcd.solution.emr.WaterPumpApp,s3://dikers.apjc/emr/test-data/spark-1.0.jar,s3://dikers.iot/data/water_pump_log.txt]

```

```


# 正在运行的任务
 aws emr  list-steps --cluster-id j-27R76Z446VVBS  --step-states="RUNNING"

# 结束任务
 aws emr  cancel-steps --cluster-id j-27R76Z446VVBS  --step-ids=s-LS0I0LAAQFDS

#停止集群
aws emr terminate-clusters --cluster-id j-27R76Z446VVBS

 
```