# Verify Dataproc VM Setup

1. Setup a cluster using GCE VMs
2. Setup and Run a test Spark job
3. Verify job run success in the web ui

----

## Simple CalcPi Job

Use included sample files on default Dataproc VM image
 - create new Job
   - fill in class: `org.apache.spark.examples.SparkPi`
   - fill in path to JAR: `file:///usr/lib/spark/examples/jars/spark-examples.jar`
   - fill in arguments: `1000`
  
---

## Guidance on Migrating

From on-premise Hadoop to GCP Dataproc --> https://cloud.google.com/architecture/hadoop
