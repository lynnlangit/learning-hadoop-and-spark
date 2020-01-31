# Databricks notebook source
# MAGIC %md ## Apache Spark MLLib
# MAGIC Let's return to the farmer's market dataset and use Spark to explore the hypothesis:
# MAGIC * The number of farmer's markets in a given zip code can be predicted from the income and taxes paid in a given area.
# MAGIC 
# MAGIC There are serveral steps to this process:
# MAGIC 1. **Part One - Load and prepare the data** 
# MAGIC   * Verify and/or load table data
# MAGIC   * Prepare the data by aggregating, grouping and counting table data values
# MAGIC   * Join data from the prepared tables
# MAGIC   * Convert 'null' values in the joined data to '0'
# MAGIC 2. **Part Two - Use the Spark ML Library**
# MAGIC   * Create and display a vector with the the features you'd like to explore in a scatterplot
# MAGIC   * Split the dataset into testing and training sets, cache both and call an action to load the cache
# MAGIC   * Create a linear regression model and fit the model with your training data
# MAGIC   * Use your model by calling predict on it
# MAGIC   * Evaluate and update your model  
# MAGIC   * Train and use the most optimal model

# COMMAND ----------

# MAGIC %md ### Part One - Load and Prepare the data 
# MAGIC * Load the table `cleaned_taxes` into a dataframe (created in previous exercise) 

# COMMAND ----------

cleanedTaxes = sqlContext.sql("SELECT * FROM cleaned_taxes")
cleanedTaxes.show()

# COMMAND ----------

# MAGIC %md NOTE: If the table did NOT load, then run the next couple of cells to re-load the data.

# COMMAND ----------

# taxes2013 = spark.read\
#   .option("header", "true")\
#   .csv("dbfs:/databricks-datasets/data.gov/irs_zip_code_data/data-001/2013_soi_zipcode_agi.csv")
# taxes2013.createOrReplaceTempView("taxes2013")

# COMMAND ----------

# %sql
# DROP TABLE IF EXISTS cleaned_taxes;

# CREATE TABLE cleaned_taxes AS
# SELECT 
#   state, 
#   int(zipcode / 10) as zipcode,
#   int(mars1) as single_returns,
#   int(mars2) as joint_returns,
#   int(numdep) as numdep,
#   double(A02650) as total_income_amount,
#   double(A00300) as taxable_interest_amount,
#   double(a01000) as net_capital_gains,
#   double(a00900) as biz_net_income
# FROM taxes2013

# COMMAND ----------

# MAGIC %md * Load the market dataset to a permanent table named `markets`

# COMMAND ----------

markets = spark.read\
  .option("header", "true")\
  .csv("dbfs:/databricks-datasets/data.gov/farmers_markets_geographic_data/data-001/market_data.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC * Use `sum` to aggreggate all the columns in the `cleanedTaxes` dataset -- NOTE: Some data will be nonsense (i.e.summing zipcode) but other data could become useful features (i.e. summing AGI in the zipcode).
# MAGIC * Group the `cleanedTaxes` dataframe by zipcode, then `sum` to aggregate across all columns. 
# MAGIC * Save the resulting dataframe in `summedTaxes`
# MAGIC * `show` the `summedTaxes` dataframe 

# COMMAND ----------

summedTaxes = cleanedTaxes\
  .groupBy("zipcode")\
  .sum()
  
summedTaxes.show()

# COMMAND ----------

# MAGIC %md Group the market data into buckets and count the number of farmer's markets in each bucket.
# MAGIC 
# MAGIC * Use `selectExpr` to transform the market data into labels that identify which zip group they belong to (we used `int(zip/10)` to group the tax data) call the new value `zipcode`.  `selectExpr` is short for "Select Expression" and can process similar operations to SQL statements.
# MAGIC * Group by the `zipcode` you just created, then `count` the groups.
# MAGIC * Use another `selectExpr` to transform the data, you only need to keep the `count` and the `zipcode as zip`.
# MAGIC * Store the results in a new dataset called `cleanedMarkets`.
# MAGIC * `show` `cleanedMarkets` 

# COMMAND ----------

cleanedMarkets = markets\
  .selectExpr("*", "int(zip / 10) as zipcode")\
  .groupBy("zipcode")\
  .count()\
  .selectExpr("double(count) as count", "zipcode as zip")

cleanedMarkets.show()

# COMMAND ----------

# MAGIC %md Join the two cleaned datasets into one dataset for analysis.
# MAGIC 
# MAGIC * Outer join `cleanedMarkets` to `summedTaxes` using `zip` and `zipcode` as the join variable.
# MAGIC * Name the resulting dataset `joined`.

# COMMAND ----------

joined = cleanedMarkets\
  .join(summedTaxes, cleanedMarkets["zip"] == summedTaxes["zipcode"], "outer")

# COMMAND ----------

# MAGIC %md  * `display` the `joined` data - do you see the 'null' values?

# COMMAND ----------

display(joined)

# COMMAND ----------

# MAGIC %md MLLib doesn't allow null values.  These values came up as `null` in the join because there were no farmer's markets in that zip code "basket".  It makes sense to replace the `null` values with zeros.
# MAGIC * Use the `na` prefix to `fill` the empty cells with `0`.
# MAGIC * Name the resulting dataset `prepped` and `display` it.

# COMMAND ----------

prepped = joined.na.fill(0)
display(prepped)

# COMMAND ----------

# MAGIC %md ### Part Two -Use MLLib with Spark
# MAGIC * Put all the features into a single vector.  
# MAGIC * Create an array to list the names of all the **non-feature** columns: `zip`, `zipcode`, `count`, call it `nonFeatureCols`.
# MAGIC * Create a list of names called `featureCols` which excludes the columns in `nonFeatureCols`.
# MAGIC * `print` the `featureCols`.

# COMMAND ----------

nonFeatureCols = {'zip', 'zipcode', 'count'}
featureCols = [column for column in prepped.columns if column not in nonFeatureCols]
print(featureCols)

# COMMAND ----------

# MAGIC %md * Use the `VectorAssembler` from `pyspark.ml.feature` to add a `features` vector to the `prepped` dataset.
# MAGIC * Call the new dataset `finalPrep`, then `display` only the `zipcode` and `features` from `finalPrep`.

# COMMAND ----------

from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=[column for column in featureCols],
    outputCol='features')

