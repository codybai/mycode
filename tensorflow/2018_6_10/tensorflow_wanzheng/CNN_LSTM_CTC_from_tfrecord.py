import tensorflow as tf
import pickle as pk
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.training import moving_averages

input_height = 32
input_wide = 256
batch_size = 100
time_steps = 256
num_hidden = 256
num_classes = 4348+1
epochs = 10000


input = tf.placeholder(tf.float32,shape=[None,32,256,1])
yto_beam = tf.sparse_placeholder(dtype=tf.int32)
ground_truth = tf.sparse_placeholder(tf.int32)