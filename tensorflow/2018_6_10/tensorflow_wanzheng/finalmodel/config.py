import tensorflow as tf
import pickle as pk
import numpy as np

from keras.datasets import cifar10
from .tools import *

data_path = ''
#dataset_len = 104066
#训练参数
batch_size = 200
epochs = 500
global_step = tf.Variable(0, trainable=False)
min_after_dequeue = 1000                          #读取文件队列最小长度
TRAIN_DATA_SET_LEN = 100000                       #训练集大小
TEST_DATA_SET_LEN = 4066                          #测试集大小
N_TRAIN_BATCH = TRAIN_DATA_SET_LEN // batch_size  #训练集batch数量
N_TEST_BATCH = TEST_DATA_SET_LEN   // batch_size  #测试集batch数量
model_name = 'model.ckpt'                       #模型名称

#网络参数
im_row = 32
im_col = 256
im_channel = 3
inputs_shape = [batch_size, im_row, im_col, im_channel]
num_classes = 4348+1                              #训练集的所有字符种类
max_label_len = 7

lstm_hidden = num_classes                         #lstm隐藏层   最后输出维度则为num_classes


#学习率设置
INITIAL_LEARNING_RATE = 1e-3
DECAY_STEPS = 5000
REPORT_STEPS = 100
LEARNING_RATE_DECAY_FACTOR = 0.9 # The learning rate decay factor
learning_rate = tf.train.exponential_decay(
    INITIAL_LEARNING_RATE, global_step, DECAY_STEPS,
    LEARNING_RATE_DECAY_FACTOR, staircase=True)





#
# class Global:      #tfrecord todo
#     def __init__(self):
#         (x_train, y_train), (x_test, y_test) = cifar10.load_data()
#         self.x_train = x_train
#         self.x_test = x_test
#
#         label = [[1] * 5]
#         y_train = label * 60000
#         y_test = label * 10000
#         self.y_train = np.array(y_train)
#         self.y_test = np.array(y_test)
#         self.dictset = [i for i in range(1,101)]
#
#
#         '''with open(data_path, "rb+") as f:
#             data = pk.load(f)
#             x, y = [], []
#             self.j = 0  # 记录总的数据量
#             for i in data:
#                 x.append(i[0])
#                 y.append(i[1])
#                 self.j += 1
#         with open(dictset_path, 'rb') as f:
#             data = pk.load(f)
#             self.dictset = data
#
#         x = np.array(x)    #变长要修改
#         y = np.array(y)
#         x = self.color_preprocessing(x)
#
#         d = int(4 / 5 * len(x))
#         self.x_train, self.y_train = x[:d], y[:d]
#         self.x_test, self.y_test = x[d:], y[d:]'''
#
#
#     def color_preprocessing(self, x):
#         mean = [125.307, 122.95, 113.865]
#         std = [62.9932, 62.0887, 66.7048]
#         x = x.astype('float32')
#         for i in range(3):
#             x[:, :, :, i] = (x[:, :, :, i] - mean[i]) / std[i]
#         return x
#
#
#     def train(self):
#         self.train_batchs = int(len(self.x_train) / batch_size)
#         self.train_size = self.train_batchs * batch_size
#         self.train_i = 0
#
#
#     def test(self):
#         self.test_batchs = int(len(self.x_test) / batch_size)
#         self.test_size = self.test_batchs * batch_size
#         self.test_i = 0
# g = Global()
#
# def get_next_batch(type):   #tfrecord todo
#     if type == 'train':
#         i = g.train_i
#         b = batch_size
#         x = g.x_train[i * b: (i + 1) * b]
#         y = g.y_train[i: (i + b)]  # y要根据数据格式调整
#         g.train_i += 1
#     elif type == 'test':
#         i = g.test_i
#         b = batch_size
#         x = g.x_test[i * b: (i + 1) * b]
#         y = g.y_test[i:(i + b)]  # y要根据数据格式调整
#         g.test_i += 1
#
#     indices, values, shape = ylist_to_sparse(y)
#     y = [indices, values, shape]
#
#     return x, y


