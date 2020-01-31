# Databricks notebook source
# MAGIC %md In our notebook we have access to sqlContext

# COMMAND ----------

sqlContext

# COMMAND ----------

# MAGIC %md Spark Context

# COMMAND ----------

sc

# COMMAND ----------

# MAGIC %md And SparkSession

# COMMAND ----------

spark

# COMMAND ----------

# MAGIC %md We can use the Spark Context to create a small python range that will provide a return type of `DataFrame`.

# COMMAND ----------

firstDataFrame = spark.range(1000000)
print (firstDataFrame)

# COMMAND ----------

# MAGIC %md You might have expected the last command to print the values of `firstDataFrame`.  But the `range` command is a **transformation** operation, and Spark will wait until the values are needed before it calculates them.  Spark will know a value is needed when you execute an **action** operation.  
# MAGIC 
# MAGIC `show()` is an **action**:

# COMMAND ----------

firstDataFrame.show()

# COMMAND ----------

# MAGIC %md To show you the values in the DataFrame, Spark must know the values first.  When you call `show()` you force Spark to execute all the transformations needed in order to know the values in the DataFrame, and Spark will automatically do this at the right time.
# MAGIC 
# MAGIC Here are some simple examples of transformations and actions.
# MAGIC 
# MAGIC Transformations (lazy) - select, distinct, groupBy, sum, orderBy, filter, limit
# MAGIC Actions - show, count, collect, save

# COMMAND ----------

# MAGIC %md Try another transformation.  Tell Spark that we want to create a `secondDataFrame` by multiplying 2 by each value in the `firstDataFrame`.

# COMMAND ----------

# select the ID column values and multiply them by 2
secondDataFrame = firstDataFrame.selectExpr("(id * 2) as value")

# COMMAND ----------

# MAGIC %md `take` is another action.  This action selects a certain number of elements from the beginning of a dataframe.  Try to take five values from each DataFrame.

# COMMAND ----------

# take the first 5 values that we have in our firstDataFrame, use print to see the results
print (firstDataFrame.take(5))
# take the first 5 values that we have in our secondDataFrame, use print to see the results
print (secondDataFrame.take(5))

# COMMAND ----------

# MAGIC %md Spark separates operations into **transformations** (which are evaluated only when needed) and **actions** (which are evaluated immediately) to support an optimization called pipelining.  This lets you decide what you want the data to look like, while leaving it up to Spark to find the most efficient way to calculate your results.
# MAGIC 
# MAGIC ![transformations and actions](http://training.databricks.com/databricks_guide/gentle_introduction/pipeline.png)
