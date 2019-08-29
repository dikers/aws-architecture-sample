package example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.s3.event.S3EventNotification;


/**
 * @author dikers
 * @date 2019-03-29
 * 实现AWS lambda服务的接口
 */

public class Application implements RequestHandler<S3EventNotification, String> {

    /**
     * Lambda 需要实现的接口
     * @param request 请求参数
     * @param context 上下文环境
     * @return
     */
    @Override
    public String handleRequest(S3EventNotification request , Context context) {

        StringBuilder stringBuilder = new StringBuilder(  );

        try {
            for (S3EventNotification.S3EventNotificationRecord record : request.getRecords()) {
                System.out.println(record.getEventSource());
                System.out.println(record.getEventName());
                System.out.println(record.getS3().getBucket().getName());
                stringBuilder.append(record.getS3().getBucket().getName()).append( "/" );
                System.out.println(record.getS3().getObject().getKey());
                stringBuilder.append(record.getS3().getObject().getKey());


                uploadImage(record.getS3().getBucket().getName() , record.getS3().getObject().getKey());
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }


        System.out.println("====: "+ stringBuilder.toString());
        return stringBuilder.toString();
    }




    public  void uploadImage(String bucketName , String key){

        S3ClientHelper s3ClientHelper = S3ClientHelper.getInstance();
        s3ClientHelper.createThumbnail(bucketName, key);



    }




}
