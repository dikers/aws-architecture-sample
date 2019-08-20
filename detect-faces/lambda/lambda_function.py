import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key

TABLE_NAME = "DetectFaces"


class DecimalEncoder(json.JSONEncoder):
    """
    json 中 整型变量转换
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        super(DecimalEncoder, self).default(o)



def query_item_list(factoryName):
    """
    获取多条数据
    :return: list
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key('factoryName').eq(factoryName)
    )
    print(response)

    result = []
    for i in range(len(response['Items'])):
        item = {}
        item['factoryName'] = response['Items'][i]['factoryName']
        item['createTime'] = response['Items'][i]['createTime']
        item['imageUrl'] =  response['Items'][i]['imageUrl']
        result.append(item)


    return result

def lambda_handler(event, context):
    response = query_item_list('factory_1')
    return response