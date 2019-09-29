package com.dikers.media;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.UUID;
import java.util.logging.Logger;

public class FFMpegUtil {



//    https://qtdebug.com/ffmpeg/

    // ffmpeg命令所在路径
    private static final String FFMPEG_PATH = "/bin/ffmpeg";
    // ffmpeg处理后的临时文件
    private static final String TMP_PATH = "/Users/mac/Downloads";
    // home路径
    private static final String HOME_PATH;

    static {
        HOME_PATH = System.getProperty("user.home");
        System.out.println("static home path : " + HOME_PATH);
    }

    /**
     * 视频转音频
     * @param videoUrl
     */
    public static String videoToAudio(String videoUrl){
        String aacFile = "";
        try {
            aacFile = TMP_PATH + "/" + new SimpleDateFormat("yyyyMMddHHmmss").format(new Date())
                    + UUID.randomUUID().toString().replaceAll("-", "") + ".mp3";
//            ffmpeg -i ~/Desktop/love.mp4  -vn -acodec mp3  ~/tmp/test.mp3
            String command = HOME_PATH + FFMPEG_PATH + " -i "+ videoUrl + " -vn -acodec mp3 "+ aacFile;
            System.out.println("video to audio command : " + command);
            Process process = Runtime.getRuntime().exec(command);
            process.waitFor();
        } catch (Exception e) {
            System.out.println("视频转音频失败，视频地址："+videoUrl+ e);
        }
        return "";
    }

    /**
     * 将字幕烧录至视频中
     * @param videoUrl
     */
    public static String burnSubtitlesIntoVideo(String videoUrl, File subtitleFile){
        String burnedFile = "";
        File tmpFile = null;
        try {
            burnedFile = TMP_PATH + "/" + new SimpleDateFormat("yyyyMMddHHmmss").format(new Date())
                    + UUID.randomUUID().toString().replaceAll("-", "") + ".mp4";
            String command = HOME_PATH + FFMPEG_PATH + " -i "+ videoUrl + " -vf subtitles="+ subtitleFile +" "+ burnedFile;
            System.out.println("burn subtitle into video command : " + command);
            Process process = Runtime.getRuntime().exec(command);
            process.waitFor();
        } catch (Exception e) {
            System.out.println("视频压缩字幕失败，视频地址："+videoUrl+",字幕地址："+videoUrl + e);
        }
        return "";
    }


    public static void main(String[] args) {
//        videoToAudio( "/Users/mac/Desktop/love.mp4" );


        burnSubtitlesIntoVideo("/Users/mac/Desktop/aws_2.mp4", new File( "/Users/mac/Desktop/aws_2_mp4.srt" ));
    }

}