finalPrep = assembler.transform(prepped)
display(finalPrep.select('zipcode', 'features'))

# COMMAND ----------

# MAGIC %md * Display the feature columns graphed out against each other as a scatter plot (hint: exclude `zip`, `zipcode` and `features` using `drop`)

# COMMAND ----------

display(finalPrep.drop("zip").drop("zipcode").drop("features"))

# COMMAND ----------

# MAGIC %md * Split the `finalPrep` data set into training and testing subsets.  The sets should be randomly selected, 70 percent of the samples should go into the `training` set, and 30 percent should go into the `test` set.
# MAGIC * Cache `training` and `test`.
# MAGIC * Perform an action such as `count` to populate the cache.

# COMMAND ----------

(training, test) = finalPrep.randomSplit((0.7, 0.3))

training.cache()
test.cache()

print(training.count())
print(test.count())

# COMMAND ----------

# MAGIC %md Spark MLLib supports both `regressors` and `classifiers`, in this example you will use linear regression.  Once you create the `regressor` you will train it, and it will return a `Model`. The `Model` will be the object you use to make predictions.
# MAGIC 
# MAGIC * Create an instance of the `LinearRegression` algorithm called `lrModel`:
# MAGIC * Set the label column to "count"
# MAGIC * Set the features column to "features"
# MAGIC * Set the "ElasticNetParam" to 0.5 (this controlls the mix of l1 and l2 regularization--we'll just use an equal amount of each)
# MAGIC * Print the results of calling `explainParams` on `lrModel`.  This will show you all the possible parameters, and whether or not you have customized them.

# COMMAND ----------

from pyspark.ml.regression import LinearRegression

lrModel = LinearRegression()\
  .setLabelCol("count")\
  .setFeaturesCol("features")\
  .setElasticNetParam(0.5)

print("Printing out the model Parameters:")
print("-"*20)
print(lrModel.explainParams())
print("-"*20)

# COMMAND ----------

# MAGIC %md 
# MAGIC * Use the `fit` method on `lrModel` to provide the `training` dataset for fitting. 
# MAGIC * Store the results in `lrFitted`.

# COMMAND ----------

lrFitted = lrModel.fit(training)

# COMMAND ----------

# MAGIC %md 
# MAGIC * Make a prediction by using the `transform` method on `lrFitted`, passing it the `test` dataset. 
# MAGIC * Store the results in `holdout`.
# MAGIC * `transform` adds a new column called "prediction" to the data we passed into it.
# MAGIC * Display the `prediction` and `count` from `holdout`

# COMMAND ----------

holdout = lrFitted.transform(test)
display(holdout.select("prediction", "count"))

# COMMAND ----------

# MAGIC %md The `transform` method shows us how many farmer's markets the `lrFitted` method predicts there will be in each zip code based on the features we provided.  The raw predictions are not rounded at all.  
# MAGIC 
# MAGIC * Use a `selectExpr` to relabel `prediction` as `raw_prediction`.
# MAGIC * `round` the `prediction` and call it `prediction` inside the expression
# MAGIC * Select `count` for comparison purposes.
# MAGIC * Create a column called `equal` that will let us know if the model predicted correctly.
# MAGIC  

