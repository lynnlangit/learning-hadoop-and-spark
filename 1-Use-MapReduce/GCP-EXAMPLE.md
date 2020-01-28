## Run WordCount on GCP Dataproc

### Create new Hadoop Job

 - MAIN class
    - needs fully-qualified name
    - case-sensitive main function
    - `org.apache.hadoop.examples.WordCount`  
 - JAR file with examples
    - examples included with base image
    - verify version of jar file
    - `file:///usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples-2.9.2.jar ` 
 - ARGS 
    - are positional `<in>`, `<out>`
    - create bucket in same project, upload data file
    - `gs://hadoop-course/shakespeare.raw`
    - `gs://hadoop-course/output`
 - NOTES
    - example includes other samples
    - source code for example jar at ...`<GitHub>`

### Hadoop Jobs

Hadoop example jobs - [hadoop-mapreduce/hadoop-mapreduce-examples.jar](https://github.com/apache/hadoop/tree/trunk/hadoop-mapreduce-project/hadoop-mapreduce-examples/src/main/java/org/apache/hadoop/examples)  

gcloud dataproc jobs submit hadoop --cluster <cluster-name> \\
  --jar file:///usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar \\
  --class org.apache.hadoop.examples.WordCount \\
  <URI of input file> <URI of output file>

### Spark Jobs
Spark example jobs - 	[spark/lib/spark-examples.jar](https://github.com/apache/spark/tree/master/examples/src/main)  

- [tutorial](https://cloud.google.com/dataproc/docs/tutorials/spark-scala) for GCP Dataproc

gcloud dataproc jobs submit spark --cluster <cluster-name> \\
  --jar file:///usr/lib/spark/lib/spark-examples.jar \\
  --class org.apache.spark.examples.JavaWordCount
  <URI of input file>