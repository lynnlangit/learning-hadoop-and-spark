# Databricks notebook source
# MAGIC %md This notebook uses Python and is a sample - be sure to update the text file name for your data

# COMMAND ----------

def printfunc(x):
    print 'Word "%s" occurs %d times' % (x[0], x[1])

infile = sc.textFile('/hone/spark/<myTextFile.txt>', 4)
rdd1 = infile.flatMap(lambda x: x.split())  
rdd2 = rdd2.map(lambda x: (x, 1)).reduceByKey(lambda x: x + y) 
print rdd2.toDebugString()
rdd2.foreach(printfunc)

# print ("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))

# COMMAND ----------

