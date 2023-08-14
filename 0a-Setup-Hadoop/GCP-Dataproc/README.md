# Verify Dataproc Setup

1. Setup a cluster
2. Run a job
3. Verify success

----

## Simple CalcPi Job

Use included sample files on default Dataproc VM image
 - create new Job
   - fill in class: `org.apache.spark.examples.SparkPi`
   - fill in path to JAR: `file:///usr/lib/spark/examples/jars/spark-examples.jar`
   - fill in arguments: `1000`
