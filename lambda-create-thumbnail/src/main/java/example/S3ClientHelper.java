package example;

import net.coobird.thumbnailator.Thumbnails;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * @date 2019-08-30
 * @author nwcd
 *
 */
public class S3ClientHelper {

    /**
     * 在 lambda 环境变量里面设置
     */
    //FIXME:  不能设置环境变量， 可以从s3中读取。
//    private static final String sRegionName = System.getenv( "region_name" );
    private static final String sRegionName = "cn-northwest-1";
    /**
     *
     * 用分号和逗号进行分割,例如下面的示例， 根据这几组数字进行缩放
     * 300,200;600,400
     *
     */
    //FIXME:  不能设置环境变量， 可以从s3中读取。
//    private static final String sImageSizeConfig = System.getenv( "image_size_config" );
    private static final String sImageSizeConfig = "300,200;600,400";


    private List<ImageSize> imageSizeList;
    private  Region region;
    private  S3Client s3Client;

    private static class LazyHolder {

        private static final S3ClientHelper HELPER_INSTANCE = new S3ClientHelper();
    }


    private S3ClientHelper() {
        System.out.println("=============== S3ClientHelper  init ========= ");
        System.out.println("region_name             :" + sRegionName);
        System.out.println("sImageSizeConfig        :" + sImageSizeConfig);
        region =  Region.of(sRegionName);
        s3Client = S3Client.builder()
                .region(region)
                .build();


        imageSizeList = new ArrayList<>(  );

        String [] items = sImageSizeConfig.split( ";" );
        for(String str: items){
            ImageSize imageSize = new ImageSize( str );
            imageSizeList.add( imageSize );
        }

    }

    public static final S3ClientHelper getInstance() {
        return LazyHolder.HELPER_INSTANCE;
    }



    public  void createThumbnail(String bucketName ,String key) {

        String lowStr = key.toLowerCase();
        if(!lowStr.endsWith(Config.IMAGE_TYPE_JPG )
                &&  !lowStr.endsWith( Config.IMAGE_TYPE_JPEG )
                && !lowStr.endsWith(Config.IMAGE_TYPE_PNG )){
            System.out.println(" ------ 不需要生成缩略图 return   key: "+key );
            return ;
        }


        for(ImageSize imageSize:  imageSizeList){
            doCreate( bucketName, key, imageSize.width, imageSize.height );
        }



    }

    /**
     * 生成缩略图
     * @param bucketName
     * @param key
     * @param width
     * @param height
     */
    private void doCreate(String bucketName, String key, int width, int height) {
        String  suffixKey = getSuffixKey(width,height);
        String newKey = key + suffixKey;


        System.out.println("create thumbnail new key: "+ newKey);
        GetObjectRequest getObjectRequest = GetObjectRequest.builder()
                .bucket(bucketName).key( key )
                .build();
        ResponseInputStream responseInputStream = s3Client.getObject(getObjectRequest);


        ByteArrayOutputStream outStream = new ByteArrayOutputStream(  );
        try {

            Thumbnails.of(responseInputStream).size( width,height ).keepAspectRatio( false ).toOutputStream(outStream);
        } catch (IOException e) {
            e.printStackTrace();
            return ;
        }

        PutObjectResponse response =  s3Client.putObject( PutObjectRequest.builder().bucket(bucketName)
                        .key(newKey).build(),
                RequestBody.fromBytes( outStream.toByteArray() )
        );


        System.out.println(response);
    }


    /**
     * 生成文件后缀
     * @param width
     * @param height
     * @return
     */
    private  String getSuffixKey(int width, int height){
        return "_"+width+"x"+height ;
    }


    private class ImageSize{

        int width;
        int height;

        public ImageSize(String configStr) {

            String [] item = configStr.split( "," );
            width = Integer.valueOf( item[0] );
            height = Integer.valueOf( item[1] );
        }
    }

}
