# Databricks notebook source
# MAGIC %md To install MXNet on a single node using the following script (for the community edition because the driver and the worker are on the same node).  
# MAGIC * Run the script below.
# MAGIC 
# MAGIC **NOTE: Use an init script to install on a multi-node cluster. Using this script on a multinode cluster will not work, because MXNet will only be installed on the driver.  The init script solves this problem by running the install script when the worker launches. ** 

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC rm -rf /usr/local/mxnet
# MAGIC 
# MAGIC mxnetGitTag="eaa6253"
# MAGIC 
# MAGIC set -ex
# MAGIC 
# MAGIC echo "**** Installing MXNet dependencies ****"
# MAGIC 
# MAGIC apt-get update
# MAGIC 
# MAGIC # Requirements stated in http://mxnet.io/get_started/setup.html#standard-installation.
# MAGIC # We used OpenBLAS instead of ATLAS.
# MAGIC apt-get install -y build-essential git libopenblas-dev libopencv-dev python-numpy python-setuptools
# MAGIC 
# MAGIC echo "**** Downloading MXNet ****"
# MAGIC 
# MAGIC MXNET_HOME=/usr/local/mxnet
# MAGIC git clone --recursive https://github.com/dmlc/mxnet $MXNET_HOME
# MAGIC cd $MXNET_HOME
# MAGIC git checkout ${mxnetGitTag}
# MAGIC git submodule update
# MAGIC 
# MAGIC echo "**** Building MXNet ****"
# MAGIC 
# MAGIC USE_CUDA=0 USE_CUDNN=0 USE_CUDA_PATH=/usr/local/cuda USE_BLAS=openblas make -e -j$(nproc)
# MAGIC 
# MAGIC echo "**** Installing MXNet ****"
# MAGIC 
# MAGIC cd python
# MAGIC python setup.py install

# COMMAND ----------

# MAGIC %md With python, it is normally only necessary to install a module before you can start using it.  However, when working in a notebook, python is already “running”.  So, python will not notice that the MXNet module is available unless you “restart” python.  
# MAGIC 
# MAGIC This is simpler than it sounds.  Simply use the cluster menu to `Detach` from your cluster.  Then use the menu again to `Attach` to the cluster.  The notebook will be executed again with a fresh instance of python, and you should be able to import MXNet as you normally would.
# MAGIC 
# MAGIC Try importing `mxnet` now as `mx`, and `print` `__version__`.

# COMMAND ----------

import mxnet as mx
print (mx.__version__)

# COMMAND ----------

# MAGIC %md With module installation out of the way.  Lets get started by loading some data.

# COMMAND ----------

import numpy as np
import os
import urllib
import urllib.request
import gzip
import struct

def download_data(url, force_download=True): 
    fname = url.split("/")[-1]
    if force_download or not os.path.exists(fname):
        urllib.request.urlretrieve(url, fname)
    return fname

