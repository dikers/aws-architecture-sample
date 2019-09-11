import json
import boto3


media_convert_endpoint_url = 'https://vasjpylpa.mediaconvert.us-east-1.amazonaws.com'
prefix_output_audio_url  = 's3://dikers.nwcd/media/out_audio/'
media_convert_queue_arn = 'arn:aws:mediaconvert:us-east-1:351315713712:queues/Default'
media_convert_role_arn = 'arn:aws:iam::351315713712:role/MediaConvertRole'

def lambda_handler(event, context):

    print(event['Records'])

    client = boto3.client('mediaconvert', endpoint_url=media_convert_endpoint_url)
    input_file = 's3://'+event['Records'][0]['s3']['bucket']['name']+'/'+event['Records'][0]['s3']['object']['key']
    name_split_list = input_file.rsplit("/", 1)[1].rsplit('.',1)
    print(name_split_list)

    if len(name_split_list) < 2:
        return '文件名称格式不正确  xx.mp4'

    output_file = prefix_output_audio_url + name_split_list[0]+'_'+name_split_list[1]

    print('input file  : ', input_file)
    print('output file : ', output_file)

    response = client.create_job(

        Queue=media_convert_queue_arn,
        Role=media_convert_role_arn,
        Settings={
            'Inputs': [
                {
                    'AudioSelectors': {
                        'Audio Selector 1': {
                            "Offset": 0,
                            'DefaultSelection': 'DEFAULT',
                            'ProgramSelection': 1
                        }
                    },

                    'VideoSelector': {
                        'ColorSpace': 'FOLLOW'
                    },
                    "FilterEnable": "AUTO",
                    "PsiControl": "USE_PSI",
                    "FilterStrength": 0,
                    "DeblockFilter": "DISABLED",
                    "DenoiseFilter": "DISABLED",
                    "TimecodeSource": "EMBEDDED",
                    'FileInput': input_file
                },
            ],
            "AdAvailOffset": 0,
            'OutputGroups': [
                {
                    'Name': 'File Group',
                    'OutputGroupSettings': {
                        'Type': 'FILE_GROUP_SETTINGS',
                        'FileGroupSettings': {
                            'Destination': output_file,
                        }

                    },
                    'Outputs': [
                        {
                            'AudioDescriptions': [
                                {
                                    'AudioSourceName': 'Audio Selector 1',
                                    'AudioTypeControl': 'FOLLOW_INPUT',
                                    'CodecSettings': {
                                        'Codec': 'AAC',
                                        'AacSettings': {
                                            'AudioDescriptionBroadcasterMix': 'NORMAL',
                                            'Bitrate': 96000,
                                            'CodecProfile': 'LC',
                                            'CodingMode': 'CODING_MODE_2_0',
                                            'RateControlMode': 'CBR',
                                            'RawFormat': 'NONE',
                                            'SampleRate': 48000,
                                            'Specification': 'MPEG4'
                                        }

                                    },
                                    'LanguageCodeControl': 'FOLLOW_INPUT',
                                },
                            ],
                            'ContainerSettings': {
                                'Container': 'MP4',
                                'Mp4Settings': {
                                    'CslgAtom': 'INCLUDE',
                                    'FreeSpaceBox': 'EXCLUDE',
                                    'MoovPlacement': 'PROGRESSIVE_DOWNLOAD'
                                }
                            }
                        },
                    ]
                },
            ]
        }
    )
    print(response)
    return 'ok'


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
                  "key": "media/input/love.mp4",
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