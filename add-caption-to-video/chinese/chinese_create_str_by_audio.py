from __future__ import print_function
import time
import boto3
import datetime
import urllib
import json

# s3 桶名称
bucket_name = 'dikers.nwcd'
# 字幕文件的前缀
srt_prefix = 'media-zh/srt/'
# lambda 临时文件夹
lambda_base_path = '/tmp/'
# FIXME:
# lambda_base_path = '/Users/mac/tmp/'
language_list = ['en', 'es', 'fr']

# mediaconvert endpoint
media_convert_endpoint_url = 'https://vasjpylpa.mediaconvert.us-east-1.amazonaws.com'


def lambda_handler(event, context):
    audio_file_url = 's3://' + event['Records'][0]['s3']['bucket']['name'] + '/' + event['Records'][0]['s3']['object'][
        'key']
    naked_name = audio_file_url.rsplit('/', 1)[1].split('.')[0]

    print('naked_name     : ', naked_name)
    print('audio_file_url : ', audio_file_url)

    # 语音生成文本
    status = get_transcribe(audio_file_url)
    _content = generate_srt(status)

    # 生成字幕文件
    sentence_list = generate_srt_file(_content)

    # 上传字幕文件
    for language in language_list:

        srt_file_name = naked_name +'_'+language + '.srt'
        key_name = srt_prefix + srt_file_name
        file_name = lambda_base_path + naked_name +'_'+language + '.srt'
        print('key_name  : ', key_name)
        print('file_name : ', file_name)
        write_to_file(sentence_list, file_name, key_name, language)

    return 'ok'


def get_transcribe(audio_file_url):
    """
    通过音频文件生成 文本
    :return:
    """
    now_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    transcribe = boto3.client('transcribe')
    job_name = "job_CN_" + now_time
    job_uri = audio_file_url

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='zh-CN'
    )
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(response)
    return response


def generate_srt(script_content):
    """
    通过文本生成 srt格式文件，并且上传
    :param script_content:
    :return:
    """
    # print(script_content['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    script_url = script_content['TranscriptionJob']['Transcript']['TranscriptFileUri']

    response = urllib.request.urlopen(script_url, timeout=30)
    data = response.read().decode()
    # print(data)
    return data


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


def generate_srt_file(raw_content):
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

    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    result_list = []
    for item in item_list:
        result = translate.translate_text(Text=item['content'],
                                          SourceLanguageCode="zh", TargetLanguageCode=language)
        result_list.append(result['TranslatedText'])
        # print(item)
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

    ms = int(str_ms)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

