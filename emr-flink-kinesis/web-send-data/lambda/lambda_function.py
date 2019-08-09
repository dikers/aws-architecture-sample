import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key

TABLE_NAME = "wordcount"


class DecimalEncoder(json.JSONEncoder):
    """
    json 中 整型变量转换
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        super(DecimalEncoder, self).default(o)



def query_item_list(create_time):
    """
    获取多条数据
    :return: list
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key('create_time').eq(create_time)
    )


    result = []
    for i in range(len(response['Items'])):
        item = {}
        item['x'] = response['Items'][i]['word_text']
        item['value'] = int(response['Items'][i]['frequency'])
        item['category'] = 'type_'+str(i % 5)
        result.append(item)
    # print(result)

    return result

def lambda_handler(event, context):
    response = query_item_list('2019080802')
    return response