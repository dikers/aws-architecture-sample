mvn clean package -Dmaven.test.skip=true
ls -la target/flink-kinese-0.1.jar
aws s3 cp target/flink-kinese-0.1.jar   s3://dikers.nwcd/emr/test-data/flink-kinese-0.1.jar
