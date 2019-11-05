package com.dikers.emr.flink;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.ReduceFunction;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer;
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisProducer;
import org.apache.flink.streaming.connectors.kinesis.config.ConsumerConfigConstants;
import org.apache.flink.util.Collector;

import java.util.Properties;

/**
 * @author  dikers
 * @date  2019-08-08
 *
 * Flink + Kinesis 使用Demo
 *
 */

public class KinesisFlinkDemo {



    private static final int  DISPLAY_COUNT = 3;


    public static void main(String[] args)  throws Exception{


        System.out.println("-------------------------- start");

        if(args.length != 5){
            System.out.println("------------------- 请输入正确参数 ");
            System.out.println("args 0 ====   AWS_REGION ");
            System.out.println("args 1 ====   AWS_ACCESS_KEY_ID ");
            System.out.println("args 2 ====   AWS_SECRET_ACCESS_KEY ");
            System.out.println("args 3 ====   input kinesis name ");
            System.out.println("args 4 ====   output kinesis name ");
            return ;
        }

        String inputKinesisName  = args[3];
        String outputKinesisName  = args[4];

        System.out.println("args 3 ====   input kinesis name "+ args[3]);
        System.out.println("args 4 ====   output kinesis name " +  args[4] );

        Properties consumerConfig = new Properties();
        consumerConfig.put( ConsumerConfigConstants.AWS_REGION, args[0]);
        consumerConfig.put(ConsumerConfigConstants.AWS_ACCESS_KEY_ID, args[1]);
        consumerConfig.put(ConsumerConfigConstants.AWS_SECRET_ACCESS_KEY, args[2]);
        consumerConfig.put(ConsumerConfigConstants.STREAM_INITIAL_POSITION, "LATEST");

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<String> kinesis = env.addSource(new FlinkKinesisConsumer<>(
                inputKinesisName, new SimpleStringSchema(), consumerConfig));


        // parse the data, group it, window it, and aggregate the counts
        DataStream<WordWithCount> windowCounts = kinesis
                .flatMap(new FlatMapFunction<String, WordWithCount>() {
                    @Override
                    public void flatMap(String value, Collector<WordWithCount> out) {
                        for (String word : value.split("\\W")) {

                            if(word == null || word.trim().length() <3){
                                continue;
                            }

                            out.collect(new WordWithCount(word, 1L));
                        }
                    }
                })
                .keyBy("word")
//                .timeWindow( Time.seconds(10), Time.seconds(5))
                .countWindow(  DISPLAY_COUNT)
                .reduce(new ReduceFunction<WordWithCount>() {
                    @Override
                    public WordWithCount reduce(WordWithCount a, WordWithCount b) {

                        return new WordWithCount(a.word, a.count + b.count);
                    }
                });

        windowCounts.print().setParallelism(1);


        // 将数据sink 到kinesis 里面
        FlinkKinesisProducer<WordWithCount> flinkKinesisProducer = new FlinkKinesisProducer<>( new SerializationSchema<WordWithCount>() {
            @Override
            public byte[] serialize(WordWithCount wordWithCount) {
                System.out.println("--- sink "+ wordWithCount);
                return   wordWithCount.toString().getBytes();
            }
        }, consumerConfig );
        flinkKinesisProducer.setFailOnError(true);
        flinkKinesisProducer.setDefaultStream(outputKinesisName);
        flinkKinesisProducer.setDefaultPartition("0");
        windowCounts.addSink( flinkKinesisProducer );


        env.execute("Socket Window WordCount");



    }




    public static class WordWithCount {

        public String word;
        public long count;

        public WordWithCount() {}

        public WordWithCount(String word, long count) {
            this.word = word;
            this.count = count;
        }

        @Override
        public String toString() {
            return word + " : " + count;
        }
    }
}
