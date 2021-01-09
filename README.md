# Learning Hadoop and Spark

## Contents

This is the companion repo to my LinkedIn Learning Courses on Hadoop and Spark.  
1. **Learning Hadoop** - [link](https://www.linkedin.com/learning/learning-hadoop-2) uses mostly GCP Dataproc for running Hadoop and associated libraries (i.e. Hive, Pig, Spark...) workloads
2. **Cloud Hadoop: Scaling Apache Spark** - [link](https://www.linkedin.com/learning/cloud-hadoop-scaling-apache-spark) - uses GCP DataProc, AWS EMR or Databricks on AWS
3. **Azure Databricks Spark Essential Training** - [link](https://www.linkedin.com/learning/azure-databricks-essential-training) uses Azure with Databricks for scaling Apache Spark workloads

---

## Development Environment Setup Information

You have a number of options - although it is possible for you to set up a local Hadoop/Spark cluster, I do NOT recommended this approach as it's needlessly complex for initial study.  Rather I do recommend that you use a partially or fully-managed cluster.  For learning, I most often use a **fully-managed (free tier) cluster**.  

### Databricks

<img src="https://github.com/lynnlangit/learning-hadoop-and-spark/blob/master/images/word-count-databricks.png" width=600 align=left>
    
- **1. FULLY-MANAGED** - Use Databricks Community Edition (managed, hosted Apache Spark) - example screenshot shown to the left
    - use **Databrick AWS community** edition (simplest set up - free tier on AWS) - [link](https://databricks.com/try-databricks) --or--
    - use **Databrick Azure trial** edition - TIP: it's simpler to try out on AWS free tier, Azure may require a pay-as-you-go account to get needed CPU/GPU resources
    - uses Databricks (Jupyter-style) notebooks to connect to a small, managed Spark cluster
    - creates and manages your data file buckets as part of Databricks service (on either AWS S3 or Azure Blob store)

---

### PaaS Cloud

- **2. PARTIALLY-MANAGED** - Setup a Hadoop/Spark managed cloud-cluster on GCP or AWS
    - see `setup-hadoop` folder in this Repo for instructions/scripts
        - create a GCS (or AWS) **bucket** for input/output job data
        - see `example_datasets` folder in this Repo for sample data files
    - for **GCP use DataProc** w/ Jupyter notebook interface --OR--
    - for **AWS use EMR** you can use EMR Studio (which includes managed Jupyter instances) - [link](https://aws.amazon.com/blogs/big-data/amazon-emr-studio-preview-a-new-notebook-first-ide-experience-with-amazon-emr/) example screenshot shown below
    
<img src="https://github.com/lynnlangit/learning-hadoop-and-spark/blob/master/images/emr-studio.png" width=800 align=right>
    
- **3. MANUAL** - Setup Hadoop/Spark locally or on a 'raw' cloud VM, such as AWS EC2
    - NOT RECOMMENDED for learning - too complex to set up
    - Cloudera Learning VM - also NOT recommended, changes too often, documentation not aligned

---
 
## Example Jobs or Scripts

**EXAMPLES** from `org.apache.hadoop_or_spark.examples` - link for [Spark examples](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples)

- Run a Hadoop **WordCount** Job with Java (jar file)
- Run a Hadoop and/or Spark **CalculatePi** (digits) Script with PySpark or other libraries
- Run using Cloudera shared demo env 
    - at `https://demo.gethue.com/` 
    - login is user:`demo`, pwd:`demo`
---

## Other LinkedIn Learning Courses on Hadoop or Spark

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

