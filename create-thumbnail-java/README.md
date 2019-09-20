# 自动生成缩略图

通过Get 方式生成缩略图



![Image](https://d2908q01vomqb2.awsstatic-china.com/472b07b9fcf2c2451e8781e944bf5f77cd8457c8/2017/09/07/a.jpg)



### 参考地址  [https://amazonaws-china.com/cn/blogs/china/image-processing-service-based-on-s3/](https://amazonaws-china.com/cn/blogs/china/image-processing-service-based-on-s3/)


[https://amazonaws-china.com/cn/blogs/china/image-processing-service-based-on-s3/](https://amazonaws-china.com/cn/blogs/china/image-processing-service-based-on-s3/)



###  mac本地 编译运行

```
mvn package
mvn spring-boot:run


mvn install
cd target
java -jar xxxx.jar -Dspring.profiles.active=prod


# 杀死进程
lsof -i tcp:8080
kill -9 id

#deploy
scp -i ~/bin/us-east-1.pem thumbnail-0.1.jar   ec2-user@ec2-54-172-59-254.compute-1.amazonaws.com:~/


```



### 登录Ec2
```
ssh -i ~/bin/us-east-1.pem     ec2-user@ec2-54-172-59-254.compute-1.amazonaws.com

```

### Ec2 上启动脚本
```
echo "kill old app"
ps -ef|grep thumbnail|grep -v grep|awk '{print $2}'|xargs kill -9

echo "start springboot "
java -jar thumbnail-0.1.jar  -Dspring.profiles.active=prod  >log.txt  &

```



--------------------------------------

# PHP  版本


###  apache + http + php 安装

(参考文档)[https://blog.csdn.net/yifan850399167/article/details/80543777]


* 新建EC2 主机 
  - 配置安全组 可以访问80端口 
  - 配置 role， 可以读写s3

登录主机执行命令

```

sudo yum -y install git httpd24 php70 ImageMagick ImageMagick-devel php70-pecl-imagick php70-pecl-imagick-devel


cd ~/
git clone https://github.com/littlehi/aws-s3-resize-image.git
ls ~/aws-s3-resize-image



```

### 修改resize.php 


**$bucketName='images.littlehi.com';**
修改s3 桶名称

**'region' => 'cn-north-1',**
修改指定region



```
$bucketName='images.littlehi.com';
$notFoundImg='404.jpg';
$src=$_GET['src'];
if(preg_match("/^(.*)_(\d+)x(\d+).([a-z]+)$/",$src,$matches)){
$objectName=$matches[1].'.'.$matches[4];
$width=$matches[2];
$height=$matches[3];
$client = new S3Client([ 'region' => 'cn-north-1', 'version' => 'latest']);
$client->registerStreamWrapper();



```
 


### 重新启动服务
```

sudo cp -r ~/aws-s3-resize-image  /var/www/html

sudo service httpd restart

```


### s3 规则配置注意事项


```
注意是s3 Endpoint的名称
Endpoint : http://bucket-name.s3-website-us-east-1.amazonaws.com/xxx.key


不是 Object URL， 否则会出现无法访问的错误
https://s3.amazonaws.com/bucket-name/xxx.key

Object URL
https://s3-ap-southeast-1.amazonaws.com/bucket-name/xxx.key

```