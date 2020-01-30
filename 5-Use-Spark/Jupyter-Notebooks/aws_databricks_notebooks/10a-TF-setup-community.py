# Databricks notebook source
# MAGIC %md # Install TensorFlow on a single node
# MAGIC 
# MAGIC We can install TensorFlow on a single node using the following script. 
# MAGIC 
# MAGIC This should work fine on the community edition because the driver and the worker are on the same node. 
# MAGIC 
# MAGIC Run the script below.

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC tfBinaryUrl="https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0-cp27-none-linux_x86_64.whl"
# MAGIC 
# MAGIC set -ex
# MAGIC 
# MAGIC echo "**** Installing CPU-enabled TensorFlow *****"
# MAGIC 
# MAGIC pip install ${tfBinaryUrl}

# COMMAND ----------

# MAGIC %md With python, it is normally only necessary to install a module before you can start using it.  However, when working in a notebook, python is already “running”.  So, python will not notice that the TensorFlow module is available unless you “restart” python.  
# MAGIC 
# MAGIC This is simpler than it sounds.  Simply use the cluster menu to `Detach` from your cluster.  Then use the menu again to `Attach` to the cluster.  The notebook will be executed again with a fresh instance of python, and you should be able to import TensorFlow as you normally would.
# MAGIC 
# MAGIC Try importing `tensorflow` now as `tf`, and `print` `__version__`.

# COMMAND ----------

import tensorflow as tf
print tf.__version__

# COMMAND ----------

# MAGIC %md Now you should have a working single-node Spark cluster.  This means that not only will python work, but Spark will work too.  

# COMMAND ----------

# MAGIC %md # Continue to Notebook 6
# MAGIC 
# MAGIC If your community cluster terminates you will need to run this notebook again to install tensorflow.  After running this notebook, you can do the exercises in Notebook 11-UseTF.py.