mvn clean package -Dmaven.test.skip=true
ls -la target/wiki-edits-0.1.jar
aws s3 cp target/wiki-edits-0.1.jar   s3://dikers.apjc/emr/test-data/wiki-edits-0.1.jar