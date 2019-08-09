aws emr add-steps --cluster-id  j-AYS9XJG4BJCW \
--steps Type=CUSTOM_JAR,Name=Flink_wiki_edits_demo,Jar=s3://dikers.apjc/emr/test-data/wiki-edits-0.1.jar