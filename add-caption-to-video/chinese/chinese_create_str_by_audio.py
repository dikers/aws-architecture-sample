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

# mediaconvert endpoint
media_convert_endpoint_url = 'https://vasjpylpa.mediaconvert.us-east-1.amazonaws.com'


def lambda_handler(event, context):
    audio_file_url = 's3://' + event['Records'][0]['s3']['bucket']['name'] + '/' + event['Records'][0]['s3']['object'][
        'key']
    naked_name = audio_file_url.rsplit('/', 1)[1].split('.')[0]
    srt_file_name = naked_name + '.srt'
    print('naked_name     : ', naked_name)
    print('audio_file_url : ', audio_file_url)
    print('srt_file_name  : ', srt_file_name)
    # 语音生成文本
    status = get_transcribe(audio_file_url)
    _content = generate_srt(status)

    # 生成字幕文件
    sentence_list = generate_srt_file(_content)

    file_name = lambda_base_path + srt_file_name
    # FIXME:
    # file_name = './chinese.srt'
    key_name = srt_prefix + srt_file_name
    print('key_name  : ', key_name)
    print('file_name : ', file_name)

    # 上传字幕文件
    write_to_file(sentence_list, file_name, key_name)

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
    return {'start_time': time_convert(start_time, True), 'end_time': time_convert(end_time, False),
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

    for item in items:

        line_dict = {}

        content = item['alternatives'][0]['content']
        line_dict['content'] = content



        if item['type'] == 'pronunciation':
            temp_str += content
            line_dict['start_time'] = item['start_time']
            line_dict['end_time'] = item['end_time']
            # print(item['start_time'], item['end_time'], content, item['type'])
            temp_list.append(line_dict)

        if content == '。' or content == '，' or content == ',' or content == '.':
            sentence_list.append(generate_sentence(temp_list, temp_str))
            temp_list = []
            temp_str = ''

    return sentence_list


def write_to_file(sentence_list, file_name, key_name):
    """

    :param sentence_list:
    :return:
    """
    print("----------- start  write to file")
    result_list = translate_text(sentence_list)
    print("-----------   result_list length: " , len(result_list))
    print("----------- sentence_list length: " , len(sentence_list))
    with open(file_name, 'w+', encoding='UTF-8') as f:
        for idx in range(len(sentence_list)):
            sentence = sentence_list[idx]
            print(sentence)
            f.write('\n')
            f.write(str(idx + 1))
            f.write('\n')
            f.write('{} --> {}\n'.format(sentence['start_time'], sentence['end_time']))
            f.write(str(result_list[idx])+'\n')
            f.write(sentence['content'])
            f.write('\n')
    print("----------- write to file success.  ")
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket_name, key_name)
    print(response)


def translate_text(item_list):
    """
    翻译文字  zh --> en
    """

    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    result_list = []
    for item in item_list:
        result = translate.translate_text(Text=item['content'],
                                          SourceLanguageCode="zh", TargetLanguageCode="en")
        result_list.append(result['TranslatedText'])
        # print(item)
    return result_list


def time_convert(second_str, is_start=True):
    """
    时间格式转换
    :param second_str:
    :param is_start:
    :return:
    """
    items = second_str.split('.')
    seconds = int(items[0])
    str = items[1]
    if len(str) == 1:
        str += '00'
    elif len(str) == 2:
        str += '0'

    ms = int(str)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

