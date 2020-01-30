# Databricks notebook source
# MAGIC %md ## A Worked Example of Transformations and Actions
# MAGIC 
# MAGIC To illustrate all of these architectural and most relevantly **transformations** and **actions** - let's go through a more thorough example, this time using `DataFrames` and a csv file. 
# MAGIC 
# MAGIC Let's load the popular diamonds dataset in as a spark `DataFrame`. Now let's go through the dataset that we'll be working with.

# COMMAND ----------

dataPath = "/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv"
diamonds = sqlContext.read.format("com.databricks.spark.csv")\
  .option("header","true")\
  .option("inferSchema", "true")\
  .load(dataPath)

# COMMAND ----------

# MAGIC %md Lets get an idea what our data looks like by using the `display` function.

# COMMAND ----------

display(diamonds)

# COMMAND ----------

# MAGIC %md With DataBricks, we can easily create more sophisticated graphs by clicking the graphing icon that you can see below. Here's a plot that allows us to compare price, color, and cut.

# COMMAND ----------

display(diamonds)

# COMMAND ----------

# MAGIC %md Create several transformations and then an action:
# MAGIC * First group by two variables: cut and color
# MAGIC * Then compute the average price
# MAGIC * Then join the resulting data set to the original dataset (`diamonds`) on the column `color`
# MAGIC * Then select two variables from the new dataset: average price and carat
# MAGIC 
# MAGIC Which of these operations are transformations?  Which are actions?

# COMMAND ----------

df1 = diamonds.groupBy("cut", "color").avg("price") # a simple grouping

df2 = df1\
  .join(diamonds, on='color', how='inner')\
  .select("`avg(price)`", "carat")

# COMMAND ----------

# MAGIC %md As we have seen several times before, we don't see any results when running this command.  The operations were all transformations, and Spark is still waiting for us to request an action that requires the engine to compute the transformations.
# MAGIC 
# MAGIC This is not to say that Spark did not do any work.  In fact it did make a plan for how to compute the transformations, should the need arise.  Use the `explain` method to see this plan.

# COMMAND ----------

df2.explain()

# COMMAND ----------

# MAGIC %md The output of the plan is shown on top, while the input of the plan is shown at the bottom of each branch of the plan.  Each branch starts by reading the CSV, and applies the specified transformations.  Because we performed a join in order to create `df2`, the plan comes together, and at the very top of the plan we see the projection of `avg(price)` and `carat`.
# MAGIC 
# MAGIC Execute an action and Spark will execute this plan (Hint: try `count`)

# COMMAND ----------

df2.count()

# COMMAND ----------

# MAGIC %md This will execute the plan that Apache Spark built up previously. Click the little arrow next to where it says `(2) Spark Jobs` after that cell finishes executing and then click the `View` link. This brings up the Apache Spark Web UI right inside of your notebook. 
# MAGIC 
# MAGIC ![img](http://training.databricks.com/databricks_guide/gentle_introduction/spark-dag-ui.png)

# COMMAND ----------

# MAGIC %md ### Caching
# MAGIC 
# MAGIC One of the significant parts of Apache Spark is the ability to to store things in memory during computation. This is a neat trick that you can use as a way to speed up access to commonly queried tables or pieces of data. This is also great for iterative algorithms that work over and over again on the same data. 
# MAGIC 
# MAGIC Use the `cache` method to cache a DataFrame or RDD

# COMMAND ----------

df2.cache()

# COMMAND ----------

# MAGIC %md Caching, like a transformation, is performed lazily. It won't store the data in memory until you call an action on that dataset. 
# MAGIC 
# MAGIC Now that we have asked Spark to cache the `df2` data set, request an action to force Spark to put the dataset into memory.

# COMMAND ----------

df2.count()

# COMMAND ----------

# MAGIC %md Now count again.

# COMMAND ----------

df2.count()

# COMMAND ----------

# MAGIC %md See that the count ran much faster the second time.  Compare plans and you will notice that some steps are skipped when using the cached data.