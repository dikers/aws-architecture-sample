# 视频自动添加字幕


### 1. 从视频中提取音频

使用MediaConvert 服务， 当视频文件转到s3中时， 调用lambda 进行音频提取

### 2. 从音频中生成文字

使用Transcript 服务， 当音频文件生成时， 调用lambda 生成srt 字幕文件


### 3. 对字幕文件进行和平

使用MediaConvert 服务， 字幕文件生成后， 和原始视频进行合并。 



### [操作步骤](https://github.com/dikers/aws-architecture-sample/blob/master/add-caption-to-video/SetupInConsole.md)
