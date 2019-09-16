import json
import boto3


bucket_name = 'dikers.nwcd'

media_convert_endpoint_url = 'https://vasjpylpa.mediaconvert.us-east-1.amazonaws.com'
output_file_base_url = 's3://'+bucket_name+'/media/out_video/'
media_convert_queue_arn = 'arn:aws:mediaconvert:us-east-1:351315713712:queues/Default'
media_convert_role_arn = 'arn:aws:iam::351315713712:role/MediaConvertRole'

prefix_input_file_url   = 's3://'+bucket_name+'/media/input/'
prefix_srt_url          = 's3://'+bucket_name+'/media/srt/'
prefix_output_video_url  = 's3://'+bucket_name+'/media/out_video/'


def lambda_handler(event, context):

    print('s3://'+event['Records'][0]['s3']['bucket']['name']+'/'+event['Records'][0]['s3']['object']['key'])

    input_file = event['Records'][0]['s3']['object']['key']
    naked_file_name = input_file.rsplit("/", 1)[1].split('.')[0]
    name_split_list = naked_file_name.split('_')
    if len(name_split_list) <2:
        return 'error: 文件名字格式不正确， love_mp4.srt , 会生成love.mp4 的视频文件'

    new_video_name = name_split_list[0]+'.'+name_split_list[1]
    print(new_video_name)

    input_video_name = prefix_input_file_url+new_video_name
    output_video_name = prefix_output_video_url+name_split_list[0]
    input_srt_name = prefix_srt_url + input_file.rsplit("/", 1)[1]

    print('input_video_name     : ', input_video_name)
    print('output_video_name    : ', output_video_name)
    print('input_srt_name       : ', input_srt_name)
    merge_video(input_video_name, output_video_name, input_srt_name)
    return 'ok'


def merge_video(input_video_name, output_video_name, input_srt_name):

    client = boto3.client('mediaconvert', endpoint_url=media_convert_endpoint_url)



    response = client.create_job(

        Queue=media_convert_queue_arn,
        Role=media_convert_role_arn,
        Settings={
            "TimecodeConfig": {
                "Source": "EMBEDDED"
            },
            "Inputs": [
                {
                    "AudioSelectors": {
                        "Audio Selector 1": {
                            "Offset": 0,
                            "DefaultSelection": "DEFAULT",
                            "ProgramSelection": 1
                        }
                    },
                    "VideoSelector": {
                        "ColorSpace": "FOLLOW"
                    },
                    "FilterEnable": "AUTO",
                    "PsiControl": "USE_PSI",
                    "FilterStrength": 0,
                    "DeblockFilter": "DISABLED",
                    "DenoiseFilter": "DISABLED",
                    "TimecodeSource": "EMBEDDED",
                    "CaptionSelectors": {
                        "Captions Selector 1": {
                            "SourceSettings": {
                                "SourceType": "SRT",
                                "FileSourceSettings": {
                                    "SourceFile": input_srt_name
                                }
                            }
                        }
                    },
                    "FileInput": input_video_name
                }
            ],
            "AdAvailOffset": 0,
            "OutputGroups": [
                {
                    "Name": "File Group",
                    "Outputs": [
                        {
                            "ContainerSettings": {
                                "Container": "MP4",
                                "Mp4Settings": {
                                    "CslgAtom": "INCLUDE",
                                    "FreeSpaceBox": "EXCLUDE",
                                    "MoovPlacement": "PROGRESSIVE_DOWNLOAD"
                                }
                            },
                            "VideoDescription": {
                                "ScalingBehavior": "DEFAULT",
                                "TimecodeInsertion": "DISABLED",
                                "AntiAlias": "ENABLED",
                                "Sharpness": 50,
                                "CodecSettings": {
                                    "Codec": "H_264",
                                    "H264Settings": {
                                        "InterlaceMode": "PROGRESSIVE",
                                        "NumberReferenceFrames": 3,
                                        "Syntax": "DEFAULT",
                                        "Softness": 0,
                                        "GopClosedCadence": 1,
                                        "GopSize": 90,
                                        "Slices": 1,
                                        "GopBReference": "DISABLED",
                                        "SlowPal": "DISABLED",
                                        "SpatialAdaptiveQuantization": "ENABLED",
                                        "TemporalAdaptiveQuantization": "ENABLED",
                                        "FlickerAdaptiveQuantization": "DISABLED",
                                        "EntropyEncoding": "CABAC",
                                        "Bitrate": 3000000,
                                        "FramerateControl": "INITIALIZE_FROM_SOURCE",
                                        "RateControlMode": "CBR",
                                        "CodecProfile": "MAIN",
                                        "Telecine": "NONE",
                                        "MinIInterval": 0,
                                        "AdaptiveQuantization": "HIGH",
                                        "CodecLevel": "AUTO",
                                        "FieldEncoding": "PAFF",
                                        "SceneChangeDetect": "ENABLED",
                                        "QualityTuningLevel": "SINGLE_PASS",
                                        "FramerateConversionAlgorithm": "DUPLICATE_DROP",
                                        "UnregisteredSeiTimecode": "DISABLED",
                                        "GopSizeUnits": "FRAMES",
                                        "ParControl": "INITIALIZE_FROM_SOURCE",
                                        "NumberBFramesBetweenReferenceFrames": 2,
                                        "RepeatPps": "DISABLED",
                                        "DynamicSubGop": "STATIC"
                                    }
                                },
                                "AfdSignaling": "NONE",
                                "DropFrameTimecode": "ENABLED",
                                "RespondToAfd": "NONE",
                                "ColorMetadata": "INSERT"
                            },
                            "AudioDescriptions": [
                                {
                                    "AudioTypeControl": "FOLLOW_INPUT",
                                    "AudioSourceName": "Audio Selector 1",
                                    "CodecSettings": {
                                        "Codec": "AAC",
                                        "AacSettings": {
                                            "AudioDescriptionBroadcasterMix": "NORMAL",
                                            "Bitrate": 96000,
                                            "RateControlMode": "CBR",
                                            "CodecProfile": "LC",
                                            "CodingMode": "CODING_MODE_2_0",
                                            "RawFormat": "NONE",
                                            "SampleRate": 48000,
                                            "Specification": "MPEG4"
                                        }
                                    },
                                    "LanguageCodeControl": "FOLLOW_INPUT"
                                }
                            ],
                            "CaptionDescriptions": [
                                {
                                    "CaptionSelectorName": "Captions Selector 1",
                                    "DestinationSettings": {
                                        "DestinationType": "BURN_IN",
                                        "BurninDestinationSettings": {
                                            "TeletextSpacing": "FIXED_GRID",
                                            "Alignment": "CENTERED",
                                            "OutlineSize": 2,
                                            "ShadowColor": "NONE",
                                            "FontOpacity": 255,
                                            "FontSize": 6,
                                            "FontColor": "WHITE",
                                            "BackgroundColor": "NONE",
                                            "FontResolution": 96,
                                            "OutlineColor": "BLACK"
                                        }
                                    },
                                    "LanguageCode": "ZHO"
                                }
                            ]
                        }
                    ],
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": output_video_name
                        }
                    }
                }
            ]

        }
    )


    print(response)


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
                    "key": "media/srt/death_mp4.srt",
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