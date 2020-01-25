## Run WordCount Apache Examples 

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

#### More Info

- the package name is `org.apache.hadoop.examples` 
- the class name is `WordCount`
- use these names when you submit the MapReduce job

#### Still More

 - review - `MR-WordCount-examples.java`
 - build - `mvn clean package` (may have to edit examples `pom.xml`)
 - verify - Once the command finishes, the wordcountjava/target directory contains a file named `wordcountjava-1.0-SNAPSHOT.jar`.

 - upload jar and run it
 - run command - `yarn jar wordcountjava-1.0-SNAPSHOT.jar org.apache.hadoop.examples.WordCount /example/data/gutenberg/davinci.txt /example/data/wordcountout`
 - review results - `hdfs dfs -cat /example/data/wordcountout/*`