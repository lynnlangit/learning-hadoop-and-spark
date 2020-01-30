// Databricks notebook source
dbutils.fs.put("/home/spark/1.6/lines","""
Hello hello world
Hello how are you world
""", true)

// COMMAND ----------

import org.apache.spark.sql.functions._

// Load a text file and interpret each line as a java.lang.String
val ds = sqlContext.read.text("/home/spark/1.6/lines").as[String]
val result = ds
  .flatMap(_.split(" "))               // Split on whitespace
  .filter(_ != "")                     // Filter empty words
  .toDF()                              // Convert to DataFrame to perform aggregation / sorting
  .groupBy($"value")                   // Count number of occurences of each word
  .agg(count("*") as "numOccurances")
  .orderBy($"numOccurances" desc)      // Show most common words first

display(result)
