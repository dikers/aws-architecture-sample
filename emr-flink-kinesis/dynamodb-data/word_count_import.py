
import boto3
import time
import re

"""
将数据导入到DynamoDB中

"""

def delete_db(table_name):
    """
    删除表
    :return:
    """
    print("delete db. ", table_name)
    client = boto3.client('dynamodb')

    try:
        response = client.delete_table(
            TableName=table_name
        )
        print(response)
    except Exception:
        print("db ["+table_name+"] is not exist!")
    else:
        print("delete db success!")


# delete_db(TABLE_NAME)


def create_db(table_name, attributeDefinitions):
    """
    创建表
    :return:
    """
    print("create db. ")
    client = boto3.client('dynamodb')

    table = client.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'create_time',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'word_text',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'create_time',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'word_text',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 20
        }
    )
    # table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(table)
    print("create db success. ")


def insert_batch_item(table_name, item_list):
    """
    批量插入数据
    :param item_list:
    :return:
    """

    print("insert batch item length: ", len(item_list))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in item_list:
            batch.put_item(
                Item=item
            )


def import_data(input_file, table_name):
    """

    导入csv中的数据
    :param input_file:
    :param table_name:
    :return:
    """
    fp = open(input_file)

    line_count = 0

    attributeDefinitions = []

    item_list = []

    for line in fp:
        print(line)
        if line_count == 0:

            title_item = line.split(',')
            # print(title_item)

            for item in title_item:
                item = item[1:-1]
                title_str = item.strip('\n').strip('"')
                titles = title_str.split(' ')
                title_dic = {}
                print(titles[0], titles[1].strip('(').strip(')'))

                title_dic['AttributeName'] = titles[0]
                title_dic['AttributeType'] = titles[1]
                attributeDefinitions.append(title_dic)
        else:
            print(line_count, line)
            title_item = line.split(',')
            item_count = 0
            item_dic = {}
            for item in title_item:
                item =  re.sub('["\n]', '', item)
                item_dic[attributeDefinitions[item_count]['AttributeName']] = item
                print(attributeDefinitions[item_count]['AttributeName'], item)
                item_count = item_count + 1
            item_list.append(item_dic)

        line_count += 1
    print(attributeDefinitions)

    # delete_db(table_name)
    # time.sleep(5)

    create_db(table_name, attributeDefinitions)
    time.sleep(15)
    print(item_list)
    insert_batch_item(table_name, item_list)

    print('import success. ')



import_data('./wordcount.csv', 'wordcount')
# import_data('./data/telemetry.csv', 'telemetry')
# import_data('./data/e411.csv', 'e411')

