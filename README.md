# Learning Hadoop and Spark

### Contents

This is the companion repo to my LinkedIn Learning Courses on Hadoop and Spark.  
1. **Learning Hadoop** - [link](https://www.lynda.com/Hadoop-tutorials/Hadoop-Fundamentals/191942-2.html)  
2. **Cloud Hadoop: Scaling Apache Spark** - [link soon] - using GCP DataProc, AWS EMR or Databricks on AWS
3. **Azure Databricks Spark Essential Training** - [link](https://www.linkedin.com/learning/azure-databricks-essential-training)

### DevEnv Setup Information

- Setup a Hadoop/Spark cloud-cluster on GCP DataProc or AWS EMR
    - see `setup-hadoop` folder in this Repo for instructions/scripts
- Setup a Hadoop/Spark dev environment 
    - can use EclipseChe (on-line IDE), or local IDE
    - select your language (i.e. Python, Scala...)
- Create a GCS bucket for input/output job data
    - see `example_datasets` folder in this Repo for sample data files

### Example Jobs or Scripts

**EXAMPLES** from `org.apache.hadoop_or_spark.examples` - link for [Spark examples](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples)

- Run a Hadoop **WordCount** Job with Java (jar file)
- Run a Hadoop and/or Spark **CalculatePi** (digits) Script with PySpark or other libraries
- Run using Cloudera shared demo env 
    - at `https://demo.gethue.com/` 
    - login is user:`demo`, pwd:`demo`
---

### Other LinkedIn Learning Courses on Hadoop or Spark

There are ~ 10 courses on Hadoop/Spark topics on LinkedIn Learning.  See graphic below  
![Learning Paths](https://github.com/lynnlangit/learning-hadoop-and-spark/blob/master/images/path.png)

- **Hadoop** for Data Science Tips and Tricks - [link](https://www.linkedin.com/learning/hadoop-for-data-science-tips-tricks-techniques)
    - Set up Cloudera Enviroment
    - Working with Files in HDFS
    - Connecting to Hadoop Hive
    - Complex Data Structures in Hive
- **Spark** courses - [link](https://www.linkedin.com/learning/search?entityType=COURSE&keywords=Spark&software=Apache%20Spark~Hadoop)
    - Various Topics - see screenshot below

![LinkedInLearningSpark](https://github.com/lynnlangit/learning-hadoop-and-spark/blob/master/images/spark-courses.png)

