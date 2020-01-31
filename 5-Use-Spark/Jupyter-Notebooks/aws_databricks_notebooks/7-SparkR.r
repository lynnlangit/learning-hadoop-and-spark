# Databricks notebook source
# MAGIC %md # SparkR Overview
# MAGIC 
# MAGIC SparkR is an R package that provides a light-weight frontend to use Apache Spark from R. 
# MAGIC 
# MAGIC The simplest way to create a DataFrame is to convert a local R data frame into a SparkR DataFrame. The following cell creates a DataFrame using the faithful dataset from R.

# COMMAND ----------

library(SparkR)
df <- createDataFrame(faithful)

# Displays the content of the DataFrame to stdout
head(df)

# COMMAND ----------

# MAGIC %md # Read Data Sources using Spark SQL
# MAGIC 
# MAGIC You can create DataFrames from stored data such as CSV and JSON using `read.df`.  
# MAGIC 
# MAGIC This method takes in the SQLContext, the path for the file to load and the type of data source. SparkR supports reading JSON and Parquet files natively and through Spark Packages you can find data source connectors for popular file formats like CSV and Avro.
# MAGIC 
# MAGIC You can also use `display` to format the loaded data frame.

# COMMAND ----------

markets <- read.df("dbfs:/databricks-datasets/data.gov/farmers_markets_geographic_data/data-001/market_data.csv", "com.databricks.spark.csv", header="true", inferSchema="true")
display(markets)

# COMMAND ----------

# MAGIC %md `read.df` attempted to infer the schmea for the CSV data.
# MAGIC 
# MAGIC use `printSchema` to show the schema for `markets`

# COMMAND ----------

printSchema(markets)

# COMMAND ----------

# MAGIC %md You can also load data from Spark SQL tables.  First load some data into a temp table.

# COMMAND ----------

taxes2013 <- read.df("dbfs:/databricks-datasets/data.gov/irs_zip_code_data/data-001/2013_soi_zipcode_agi.csv","com.databricks.spark.csv", header="true", inferSchema="true")
createOrReplaceTempView(taxes2013, "taxes2013")

# COMMAND ----------

# MAGIC %md Next cleanup the data and store in a persistent table.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS cleaned_taxes;
# MAGIC 
# MAGIC CREATE TABLE cleaned_taxes AS
# MAGIC SELECT 
# MAGIC   state, 
# MAGIC   int(zipcode / 10) as zipcode,
# MAGIC   int(mars1) as single_returns,
# MAGIC   int(mars2) as joint_returns,
# MAGIC   int(numdep) as numdep,
# MAGIC   double(A02650) as total_income_amount,
# MAGIC   double(A00300) as taxable_interest_amount,
# MAGIC   double(a01000) as net_capital_gains,
# MAGIC   double(a00900) as biz_net_income
# MAGIC FROM taxes2013

# COMMAND ----------

# MAGIC %md Finally, load the data into a dataframe using the persistent table as a source.

# COMMAND ----------

taxes <- sql("SELECT * FROM cleaned_taxes")
display(taxes)

# COMMAND ----------

# MAGIC %md Let's revist the `faithful` dataset.
# MAGIC 
# MAGIC `select` the `eruptions` column from `df`.  Store the result in `eruptions`.
# MAGIC 
# MAGIC Use `head` to show `eruptions`.

# COMMAND ----------

eruptions <- select(df, df$eruptions)

head(eruptions)

# COMMAND ----------

# MAGIC %md You can also specify the column name using a string.

# COMMAND ----------

eruptions2 <- select(df, "eruptions")
head(eruptions)

# COMMAND ----------

# MAGIC %md You can `filter` a dataset too.
# MAGIC 
# MAGIC Use `filter` to show only the rows where `waiting` is less than 50.  Store the results in `waiting`.
# MAGIC 
# MAGIC Show `waiting`.

# COMMAND ----------

waiting <- filter(df, df$waiting < 50)
display(waiting)

# COMMAND ----------

# MAGIC %md Next group `df` by "waiting" and count the occurrences of each waiting period.
# MAGIC 
# MAGIC Store the results in `waiting_counts` and show `waiting_counts`.

# COMMAND ----------

waiting_counts <- count(groupBy(df, df$waiting))
display(waiting_counts)

# COMMAND ----------

# MAGIC %md Display the most common waiting times using `head`.
# MAGIC 
# MAGIC First `arrange` the `waiting_times` dataframe in descending order by count.  Store the results in `sorted_waiting_times`, then use `head` to show the most common.

# COMMAND ----------

sorted_waiting_times <- arrange(waiting_counts, desc(waiting_counts$count))
head(sorted_waiting_times)

# COMMAND ----------

# MAGIC %md You can apply a transformation to a column, then assign the result back to a new column on the same dataframe.
# MAGIC 
# MAGIC Tranform `waiting` to `waiting_seconds` and store the result as a new column on `sorted_waiting_times`.  Show `sorted_waiting_times`.

# COMMAND ----------

sorted_waiting_times$waiting_seconds <- sorted_waiting_times$waiting * 60
display(sorted_waiting_times)

# COMMAND ----------

# MAGIC %md Finally we can access Spark MLLib easily from R.  Let's load the `iris` dataset and build a linear regression model.

# COMMAND ----------

iris_data <- createDataFrame(iris)

model <- glm(Sepal_Length ~ Sepal_Width + Species, data = iris_data, family = "gaussian")

summary(model)

# COMMAND ----------