def read_data(label_url, image_url):
    with gzip.open(download_data(label_url)) as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        label = np.fromstring(flbl.read(), dtype=np.int8)
    with gzip.open(download_data(image_url), 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        image = np.fromstring(fimg.read(), dtype=np.uint8).reshape(len(label), rows, cols)
    return (label, image)

path='http://yann.lecun.com/exdb/mnist/'
(train_lbl, train_img) = read_data(
    path+'train-labels-idx1-ubyte.gz', path+'train-images-idx3-ubyte.gz')
(val_lbl, val_img) = read_data(
    path+'t10k-labels-idx1-ubyte.gz', path+'t10k-images-idx3-ubyte.gz')

# COMMAND ----------

import matplotlib.pyplot as plt
for i in range(10):
    plt.subplot(1,10,i+1)
    plt.imshow(train_img[i], cmap='Greys_r')
    plt.axis('off')
plt.show()
display()

# COMMAND ----------

print('label: %s' % (train_lbl[0:10],))

# COMMAND ----------

# MAGIC %md Create data iterators

# COMMAND ----------

def to4d(img):
    return img.reshape(img.shape[0], 1, 28, 28).astype(np.float32)/255

batch_size = 100
train_iter = mx.io.NDArrayIter(to4d(train_img), train_lbl, batch_size, shuffle=True)
val_iter = mx.io.NDArrayIter(to4d(val_img), val_lbl, batch_size)

# COMMAND ----------

# MAGIC %md Multilayer Perceptron

# COMMAND ----------

# Create a place holder variable for the input data
data = mx.sym.Variable('data')
# Flatten the data from 4-D shape (batch_size, num_channel, width, height) 
# into 2-D (batch_size, num_channel*width*height)
data = mx.sym.Flatten(data=data)

# The first fully-connected layer
fc1  = mx.sym.FullyConnected(data=data, name='fc1', num_hidden=128)
# Apply relu to the output of the first fully-connnected layer
act1 = mx.sym.Activation(data=fc1, name='relu1', act_type="relu")

# The second fully-connected layer and the according activation function
fc2  = mx.sym.FullyConnected(data=act1, name='fc2', num_hidden = 64)
act2 = mx.sym.Activation(data=fc2, name='relu2', act_type="relu")

# The thrid fully-connected layer, note that the hidden size should be 10, which is the number of unique digits
fc3  = mx.sym.FullyConnected(data=act2, name='fc3', num_hidden=10)
# The softmax and loss layer
mlp  = mx.sym.SoftmaxOutput(data=fc3, name='softmax')

# COMMAND ----------

# MAGIC %md Now both the network definition and data iterators are ready. We can start training.

# COMMAND ----------

model = mx.model.FeedForward(
    symbol = mlp,       # network structure
    num_epoch = 10,     # number of data passes for training 
    learning_rate = 0.1 # learning rate of SGD 
)
model.fit(
    X=train_iter,       # training data
    eval_data=val_iter, # validation data
    batch_end_callback = mx.callback.Speedometer(batch_size, 200) # output progress for each 200 data batches
) 

# COMMAND ----------

# MAGIC %md After training is done, we can predict a single image.

# COMMAND ----------

plt.clf()
plt.imshow(val_img[0], cmap='Greys_r')
plt.axis('off')
plt.show()
display()

# COMMAND ----------

prob = model.predict(val_img[0:1].astype(np.float32)/255)[0]
print ('Classified as %d with probability %f' % (prob.argmax(), max(prob)))

# COMMAND ----------

# MAGIC %md We can also evaluate the accuracy by given a data iterator.

# COMMAND ----------

print ('Validation accuracy: %f%%' % (model.score(val_iter)*100,))

# COMMAND ----------

# MAGIC %md Convolutional Neural Networks

# COMMAND ----------

data = mx.symbol.Variable('data')
# first conv layer
conv1 = mx.sym.Convolution(data=data, kernel=(5,5), num_filter=20)
tanh1 = mx.sym.Activation(data=conv1, act_type="tanh")
pool1 = mx.sym.Pooling(data=tanh1, pool_type="max", kernel=(2,2), stride=(2,2))
# second conv layer
conv2 = mx.sym.Convolution(data=pool1, kernel=(5,5), num_filter=50)
tanh2 = mx.sym.Activation(data=conv2, act_type="tanh")
pool2 = mx.sym.Pooling(data=tanh2, pool_type="max", kernel=(2,2), stride=(2,2))
# first fullc layer
flatten = mx.sym.Flatten(data=pool2)
fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=500)
tanh3 = mx.sym.Activation(data=fc1, act_type="tanh")
# second fullc
fc2 = mx.sym.FullyConnected(data=tanh3, num_hidden=10)
# softmax loss
lenet = mx.sym.SoftmaxOutput(data=fc2, name='softmax')

# COMMAND ----------

# MAGIC %md Note that LeNet is more complex than the previous multilayer perceptron, so we use GPU instead of CPU for training.  
# MAGIC NOTE: This takes up to 45 minute on the community edition - this is the point at which you could integrate with Spark (i.e. via broadcast, etc...)  to optimize.

# COMMAND ----------

model = mx.model.FeedForward(
#     ctx = mx.gpu(0),     # use GPU 0 for training, others are same as before
    symbol = lenet,       
    num_epoch = 10,     
    learning_rate = 0.1)
model.fit(
    X=train_iter,  
    eval_data=val_iter, 
    batch_end_callback = mx.callback.Speedometer(batch_size, 200)
) 

# COMMAND ----------

print ('Validation accuracy: %f%%' % (model.score(val_iter)*100,))
