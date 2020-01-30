# Databricks notebook source
# MAGIC %md
# MAGIC In this exercise we will use Spark to explore the hypothesis stated below:
# MAGIC 
# MAGIC **The number of farmer's markets in a given zip code can be predicted from the income and taxes paid in a given area.**
# MAGIC 
# MAGIC We explore the process for discovering whether or not we can accurately predict the number of farmer's markets.  We will use two datasets.
# MAGIC 
# MAGIC ![img](http://training.databricks.com/databricks_guide/USDA_logo.png)
# MAGIC 
# MAGIC The [**Farmers Markets Directory and Geographic Data**](http://catalog.data.gov/dataset/farmers-markets-geographic-data/resource/cca1cc8a-9670-4a27-a8c7-0c0180459bef) dataset contains information on the longitude and latitude, state, address, name, and zip code of Farmers Markets in the United States. The raw data is published by the Department of Agriculture. 
# MAGIC 
# MAGIC ![img](http://training.databricks.com/databricks_guide/irs-logo.jpg)
# MAGIC 
# MAGIC The [**SOI Tax Stats - Individual Income Tax Statistics - ZIP Code Data (SOI)**](http://catalog.data.gov/dataset/zip-code-data) study provides detailed tabulations of individual income tax return data at the state and ZIP code level and is provided by the IRS. The data includes items, such as:
# MAGIC 
# MAGIC - Number of returns, which approximates the number of households
# MAGIC - Number of personal exemptions, which approximates the population
# MAGIC - Adjusted gross income
# MAGIC - Wages and salaries
# MAGIC - Dividends before exclusion
# MAGIC - Interest received

# COMMAND ----------

# MAGIC %md Read in the data
# MAGIC 
# MAGIC This data is located in in csv files and Apache Spark 2.0 can read the data in directly.

# COMMAND ----------

taxes2013 = spark.read\
  .option("header", "true")\
  .csv("dbfs:/databricks-datasets/data.gov/irs_zip_code_data/data-001/2013_soi_zipcode_agi.csv")

# COMMAND ----------

markets = spark.read\
  .option("header", "true")\
  .csv("dbfs:/databricks-datasets/data.gov/farmers_markets_geographic_data/data-001/market_data.csv")

# COMMAND ----------

# MAGIC %md Use the `display` command to take a quick look at the dataframes you created.

# COMMAND ----------

display(taxes2013)

# COMMAND ----------

# MAGIC %md Now register the DataFrames as Spark SQL tables so that we can use our SQL skills to manipulate the data. The lifetime of this temporary table is tied to the Spark Context that was used to create this DataFrame. When you shutdown the SQLContext associated with a cluster the temporary table disappears as well. 

# COMMAND ----------

taxes2013.createOrReplaceTempView("taxes2013")
markets.createOrReplaceTempView("markets")

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ## Running SQL Commands
# MAGIC 
# MAGIC This is a python notebook.  To use another language in a python notebook we prefix the cell with the language identifier.  To use SQL in your python notebook, prefix the cell with `%sql`
# MAGIC 
# MAGIC Use SQL to `show tables`.

# COMMAND ----------

# MAGIC %sql show tables

# COMMAND ----------

# MAGIC %md Take a quick look at the tables using `SELECT *`.  This is very similar to calling `display` on the DataFrame.

# COMMAND ----------

# MAGIC %sql SELECT * FROM taxes2013

# COMMAND ----------

# MAGIC %md Next, cleanup the data using SQL
# MAGIC 1. Create a new table called `cleaned_taxes` from the `taxes2013` temp table
# MAGIC 1. All the values are currently strings, convert them to approriate data types as needed
# MAGIC   1. zipcode => int
# MAGIC   1. mars1 => int
# MAGIC   1. mars2 => int
# MAGIC   1. numdep => int
# MAGIC   1. A02650 => double
# MAGIC   1. A00300 => double
# MAGIC   1. a01000 => double
# MAGIC   1. a00900 => double 
# MAGIC 1. Rename columns for clarity as needed
# MAGIC   1. state => state
# MAGIC   1. zipcode => zipcode
# MAGIC   1. mars1 => single_returns
# MAGIC   1. mars2 => joint_returns
# MAGIC   1. numdep => numdep
# MAGIC   1. A02650 => total_income_amount
# MAGIC   1. A00300 => taxable_interest_amount
# MAGIC   1. a01000 => net_capital_gains
# MAGIC   1. a00900 => biz_net_income
# MAGIC 1. Shorten each zip code to 4 digits instead of 5, to group nearby areas together

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

# MAGIC %md Now that the data is cleaned up, create some nice plots
# MAGIC 
# MAGIC Explore the average total income per zip code per state. 
# MAGIC 
# MAGIC Which states have the highest income per zip code?

