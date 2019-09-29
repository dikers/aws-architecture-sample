from __future__ import print_function
import time
import boto3
import datetime
import urllib
import json

bucket_name = 'dikers.nwcd'
srt_prefix = 'media/srt/'
output_video_prefix = 's3://'+bucket_name+'/media/out_video/'
intput_video_prefix = 's3://'+bucket_name+'/media/input/'
lambda_base_path = '/tmp/'
media_convert_endpoint_url = 'https://vasjpylpa.mediaconvert.us-east-1.amazonaws.com'


def lambda_handler(event, context):

    audio_file_url = 's3://'+event['Records'][0]['s3']['bucket']['name']+'/'+event['Records'][0]['s3']['object']['key']
    naked_name = audio_file_url.rsplit('/', 1)[1].split('.')[0]
    srt_file_name = naked_name + '.srt'
    print('naked_name     : ', naked_name)
    print('audio_file_url : ', audio_file_url)
    print('srt_file_name  : ', srt_file_name)
    # 语音生成文本
    status = get_transcribe(audio_file_url)
    raw_content = generate_srt(status)

    # 生成字幕文件
    sentence_list = generate_srt_file(raw_content)

    file_name = lambda_base_path + srt_file_name
    key_name = srt_prefix + srt_file_name
    print('key_name  : ', key_name)
    print('file_name : ', file_name)
    # 上传字幕文件
    write_to_file(sentence_list,file_name , key_name )




    return 'ok'


def get_transcribe(audio_file_url):
    """
    通过音频文件生成 文本
    :return:
    """
    nowTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    transcribe = boto3.client('transcribe')
    job_name = "job_name_" + nowTime
    job_uri = audio_file_url

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='en-US'
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
    print(script_content['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    script_url = script_content['TranscriptionJob']['Transcript']['TranscriptFileUri']

    response = urllib.request.urlopen(script_url, timeout=30)
    data = response.read().decode()
    # print(data)
    return data


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

        temp_str += content + ' '

        if item['type'] == 'pronunciation':

            line_dict['start_time'] = item['start_time']
            line_dict['end_time'] = item['end_time']
            # print(item['start_time'], item['end_time'], content, item['type'])
            temp_list.append(line_dict)

        if content == '.' or content == '?' or content == '!' or content == ',':
            sentence_list.append(generate_sentence(temp_list, temp_str))
            temp_list = []
            temp_str = ''

    return sentence_list



def write_to_file(sentence_list , file_name, key_name):
    """

    :param sentence_list:
    :return:
    """
    print("----------- start  write to file")
    result_list = translate_text(sentence_list)
    print('===========', result_list)
    with open(file_name, 'w+') as f:
        for idx in range(len(sentence_list)):
            sentence = sentence_list[idx]
            f.write('\n')
            f.write(str(idx + 1))
            f.write('\n')
            f.write('{} --> {}\n'.format(sentence['start_time'], sentence['end_time']))
            f.write(sentence['content']+ '\n')
            f.write(str(result_list[idx]) + '\n')
            f.write('\n')

    print("-----------11 write to file success.  ")
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket_name, key_name)
    print(response)


def generate_sentence(temp_list, content_str):
    """
    生成srt 句子
    :param temp_list:
    :param content_str:
    :return:
    """
    start_time = temp_list[0]['start_time']
    end_time = temp_list[len(temp_list)-1]['end_time']
    return {'start_time': time_convert(start_time, True), 'end_time': time_convert(end_time, False), 'content': content_str}


def translate_text(item_list):
    """
    翻译文字  en --> zh
    """

    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    result_list = []
    for item in item_list:
        result = translate.translate_text(Text=item['content'],
                                          SourceLanguageCode='en', TargetLanguageCode='zh')
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
    str_temp = items[1]
    if len(str_temp) == 1:
        str_temp += '00'
    elif len(str_ms) > 3:
        str_ms = str_ms[0:3]
    elif len(str_temp) == 2:
        str_temp += '0'

    ms = int(str_temp)


    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


if __name__ == "__main__":

    raw_content = """
    {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "dikers.nwcd",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::dikers.nwcd"
        },
        "object": {
          "key": "media/out_audio/death_mp4.mp4",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}
     """
    event = json.loads(raw_content)
    lambda_handler(event, '')