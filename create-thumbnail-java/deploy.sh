
mvn clean install
echo "-------- deploy to ec2 --------"
scp -i ~/bin/us-east-1.pem  ./target/thumbnail-0.1.jar   ec2-user@ec2-54-172-59-254.compute-1.amazonaws.com:~/