# COMMAND ----------

holdout = holdout.selectExpr(\
                             "prediction as raw_prediction", \
                             "double(round(prediction)) as prediction", \
                             "count", \
                             """CASE double(round(prediction)) = count 
                                WHEN true then 1
                                ELSE 0
                                END as equal""")
display(holdout)

# COMMAND ----------

# MAGIC %md * Use another `selectExpr` to `display` the proportion of predictions that were exactly correct.

# COMMAND ----------

display(holdout.selectExpr("sum(equal)/sum(1)"))

# COMMAND ----------

# MAGIC %md * Use `RegressionMetrics` to get more insight into the model performance. NOTE: Regression metrics requires input formatted as tuples of `double`s where the first item is the `prediction` and the second item is the observation (in this case the observation is `count`).  Once you have `map`ped these values from `holdout` you can directly pass them to the `RegressionMetrics` constructor.

# COMMAND ----------

from pyspark.mllib.evaluation import RegressionMetrics

mapped = holdout.select("prediction", "count").rdd.map(lambda x: (float(x[0]), float(x[1])))
rm = RegressionMetrics(mapped)

print ("MSE: ", rm.meanSquaredError)
print ("MAE: ", rm.meanAbsoluteError)
print ("RMSE Squared: ", rm.rootMeanSquaredError)
print ("R Squared: ", rm.r2)
print ("Explained Variance: ", rm.explainedVariance)

# COMMAND ----------

# MAGIC %md Because these results still aren't very good, rather than training a single-model, let's train several using a pipeline.
# MAGIC 
# MAGIC * Use a `RandomForestRegressor` algorithm.  This algorithm has several `hyperparameters` that we can tune, rather than tune them individually, we will use a `ParamGridBuilder` to search the "hyperparameter space" for us.  This can take some time on small clusters, so be patient.
# MAGIC 
# MAGIC * Use the `Pipeline` to feed the algorithm into a `CrossValidator` to help prevent "overfitting".
# MAGIC * Use the `CrossValidator` uses a `RegressionEvaluator` to test the model results against a metric (default is RMSE).
# MAGIC 
# MAGIC * NOTE: In production, using AWS EC2 compute-optimized instance speed this up -- 3 min (c3.4xlarge) vs 10 min (r3.xlarge)

# COMMAND ----------

from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator

rfModel = RandomForestRegressor()\
  .setLabelCol("count")\
  .setFeaturesCol("features")
  
paramGrid = ParamGridBuilder()\
  .addGrid(rfModel.maxDepth, [5, 10])\
  .addGrid(rfModel.numTrees, [20, 60])\
  .build()

steps = [rfModel]

pipeline = Pipeline().setStages(steps)

cv = CrossValidator()\
  .setEstimator(pipeline)\
  .setEstimatorParamMaps(paramGrid)\
  .setEvaluator(RegressionEvaluator().setLabelCol("count"))

pipelineFitted = cv.fit(training)

# COMMAND ----------

# MAGIC %md * Access the best model on the `pipelineFitted` object by accessing the first stage of the `bestModel` attribute.

# COMMAND ----------

print("The Best Parameters:\n--------------------")
print(pipelineFitted.bestModel.stages[0])

# COMMAND ----------

# MAGIC %md * Use the `bestModel` to `transform` the `test` dataset.  
# MAGIC * Use a `selectExpr` to show the raw prediction, rounded prediction, count, and whether or not the prediction exactly matched (hint: this is the same `selectExpr` you used on the previous model results).
# MAGIC * Store the results in `holdout2`, then display.

# COMMAND ----------

holdout2 = pipelineFitted.bestModel\
  .transform(test)\
  .selectExpr("prediction as raw_prediction", \
    "double(round(prediction)) as prediction", \
    "count", \
    """CASE double(round(prediction)) = count 
  WHEN true then 1
  ELSE 0
END as equal""")
  
display(holdout2)

# COMMAND ----------

# MAGIC %md * Show the `RegressionMetrics` for the new model results.

# COMMAND ----------

from pyspark.mllib.evaluation import RegressionMetrics

mapped2 = holdout2.select("prediction", "count").rdd.map(lambda x: (float(x[0]), float(x[1])))
rm2 = RegressionMetrics(mapped2)

print ("MSE: ", rm2.meanSquaredError)
print ("MAE: ", rm2.meanAbsoluteError)
print ("RMSE Squared: ", rm2.rootMeanSquaredError)
print ("R Squared: ", rm2.r2)
print ("Explained Variance: ", rm2.explainedVariance)

# COMMAND ----------

# MAGIC %md * See if there an improvement in the "exactly right" proportion.

# COMMAND ----------

display(holdout2.selectExpr("sum(equal)/sum(1)"))
