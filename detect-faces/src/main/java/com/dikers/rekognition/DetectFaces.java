package com.dikers.rekognition;
import com.alibaba.fastjson.JSONObject;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.services.rekognition.model.*;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.AwsCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;
import software.amazon.awssdk.services.dynamodb.model.PutItemResponse;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;

import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class DetectFaces {

    String BUCKET_NAME ;
    Region REGION ;
    String DB_NAME = "DetectFaces";
    S3Client s3Client;

    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    DynamoDbClient dynamoDbClient;
    AmazonRekognition rekognitionClient ;
    ExecutorService executorService ;
    AWSStaticCredentialsProvider awsStaticCredentialsProvider;

    public DetectFaces(String accessKey, String secretKey , String bucketName, Region region ) {

        BUCKET_NAME = bucketName;

        REGION = region;
        AwsCredentials awsCreds = AwsBasicCredentials.create(accessKey, secretKey);


        awsStaticCredentialsProvider = new AWSStaticCredentialsProvider( new BasicAWSCredentials(accessKey,  secretKey));

        executorService =  Executors.newCachedThreadPool();
        s3Client = S3Client.builder()
                .credentialsProvider(StaticCredentialsProvider.create( awsCreds))
                .region(REGION)
                .build();

        dynamoDbClient = DynamoDbClient.builder().region( REGION ).credentialsProvider(StaticCredentialsProvider.create( awsCreds)).build();

        rekognitionClient = AmazonRekognitionClientBuilder.standard().withRegion( region.toString()).withCredentials(awsStaticCredentialsProvider).build();

    }

    public static void main(String[] args) throws Exception {
        if(args.length <5 ){

            System.out.println("输入参数不正确： ");
            System.out.println(" java -jar rekognition-1.0.jar accessKey secretKey bucketName region  mediaPath");
            return ;
        }

        String accessKey = args[0];
        String secretKey = args[1];
        String bucketName = args[2];
        Region region = Region.of(args[3]);
        String inputPath = args[4];


        System.out.println(" ---------- ACCESS_KEY : "+  accessKey);
        System.out.println(" ---------- SECRET_KEY : "+  secretKey);
        System.out.println(" ---------- BUCKET_NAME : "+  bucketName);
        System.out.println(" ---------- region : "+  region);
        System.out.println(" ---------- inputPath : "+  inputPath);
        DetectFaces  detectFaces = new DetectFaces(accessKey , secretKey,bucketName, region );
        detectFaces.copyImageToS3("/Users/mac/Desktop/sleep.jpg");

    }


    public void processImage(String filePath){
        executorService.submit( getThread(filePath));
    }


    /**
     * 保存图片到S3中
     * @param filePath
     */
    private void copyImageToS3(String filePath ) {
        try {

            String key =  UUID.randomUUID().toString().replace( "-", "" )+".jpg";
            PutObjectResponse putObjectResponse = s3Client.putObject( PutObjectRequest.builder().bucket(BUCKET_NAME).key(key).build(),
                    RequestBody.fromBytes(file2byte(filePath)));
            System.out.println("---------------- update ["+BUCKET_NAME+"]["+key+"] image success    " );

            getResult(key);

        } catch (Exception e) {
            e.printStackTrace();
        }

    }


    /**
     * 得到rekognition 预测结果
     * @param name
     * @throws Exception
     */
    private void getResult(String name) throws Exception{

        DetectFacesRequest request = new DetectFacesRequest()
                .withImage(new Image()
                        .withS3Object(new S3Object()
                                .withName(name)
                                .withBucket(BUCKET_NAME)))
                .withAttributes(Attribute.ALL).withRequestCredentialsProvider( awsStaticCredentialsProvider );
        // Replace Attribute.ALL with Attribute.DEFAULT to get default values.

        try {
            DetectFacesResult result = rekognitionClient.detectFaces(request);
            List < FaceDetail > faceDetails = result.getFaceDetails();


            if(faceDetails.size() == 0 ){

                System.out.println("=======【"+ (new Date( ).toString() ) +"】    没有检测到人脸 ");
                saveToDB(name );
            }

            for (FaceDetail face: faceDetails) {
//                if (request.getAttributes().contains("ALL")) {
//                    AgeRange ageRange = face.getAgeRange();
//                    System.out.println("The detected face is estimated to be between "
//                            + ageRange.getLow().toString() + " and " + ageRange.getHigh().toString()
//                            + " years old.");
//                    System.out.println("Here's the complete set of attributes:");
//                } else { // non-default attributes have null values.
//                    System.out.println("Here's the default set of attributes:");
//                }

                ObjectMapper objectMapper = new ObjectMapper();

//                System.out.println(objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(face));


                JSONObject object = JSONObject.parseObject( objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(face) );

                if(!object.getJSONObject( "eyesOpen" ).getBoolean( "value" )){

                    System.out.println("=======【"+ (new Date( ).toString() ) +"】    睡觉了  "+object.getJSONObject( "eyesOpen" ).getBigDecimal( "confidence" )+"     ");
                    System.out.println("=======  Confidence:   ");

                    saveToDB(name );

                }else {
                    System.out.println("+++++++【"+ (new Date( ).toString() ) +"】    没有睡觉  ");
                }


            }

        } catch (AmazonRekognitionException e) {
            e.printStackTrace();
        }


    }


    private  Runnable getThread(final String fileName){
        return new Runnable() {
            @Override
            public void run() {

                System.out.println("fileName:   " +fileName);
                copyImageToS3( fileName );

            }
        };
    }



    private  byte[] file2byte(String filePath)
    {
        byte[] buffer = null;
        try
        {
            File file = new File(filePath);
            FileInputStream fis = new FileInputStream(file);
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            byte[] b = new byte[1024];
            int n;
            while ((n = fis.read(b)) != -1)
            {
                bos.write(b, 0, n);
            }
            fis.close();
            bos.close();
            buffer = bos.toByteArray();
        }
        catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        return buffer;
    }


    /**
     * 保存到数据库
     * @param key
     */
    private void saveToDB(String key){


//        S3 有两种访问方式
//        saveToDB("https://s3.amazonaws.com/"+BUCKET_NAME+"/"+name );
        //TODO:  url 地址需要从S3 中返回， 这里先固定。
        String url = "https://"+BUCKET_NAME+".s3-us-west-2.amazonaws.com/"+key;


        Date currentTime = new Date();



        String createTime = simpleDateFormat.format(currentTime);

        HashMap<String, AttributeValue> item_values =
                new HashMap<String,AttributeValue>();

        //TODO:  工厂名称先固定。
        item_values.put("factoryName", AttributeValue.builder().s("factory_1").build());
        item_values.put("createTime", AttributeValue.builder().s(createTime).build());
        item_values.put("imageUrl", AttributeValue.builder().s(url).build());



        PutItemRequest request = PutItemRequest.builder()
                .tableName(DB_NAME)
                .item(item_values)
                .build();

        try {
           PutItemResponse putItemResponse =  dynamoDbClient.putItem(request);
        } catch (ResourceNotFoundException e) {
            System.err.format("Error: The table \"%s\" can't be found.\n", DB_NAME);
            System.err.println("Be sure that it exists and that you've typed its name correctly!");
        } catch (DynamoDbException e) {
            System.err.println(e.getMessage());
        }

    }

}
