package com.dikers.media;


import com.dikers.rekognition.DetectFaces;
import org.bytedeco.javacpp.*;
import org.bytedeco.javacv.*;
import software.amazon.awssdk.regions.Region;

import javax.swing.*;

public  class MediaConvert {


    private final static int RECORD_IMAGE_COUNT = 30;  //  30/5  6秒发一张图
    private final static int CAMERA_INTERVAL = 200 ;  //一秒5张图
    public static String ACCESS_KEY = "";
    public static String SECRET_KEY = "";
    public static String BUCKET_NAME = "";
    public static String inputPath = "";
    public static String inputImagePath = "";

    static Region mRegion ;



    public static void main(String[] args) throws Exception {

        if(args.length < 6 ){

            System.out.println("输入参数不正确： ");
            System.out.println(" ---------- accessKey secretKey bucketName region  mediaPath  imagePath ");
            return ;
        }

        ACCESS_KEY = args[0];
        SECRET_KEY = args[1];
        BUCKET_NAME = args[2];
        mRegion = Region.of(args[3]);
        inputPath = args[4];
        inputImagePath = args[5];


        System.out.println(" ---------- ACCESS_KEY : "+  ACCESS_KEY);
        System.out.println(" ---------- SECRET_KEY : "+  SECRET_KEY);
        System.out.println(" ---------- BUCKET_NAME : "+  BUCKET_NAME);
        System.out.println(" ---------- region : "+  mRegion);
        System.out.println(" ---------- inputPath : "+  inputPath);


        recordCamera(inputPath , 10);
    }



    /** 按帧录制本机摄像头视频（边预览边录制，停止预览即停止录制）
     *
     * @author eguid
     * @param outputFile -录制的文件路径，也可以是rtsp或者rtmp等流媒体服务器发布地址
     * @param frameRate - 视频帧率
     * @throws Exception
     * @throws InterruptedException
     * @throws FrameRecorder.Exception
     */
    public static void recordCamera(String outputFile, double frameRate)
            throws Exception, InterruptedException, FrameRecorder.Exception {
        Loader.load( opencv_objdetect.class);

        DetectFaces detectFaces = new DetectFaces(ACCESS_KEY, SECRET_KEY, BUCKET_NAME , mRegion);

        FrameGrabber grabber = FrameGrabber.createDefault(0);//本机摄像头默认0，这里使用javacv的抓取器，至于使用的是ffmpeg还是opencv，请自行查看源码
        grabber.start();//开启抓取器

        OpenCVFrameConverter.ToIplImage converter = new OpenCVFrameConverter.ToIplImage();//转换器
        opencv_core.IplImage grabbedImage = converter.convert(grabber.grab());//抓取一帧视频并将其转换为图像，至于用这个图像用来做什么？加水印，人脸识别等等自行添加
        int width = grabbedImage.width();
        int height = grabbedImage.height();

        FrameRecorder recorder = FrameRecorder.createDefault(outputFile, width, height);
        recorder.setVideoCodec( avcodec.AV_CODEC_ID_H264); // avcodec.AV_CODEC_ID_H264，编码
        recorder.setFormat("flv");//封装格式，如果是推送到rtmp就必须是flv封装格式
        recorder.setFrameRate(frameRate);

        recorder.start();//开启录制器
        long startTime=0;
        long videoTS=0;
        int imageCount = 1;
        CanvasFrame frame = new CanvasFrame("camera", CanvasFrame.getDefaultGamma() / grabber.getGamma());
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE);
        frame.setAlwaysOnTop(true);
        Frame rotatedFrame=converter.convert(grabbedImage);//不知道为什么这里不做转换就不能推到rtmp
        while (frame.isVisible() && (grabbedImage = converter.convert(grabber.grab())) != null) {
            rotatedFrame = converter.convert(grabbedImage);
            frame.showImage(rotatedFrame);
            if (startTime == 0) {
                startTime = System.currentTimeMillis();
            }
            videoTS = 1000 * (System.currentTimeMillis() - startTime);
            recorder.setTimestamp(videoTS);
            recorder.record(rotatedFrame);

            frame.showImage(grabber.grab());//获取摄像头图像并放到窗口上显示， 这里的Frame frame=grabber.grab(); frame是一帧视频图像

            if(imageCount % RECORD_IMAGE_COUNT == 0){
                opencv_core.Mat mat = converter.convertToMat(grabber.grabFrame());
                String fileName =  inputImagePath + imageCount + ".jpg";
                opencv_imgcodecs.imwrite(fileName, mat);
                detectFaces.processImage( fileName );
            }
            imageCount++;

            Thread.sleep(CAMERA_INTERVAL);
        }
        frame.dispose();
        recorder.stop();
        recorder.release();
        grabber.stop();

    }


}