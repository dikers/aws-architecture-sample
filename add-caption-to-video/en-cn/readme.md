### 创建两个buckets (是否允许公开，选允许！)
1. 'transcribe.jobs' -- 与transcribe.py内的对应，存放transcribe job文件
2. 'media.subtitle' -- 与read-json-translate-generate-srt.py相对应，为主要目录桶

### 创建两个role
1. 'lambda.transcribe' -- service选Lambda，permission选AdministratorAccess
2. 'MediaConvert' -- servie选mediaConvert，copy arn到merge.py

### 创建Lambda 1
1. 修改timeout为10分钟
2. 执行role选lambda.transcribe
3. 脚本transcribe.py，按实际情况修改相应变量
4. 添加input文件夹内的mp4为执行trigger

### 创建Lambda 2
1. 修改timeout为10分钟
2. 执行role选lambda.transcribe
3. 脚本read-json-translate-generate-srt.py，按实际情况修改相应变量
4. 添加'transcribe.jobs'桶的前缀为job_name_, 后缀为.json为执行trigger

### 创建Lambda 3
1. 修改timeout为10分钟
2. 执行role选lambda.transcribe
3. 脚本merge.py，按实际情况修改相应变量
4. 添加srt文件夹内的.srt为执行trigger

## 注意：lambda的s3 trigger action选ObjectCreated就行

