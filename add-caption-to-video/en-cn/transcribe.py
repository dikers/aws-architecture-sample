import json
import boto3
import datetime
# FIXME 存放transcribe的job信息，需要修改
transcribe_job_bucket = 'transcribe.jobs'

def lambda_handler(event, context):
    transcribe = boto3.client(service_name='transcribe', endpoint_url='https://cn.transcribe.cn-northwest-1.amazonaws.com.cn')
    nowTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    job_name = "job_name_" + nowTime
    job_uri = 's3://'+event['Records'][0]['s3']['bucket']['name']+'/'+event['Records'][0]['s3']['object']['key']
    transcribe.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {'MediaFileUri': job_uri},
        MediaFormat= 'mp4',
        LanguageCode='en-US',
        OutputBucketName = transcribe_job_bucket
    )
    return 'ok'
