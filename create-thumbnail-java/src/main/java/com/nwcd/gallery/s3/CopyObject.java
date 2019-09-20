package com.nwcd.gallery.s3;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.util.StringUtils;
import net.coobird.thumbnailator.Thumbnails;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.UUID;

// snippet-end:[s3.java.copy_object.import]

/**
 * Copy an object from one Amazon S3 bucket to another.
 *
 * This code expects that you have AWS credentials set up per:
 * http://docs.aws.amazon.com/java-sdk/latest/developer-guide/setup-credentials.html
 */
// snippet-start:[s3.java.copy_object.main]
public class CopyObject
{
    public static void main(String[] args){


//        String object_key = "face_test.jpg";
//        String BUCKET = "dikers.nwcd";
//        AWSCredentials credentials = null;
//        try {
//            credentials = new  ProfileCredentialsProvider().getCredentials();
//        } catch (Exception e) {
//            throw new AmazonClientException(
//                    "Cannot load the credentials from the credential profiles file. " +
//                            "Please make sure that your credentials file is at the correct " +
//                            "location (~/.aws/credentials), and is in valid format.",
//                    e);
//        }
//        Region region = Region.US_EAST_1;
//        S3Client s3 = S3Client.builder().region(region).build();
//
//        ByteArrayOutputStream smallStream = new ByteArrayOutputStream(  );
//        ResponseInputStream<GetObjectResponse>  responseInputStream = s3.getObject( GetObjectRequest.builder().bucket( BUCKET ).key( "face.jpg" ).build() );
//
//        try {
//
//            Thumbnails.of(responseInputStream).size( 200,200 ).outputQuality(0.75f).toOutputStream(smallStream);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//
//        PutObjectResponse response =  s3.putObject( PutObjectRequest.builder().bucket(BUCKET).key(object_key).build(),
//                RequestBody.fromBytes( smallStream.toByteArray() )
//        );
//
//
//        System.out.println("Done!");



    }


    private static void createName(){
        String src = "face_200x200.jpg";



        int pos = src.lastIndexOf( "." );

        String postfix = src.substring(pos, src.length()  );
        System.out.println("postfix: "+postfix);

        String prefix = src.substring( 0, pos );

        if (StringUtils.isNullOrEmpty( postfix ) || StringUtils.isNullOrEmpty( prefix )
                || postfix.length()<=1 || prefix.length()<=1){


            return;
        }

        pos = prefix.lastIndexOf( "_" );

        String filePostfix = prefix.substring( pos+1, prefix.length() );
        System.out.println("filePostfix: "+filePostfix);

        String filePrefix = prefix.substring(0, pos  );
        System.out.println("filePrefix: "+filePrefix);

        String originName = filePrefix+postfix;
        System.out.println("originName: "+originName);

        if(StringUtils.isNullOrEmpty( originName )){
            return ;
        }


        if(StringUtils.isNullOrEmpty(filePostfix ) || filePostfix.length()<3){
            return ;
        }


        String [] sizeArr = filePostfix.split( "x" );

        if(sizeArr == null || sizeArr.length!=2){

            return ;
        }

        int width = Integer.valueOf( sizeArr[0] );
        int height = Integer.valueOf( sizeArr[1] );

        System.out.println( "width: "+ width + " Height: "+ height);

    }
}
 
// snippet-end:[s3.java.copy_object.main]
// snippet-end:[s3.java.copy_object.complete]
