import json
import boto3
import base64
from boto3.dynamodb.conditions import Key

TABLE_NAME = "wordcount"
CREATE_TIME = '2019080802' #暂时固定，实际开发中根据情况获取当前小时信息

def insert_item(item):
    """
    向DynamoDB中插入单条数据
    :param item:
    :return:
    """
    print("insert item: ", item)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=item)


def query_item(create_time, word):
    """
    查询单条数据， 根据分区键和排序键进行查询
    :return: item
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key('create_time').eq(create_time) & Key('word_text').eq(word)
    )

    return response['Items']

def handle_record(records):
    """
    对单位时间的单词出现次数进行累加操作， 然后写入到DynamoDB
    """

    for i in range(len(records)):
        try:
            print('data raw    =  [',  base64.b64decode(records[i]['kinesis']['data']), ']  ' )
            print('data decode =  [', str(base64.b64decode(records[i]['kinesis']['data']) , 'utf-8'), ']  ' )
            line = str(base64.b64decode(records[i]['kinesis']['data']) , 'utf-8')
        except UnicodeDecodeError as e:
            print('except:', e)
            continue

        x = line.split(':');
        item = {}
        word_text = x[0].lstrip().rstrip()
        frequency =  int(x[1].lstrip().rstrip())
        print('word= ', word_text, '\t  frequency= ', frequency)
        item['create_time'] = CREATE_TIME
        item['word_text'] = word_text

        old_items = query_item(CREATE_TIME,word_text )

        # 累加
        if len(old_items) > 0   :
            frequency = frequency + int(old_items[0]['frequency'])

        item['frequency'] =  frequency
        insert_item(item)


def lambda_handler(event, context):
    records = event['Records'];
    print("============================= \n" , records)
    print('收到 {0}条数据 '.format(len(records)))
    handle_record(records)

    return {
        'statusCode': 200,
        'body': 'ok'
    }
