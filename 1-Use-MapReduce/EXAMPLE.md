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