
import json
import boto3

# FIXME
bucket_name = 'media.subtitle'

# FIXME
media_convert_endpoint_url = 'https://jueykjjnc.mediaconvert.cn-northwest-1.amazonaws.com.cn'

# FIXME
media_convert_queue_arn = 'arn:aws-cn:mediaconvert:cn-northwest-1:973571775775:queues/Default'

# FIXME
media_convert_role_arn = 'arn:aws-cn:iam::973571775775:role/MediaConvert'

out_video_format = 'mp4'

prefix_input_file_url   = 's3://'+bucket_name  + '/input/'
prefix_srt_url          = 's3://'+bucket_name  + '/srt/'
prefix_output_video_url = 's3://'+bucket_name  + '/out_video/'


def lambda_handler(event, context):

    print('file name: ' ,'s3://'+event['Records'][0]['s3']['bucket']['name']+'/'+event['Records'][0]['s3']['object']['key'])

    input_file = event['Records'][0]['s3']['object']['key']
    naked_file_name = input_file.rsplit("/", 1)[1].split('.')[0]
    name_split_list = naked_file_name.split('_')
    print(name_split_list)
    if len(name_split_list) <2:
        return 'error: 文件名字格式不正确， love_mp4_en.srt , 会生成love.mp4 的视频文件'

    # 生成新的 video name
    new_video_name = naked_file_name+'.'+out_video_format
    print(new_video_name)

    nake_name = name_split_list[0]+'.'+out_video_format

    input_video_name = prefix_input_file_url+nake_name
    output_video_name = prefix_output_video_url+new_video_name
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
                                            "FontSize": 8,
                                            "FontColor": "WHITE",
                                            "BackgroundColor": "NONE",
                                            "FontResolution": 200,
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