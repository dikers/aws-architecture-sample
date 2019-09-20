package com.nwcd.gallery.web;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.util.StringUtils;
import lombok.extern.slf4j.Slf4j;
import net.coobird.thumbnailator.Thumbnails;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;

/**
 * Client 控制层
 *
 * Created by bysocket on 30/09/2017.
 */
@Controller
@Slf4j
public class ClientController {


    /**
     * S3 相关配置
     */

    private static final String BUCKET = "dikers.nwcd";
    Region REGION = Region.US_EAST_1;


    @RequestMapping( value = "/resize",  method = RequestMethod.GET)
    public void client(HttpServletRequest request,
                         HttpServletResponse response,
                         @RequestParam(name = "src") String src ) {

        log.info( "resize image src ==> 【{}】 ", src );
        if (StringUtils.isNullOrEmpty( src )){
            log.info( "resize image src ==> 【{}】 为空字符，退出 ", src );
        }
        OutputStream toClient = null;
        try {
            toClient = new BufferedOutputStream(response.getOutputStream());
            ImageItem imageItem = createImageItem( src );

            byte[] buffer =createThumbnail(imageItem);


            if(buffer == null){
            }
            response.addHeader("Content-Length", "filename=" + imageItem.newName);
            response.setContentType("image/jpeg");


            toClient.write(buffer);
            toClient.flush();
            toClient.close();
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            try {
                toClient.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }



    private byte[]  createThumbnail(ImageItem imageItem){

        long start = System.currentTimeMillis();
        long tmpTime = start;
        if(imageItem == null){
            return null;
        }

        AWSCredentials credentials = null;
        try {
            credentials = new ProfileCredentialsProvider().getCredentials();
        } catch (Exception e) {
            throw new AmazonClientException(
                    "Cannot load the credentials from the credential profiles file. " +
                            "Please make sure that your credentials file is at the correct " +
                            "location (~/.aws/credentials), and is in valid format.",
                    e);
        }
        S3Client s3 = S3Client.builder().region(REGION).build();

        ByteArrayOutputStream smallStream = new ByteArrayOutputStream(  );
        ResponseInputStream<GetObjectResponse> responseInputStream = s3.getObject( GetObjectRequest.builder().bucket( BUCKET ).key( imageItem.originName ).build() );


        log.info("Get origin success.  use time: {} ms" , System.currentTimeMillis()  - tmpTime);
        tmpTime = System.currentTimeMillis();

        try {

            Thumbnails.of(responseInputStream).size( imageItem.width ,imageItem.height).keepAspectRatio(false).outputQuality(0.7f).toOutputStream(smallStream);
        } catch (IOException e) {
            e.printStackTrace();
            throw new AmazonClientException(
                    "图片压缩出错", e);
        }
        log.info("Thumbnails image success. .  use time: {} ms" , System.currentTimeMillis() - tmpTime);
        tmpTime = System.currentTimeMillis();

        byte[] result = smallStream.toByteArray().clone();
        PutObjectResponse response =  s3.putObject( PutObjectRequest.builder().bucket(BUCKET).key(imageItem.newName).build(),
                RequestBody.fromBytes( smallStream.toByteArray() )
        );
        log.info("Upload new image.  use time: {} ms" , System.currentTimeMillis() - tmpTime);

        log.info("Done!  Total use time: {} ms" , System.currentTimeMillis() - start);

        return result;

    }



    private ImageItem createImageItem(String src){

//        String src = "face_200x200.jpg";

        log.error( " createImageItem src --> 【{}】", src );

        int pos = src.lastIndexOf( "." );

        String postfix = src.substring(pos, src.length()  );

        String prefix = src.substring( 0, pos );

        if (StringUtils.isNullOrEmpty( postfix ) || StringUtils.isNullOrEmpty( prefix )
                || postfix.length()<=2 || prefix.length()<=1){
            log.error( "图片名称不正确  src --> 【{}】", src );

            return null;
        }

        pos = prefix.lastIndexOf( "_" );

        String filePostfix = prefix.substring( pos+1, prefix.length() );
        log.error("filePostfix: "+filePostfix);

        String filePrefix = prefix.substring(0, pos  );
        log.error("filePrefix: "+filePrefix);

        String originName = filePrefix+postfix;
        log.error("originName: "+originName);

        if(StringUtils.isNullOrEmpty( originName )){
            log.error( "图片名称不正确  src --> 【{}】", src );
            return null ;
        }


        if(StringUtils.isNullOrEmpty(filePostfix ) || filePostfix.length()<3){
            log.error( "图片名称不正确  src --> 【{}】", src );
            return null;
        }


        String [] sizeArr = filePostfix.split( "x" );

        if(sizeArr == null || sizeArr.length!=2){
            log.error( "图片名称不正确  src --> 【{}】", src );
            return null;
        }

        int width = Integer.valueOf( sizeArr[0] );
        int height = Integer.valueOf( sizeArr[1] );



        ImageItem imageItem = new ImageItem();
        imageItem.height = height;
        imageItem.width = width;
        imageItem.newName = src;
        imageItem.originName = originName;
        imageItem.postfix = postfix.substring(1);

        log.info(  " src  【{}】  --> {}" , src, imageItem);
        return  imageItem;

    }

    private static class ImageItem{

        int width;
        int height;
        String originName;
        String newName;
        String postfix;


        @Override
        public String toString() {
            return "ImageItem{" +
                    "width=" + width +
                    ", height=" + height +
                    ", originName='" + originName + '\'' +
                    ", newName='" + newName + '\'' +
                    ", postfix='" + postfix + '\'' +
                    '}';
        }
    }

}
