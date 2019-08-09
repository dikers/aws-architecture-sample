### 数据保存Lambda


Flink 会把数据发送给 Kinesis （out_kinesis）, lambda 来接收这个kinesis 发送的数据， 
lambda 通过对单位时间的单词进行累加操作， 并且保存到DynamoBD 中。 
