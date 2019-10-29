import json
import boto3
import random
import datetime

kinesis = boto3.client('kinesis')

def lambda_handler(event, context):


    data = event['word']
    print('接收到前端消息[{0}] . '.format(data))
    kinesis.put_record(
        StreamName="testKinesis",
        Data=data,
        PartitionKey="partitionkey")

    return {
        'statusCode': 200,
        'body': 'OK'
    }




