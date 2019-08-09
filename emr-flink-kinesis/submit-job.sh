aws emr add-steps --cluster-id  j-AYS9XJG4XXXX \
--steps Type=CUSTOM_JAR,Name=Flink_demo,Jar=s3://dikers.apjc/emr/test-data/flink-kinese-0.1.jar