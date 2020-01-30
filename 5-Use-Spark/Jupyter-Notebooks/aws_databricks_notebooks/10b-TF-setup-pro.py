# Databricks notebook source
# MAGIC %md # Install TensorFlow with an init script.
# MAGIC 
# MAGIC Init scripts are global to the databricks cluster (which is separate from the spark cluster).  
# MAGIC 
# MAGIC You save an init script to the databricks file system in a subdirectory bearing the cluster name.  
# MAGIC 
# MAGIC When you launch a cluster with that name, databricks looks for the folder in order to run the scripts there.
# MAGIC 
# MAGIC ## Create the init-script
# MAGIC 
# MAGIC Because this script will update the global databricks environment, it can be run from any notebook, attached to any cluster.  

# COMMAND ----------

# The name of the cluster on which to install TensorFlow:
clusterName = "tensorflow-cpu"

# TensorFlow binary URL
tfBinaryUrl = "https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0-cp27-none-linux_x86_64.whl"

# Create the script tempalte, then render it using format.
script = """#!/usr/bin/env bash

set -ex

echo "**** Installing GPU-enabled TensorFlow *****"

pip install {tfBinaryUrl}
""".format(tfBinaryUrl = tfBinaryUrl)

# Write the script to the global environment
dbutils.fs.mkdirs("dbfs:/databricks/init/")
dbutils.fs.put("dbfs:/databricks/init/%s/install-tensorflow-gpu.sh" % clusterName, script, True)

# COMMAND ----------

# MAGIC %md Now that the template exists we can create a cluster called `tensorflow-cpu`, since that is the name of the folder where we put the script.
# MAGIC 
# MAGIC Once the `tensorflow-cpu` cluster launches, attach this notebook to it and see if tensorflow is available by trying to import it.
# MAGIC 
# MAGIC If you are already running on the cluster where you want to install tensorflow, restart it, then attach this notebook to it when it finishes restarting.

# COMMAND ----------

import tensorflow as tf
print tf.__version__

# COMMAND ----------

# MAGIC %md Now you should have a working multi-node Spark cluster.  This means that not only will python work, but Spark will work too.  This step is not necessary in the community edition because all community edition clusters are single-node, with the driver and the worker on the same node.
# MAGIC 
# MAGIC A single-node professional cluster only includes the driver, there is no way to install the worker on the same node using a professional account.

# COMMAND ----------

# MAGIC %md # Continue to Notebook 6
# MAGIC 
# MAGIC This notebook only needs to run once to setup the cluster.  Now you can do the exercises in Notebook 11_Use_TF.py.