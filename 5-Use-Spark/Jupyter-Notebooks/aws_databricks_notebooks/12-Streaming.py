# Databricks notebook source
# MAGIC %md # Structured Streaming
# MAGIC 
# MAGIC * Use DataFrame API to build Structured Streaming applications. 
# MAGIC * Compute real-time metrics like running counts and windowed counts on a stream of timestamped actions (e.g. Open, Close, etc).
# MAGIC * Use cluster version "Spark 2.0 (Scala 2.10)".

# COMMAND ----------

spark

# COMMAND ----------

# MAGIC %md ## Sample Data
# MAGIC We have some sample action data as files in `/databricks-datasets/structured-streaming/events/` which we are going to use to build this application. There are about 50 JSON files in the directory. Let's see an example of what each JSON file contains.

# COMMAND ----------

# MAGIC %fs head /databricks-datasets/structured-streaming/events/file-0.json

# COMMAND ----------

# MAGIC %md 
# MAGIC Each line in the file contains JSON record with two fields - `time` and `action`. Let's try to analyze these files interactively.

# COMMAND ----------

# MAGIC %md ## Batch/Interactive Processing
# MAGIC The usual first step in attempting to process the data is to interactively query the data. Let's define a static DataFrame on the files, and give it a table name.  Since we know the data format already, we can define the schema upfront to speed up processing.

# COMMAND ----------

from pyspark.sql.types import *

inputPath = "/databricks-datasets/structured-streaming/events/"

jsonSchema = StructType([ StructField("time", TimestampType(), True), StructField("action", StringType(), True) ])

staticInputDF = (
  spark
    .read
    .schema(jsonSchema)
    .json(inputPath)
)

display(staticInputDF)

# COMMAND ----------

# MAGIC %md Now we can compute the number of "open" and "close" actions with one hour windows. To do this, we will group by the `action` column and 1 hour windows over the `time` column.  We can register the results as a temp table.

# COMMAND ----------

from pyspark.sql.functions import window

staticCountsDF = (
  staticInputDF
    .groupBy(
       staticInputDF.action, 
       window(staticInputDF.time, "1 hour"))    
    .count()
)
staticCountsDF.cache()

staticCountsDF.createOrReplaceTempView("static_counts")

# COMMAND ----------

# MAGIC %md Now we can directly use SQL to query the table. For example, here are the total counts across all the hours.

# COMMAND ----------

# MAGIC %sql 
# MAGIC SELECT action, SUM(count) AS total_count 
# MAGIC FROM static_counts 
# MAGIC GROUP BY action

# COMMAND ----------

# MAGIC %md Or we can make a timeline of windowed counts.  Note the two ends of the graph. Some time passes between open actions and close actions, so there are more "opens" in the beginning and more "closes" in the end.

# COMMAND ----------

# MAGIC %sql 
# MAGIC SELECT action, date_format(window.end, "MMM-dd HH:mm") AS time, count 
# MAGIC FROM static_counts 
# MAGIC ORDER BY time, action

# COMMAND ----------

# MAGIC %md ## Stream Processing 
# MAGIC We can convert this to a streaming query that continuously updates as data comes. We can use our static set of files to emulate a real stream by reading them one at a time.  Note that we use `readStream` instead of `read` when constructing our query.
# MAGIC 
# MAGIC We use the `option` method to instruct Spark to read one file at a time, emulating a stream.  Once we have emulated the stream, the query is the same as the static query.

# COMMAND ----------

from pyspark.sql.functions import *

streamingInputDF = (
  spark
    .readStream                       
    .schema(jsonSchema)              
    .option("maxFilesPerTrigger", 1)  
    .json(inputPath)
)

streamingCountsDF = (                 
  streamingInputDF
    .groupBy(
      streamingInputDF.action, 
      window(streamingInputDF.time, "1 hour"))
    .count()
)

print ("Is this DF actually a streaming DF?", ("Yes" if streamingCountsDF.isStreaming else "No"))

# COMMAND ----------

# MAGIC %md To start streaming computation define a sink and starting it. 

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", "2") 

query = (
  streamingCountsDF
    .writeStream
    .format("memory")       
    .queryName("counts")     
    .outputMode("complete") 
    .start()
)

# COMMAND ----------

# MAGIC %md 
# MAGIC `query` is a handle to the streaming query that is running in the background. This query is continuously picking up files and updating the windowed counts. 
# MAGIC 
# MAGIC Note the status of query in the above cell. Both the `Status: ACTIVE` and the progress bar shows that the query is active. 
# MAGIC Furthermore, if you expand the `>Details` above, you will find the number of files they have already processed. 
# MAGIC 
# MAGIC Wait a few seconds for a few files to be processed and then interactively query the in-memory `counts` table. Wait a few seconds more, then run the query again.

# COMMAND ----------

# MAGIC %sql 
# MAGIC SELECT action, date_format(window.end, "MMM-dd HH:mm") AS time, count 
# MAGIC FROM counts 
# MAGIC ORDER BY time, action

# COMMAND ----------

# MAGIC %md We can also see the total number of "opens" and "closes".

# COMMAND ----------

# MAGIC %sql 
# MAGIC SELECT action, SUM(count) AS total_count 
# MAGIC FROM counts 
# MAGIC GROUP BY action 
# MAGIC ORDER BY action

# COMMAND ----------

# MAGIC %md 
# MAGIC If you don't see any updates as you re-run the queries, try restarting the streaming query.  There are only a few files and once they are all processed, there won't be any more updates in the stream.
# MAGIC 
# MAGIC Finally, you can stop the query running in the background, either by clicking on the 'Cancel' link in the cell of the query, or by executing `query.stop()`. 

# COMMAND ----------

query.stop()