# COMMAND ----------

# MAGIC %sql SELECT state, total_income_amount FROM cleaned_taxes 

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC New Jersey and California have higher average incomes per zip code.

# COMMAND ----------

# MAGIC %md Next let's explore some specifics of this particular dataset.
# MAGIC 
# MAGIC Use SQL to `describe` the dataset so that you can see the schema.

# COMMAND ----------

# MAGIC %sql describe cleaned_taxes

# COMMAND ----------

# MAGIC %md  Let's look at the set of zip codes with the lowest total capital gains and plot the results. 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT zipcode, SUM(net_capital_gains) AS cap_gains
# MAGIC FROM cleaned_taxes
# MAGIC   WHERE NOT (zipcode = 0000 OR zipcode = 9999)
# MAGIC GROUP BY zipcode
# MAGIC ORDER BY cap_gains ASC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md Let's look at a combination of capital gains and business net income to see what we find. 
# MAGIC 
# MAGIC Build a `combo` metric that represents the total capital gains and business net income by zip code. 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT zipcode,
# MAGIC   SUM(biz_net_income) as business_net_income,
# MAGIC   SUM(net_capital_gains) as capital_gains,
# MAGIC   SUM(net_capital_gains) + SUM(biz_net_income) as capital_and_business_income
# MAGIC FROM cleaned_taxes
# MAGIC   WHERE NOT (zipcode = 0000 OR zipcode = 9999)
# MAGIC GROUP BY zipcode
# MAGIC ORDER BY capital_and_business_income DESC
# MAGIC LIMIT 50

# COMMAND ----------

# MAGIC %md 
# MAGIC We can also get a peek at what will happen when we execute the query.
# MAGIC 
# MAGIC Use the `EXPLAIN` keyword in SQL.

# COMMAND ----------

# MAGIC %sql
# MAGIC EXPLAIN
# MAGIC   SELECT zipcode,
# MAGIC     SUM(biz_net_income) as net_income,
# MAGIC     SUM(net_capital_gains) as cap_gains,
# MAGIC     SUM(net_capital_gains) + SUM(biz_net_income) as combo
# MAGIC   FROM cleaned_taxes
# MAGIC   WHERE NOT (zipcode = 0000 OR zipcode = 9999)
# MAGIC   GROUP BY zipcode
# MAGIC   ORDER BY combo desc
# MAGIC   limit 50

# COMMAND ----------

# MAGIC %md We can see above that we're fetching the data from `dbfs:/user/hive/warehouse/cleaned_taxes` which is where the data is stored when we registered it as a temporary table. 
# MAGIC 
# MAGIC Let's `cache` the data 

# COMMAND ----------

# MAGIC %sql CACHE TABLE cleaned_taxes

# COMMAND ----------

# MAGIC %md When we cache data using SQL, Spark caches *eagerly*--right away.  This differs from `cacheTable` on the `SqlContext` which caches the data only when it is needed.
# MAGIC 
# MAGIC Let's run the exact same query again. You'll notice that it takes just a fraction of the time because the data is stored in memory.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT zipcode,
# MAGIC   SUM(biz_net_income) as net_income,
# MAGIC   SUM(net_capital_gains) as cap_gains,
# MAGIC   SUM(net_capital_gains) + SUM(biz_net_income) as combo
# MAGIC FROM cleaned_taxes
# MAGIC   WHERE NOT (zipcode = 0000 OR zipcode = 9999)
# MAGIC GROUP BY zipcode
# MAGIC ORDER BY combo desc
# MAGIC limit 50

# COMMAND ----------

# MAGIC %md Now `EXPLAIN` the plan 

# COMMAND ----------

# MAGIC %sql
# MAGIC EXPLAIN
# MAGIC   SELECT zipcode,
# MAGIC     SUM(biz_net_income) as net_income,
# MAGIC     SUM(net_capital_gains) as cap_gains,
# MAGIC     SUM(net_capital_gains) + SUM(biz_net_income) as combo
# MAGIC   FROM cleaned_taxes
# MAGIC   WHERE NOT (zipcode = 0000 OR zipcode = 9999)
# MAGIC   GROUP BY zipcode
# MAGIC   ORDER BY combo desc
# MAGIC   limit 50

# COMMAND ----------

# MAGIC %md 
# MAGIC Instead of going down to the source data it performs a `InMemoryColumnarTableScan`. This means that it has all of the information that it needs in memory.
# MAGIC 
# MAGIC Now let's look at the Farmer's Market Data. 
# MAGIC 
# MAGIC Start with a total summation of farmer's markets per state. 

# COMMAND ----------

# MAGIC %sql SELECT State, COUNT(State) as Sum
# MAGIC       FROM markets 
# MAGIC       GROUP BY State 