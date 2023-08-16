#!/usr/bin/python
import pyspark
sc = pyspark.SparkContext()
rdd = sc.parallelize(['Hello,','pyspark', 'world!'])
words = sorted(rdd.collect())
print(words)
