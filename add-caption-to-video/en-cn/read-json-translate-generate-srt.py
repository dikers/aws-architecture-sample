import json
import boto3



# FIXME 主bucket
bucket_name = 'media.subtitle'

# FIXME global IAM, 需要translate权限
aws_access_key_id='fixme'
aws_secret_access_key='fixme'



# 原视频语言
source_language = 'en' 
# 需要翻译的语言
language_list = ['zh']
srt_prefix = 'srt/'
target_region_name = 'us-east-1'
lambda_base_path = '/tmp/'

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    transcribe = boto3.client(service_name='transcribe', endpoint_url='https://cn.transcribe.cn-northwest-1.amazonaws.com.cn')
    print(event['Records'][0])
    res = s3.get_object(Bucket=event['Records'][0]['s3']['bucket']['name'], Key=event['Records'][0]['s3']['object']['key'])
    job_name = event['Records'][0]['s3']['object']['key'].split('.')[0]
    print(job_name)
    trans_job = transcribe.get_transcription_job(TranscriptionJobName = job_name)
    audio_uri = trans_job['TranscriptionJob']['Media']['MediaFileUri']
    naked_name = audio_uri.rsplit('/', 1)[1].split('.')[0]
    _content = res['Body'].read().decode()
    sentence_list = generate_srt_file(_content, source_language != 'cn')

    # 上传字幕文件
    for language in language_list:

        srt_file_name = naked_name +'_'+language + '.srt'
        key_name = srt_prefix + srt_file_name
        file_name = lambda_base_path + naked_name +'_'+language + '.srt'
        print('key_name  : ', key_name)
        print('file_name : ', file_name)
        write_to_file(sentence_list, file_name, key_name, language)

    return 'ok'


def generate_sentence(temp_list, content_str):
    """
    生成srt 句子
    :param temp_list:
    :param content_str:
    :return:
    """
    start_time = temp_list[0]['start_time']
    end_time = temp_list[len(temp_list) - 1]['end_time']
    return {'start_time': time_convert(start_time), 'end_time': time_convert(end_time),
            'content': content_str}


def generate_srt_file(raw_content, space=False):
    """
    生成字幕srt文件
    :param raw_content:
    :return:
    """
    content_object = json.loads(raw_content)
    items = content_object['results']['items']

    sentence_list = []
    temp_list = []
    temp_str = ''

    total_count = 0
    last_str_index = 0
    for item in items:
        total_count += 1
        line_dict = {}

        content = item['alternatives'][0]['content']
        line_dict['content'] = content

        stop_flag = False
        if item['type'] == 'pronunciation':
            if space and temp_str != '' and not(content == '。' or content == '，' or content == ',' or content == '.' or content == '？' or content == '?' or stop_flag):
                temp_str += ' '
            temp_str += content
            line_dict['start_time'] = item['start_time']
            line_dict['end_time'] = item['end_time']
            # print(item, ' total_count: ', total_count)
            temp_list.append(line_dict)

            # 当单词子间相隔时间大于0.3秒， 拆分两个句子
            if total_count < len(items) and items[total_count]['type'] == 'pronunciation' \
                    and items[last_str_index]['type'] == 'pronunciation':

                _end_time = float(items[last_str_index]['end_time'])
                _start_time = float(items[total_count]['start_time'])

                if (_start_time - _end_time > 0.23 and len(temp_list)>1)  or len(temp_list) > 26:
                    stop_flag = True


        if content == '。' or content == '，' or content == ',' or content == '.' or content == '？' or content == '?' or stop_flag:
            sentence_list.append(generate_sentence(temp_list, temp_str))
            print(temp_str)
            temp_list = []
            temp_str = ''

        if item['type'] == 'pronunciation':
            last_str_index = total_count

    if len(temp_list) > 1:
        sentence_list.append(generate_sentence(temp_list, temp_str))
        temp_str = ''
        print(temp_str)



    return sentence_list


def write_to_file(sentence_list, file_name, key_name , language):
    """

    :param sentence_list:
    :return:
    """
    print("----------- start  write to [{}]  language[{}]: ".format(file_name, language))
    result_list = translate_text(sentence_list, language)
    print("-----------   result_list length: ", len(result_list))
    print("----------- sentence_list length: ", len(sentence_list))
    with open(file_name, 'w+', encoding='UTF-8') as f:
        for idx in range(len(sentence_list)):
            sentence = sentence_list[idx]
            # print(sentence)
            f.write('\n')
            f.write(str(idx + 1))
            f.write('\n')
            f.write('{} --> {}\n'.format(sentence['start_time'], sentence['end_time']))
            f.write(str(result_list[idx]) + '\n')
            f.write(sentence['content'])
            f.write('\n')
    print("----------- write to file success.  ")
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket_name, key_name)
    print('upload srt to s3: ', response)


def translate_text(item_list, language):
    """
    翻译文字  zh --> en
    """
    # 合并成一个字符串进行翻译
    # print('---- item_list: ',item_list )
    item_list_str = ''
    for item in item_list:
        item_list_str += item['content']+'\n'

    # print('---- item_list_str: ',item_list_str )
    translate = boto3.client(service_name='translate', region_name=target_region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, use_ssl=True)
    result_list = []
    result = translate.translate_text(Text=item_list_str,
                                      SourceLanguageCode=source_language, TargetLanguageCode=language)
    result_list = result['TranslatedText'].split('\n')
    print(result_list)
    return result_list


def time_convert(second_str):
    """
    时间格式转换
    :param second_str:
    :param is_start:
    :return:
    """
    items = second_str.split('.')
    seconds = int(items[0])
    str_ms = items[1]
    if len(str_ms) == 1:
        str_ms += '00'
    elif len(str_ms) == 2:
        str_ms += '0'
    elif len(str_ms) > 3:
        str_ms = str_ms[0:3]

    ms = int(str_ms)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)
