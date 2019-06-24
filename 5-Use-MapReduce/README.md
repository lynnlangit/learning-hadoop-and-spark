# learning-hadoop
Companion Repository to Learning Hadoop course on Linked In Learning

Course is here - https://www.lynda.com/Hadoop-tutorials/Hadoop-Fundamentals/191942-2.html

Examples:
-- WordCount
-- Customized WordCount (Tokenizer...)
-- Multi-file WordCount  

### How to Compile WordCount

How to...from [link](https://hadoop.apache.org/docs/r3.0.0/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)

#### Path Variables

export JAVA_HOME=/usr/java/default
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar

#### Compile it

`bin/hadoop com.sun.tools.javac.Main WordCount.java`
`jar cf wc.jar WordCount*.class`

#### Run it

Assuming that:

/user/joe/wordcount/input - input directory in HDFS
/user/joe/wordcount/output - output directory in HDFS
Sample text-files as input:

`bin/hadoop fs -ls /user/joe/wordcount/input/`
/user/joe/wordcount/input/file01
/user/joe/wordcount/input/file02

`bin/hadoop fs -cat /user/joe/wordcount/input/file01`
Hello World Bye World

`bin/hadoop fs -cat /user/joe/wordcount/input/file02`
Hello Hadoop Goodbye Hadoop

##### Run the application:

`bin/hadoop jar wc.jar WordCount /user/joe/wordcount/input /user/joe/wordcount/output`

`bin/hadoop fs -cat /user/joe/wordcount/output/part-r-00000`
Bye 1
Goodbye 1
Hadoop 2
Hello 2
World 2
