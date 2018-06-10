import tensorflow as tf
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data',one_hot=True)
import numpy as np
import pickle as pkl
from PIL import Image

batch_size = 100
batch_xs, batch_ys = mnist.train.next_batch(batch_size)
seq_len = np.ones(4) * 7

#完成
def decode_sparse_tensor(sparse_tensor):  #将SparseTensor转化成稀疏矩阵
    return tf.sparse_to_dense(sparse_tensor.indices, sparse_tensor.dense_shape, sparse_tensor.values)
#完成
def ylist_to_sparse(labellist):  #  直接用读取出来的data变成SparseTensor 所有的y
    indices = []
    values=[]
    max_row = 0
    max_col = 0
    y = []
    for j in labellist:
        y.append(list(j[0]))
    # y:#[
    # ['大', '飞', '机'],
    # ['大', '写', '的', 'A', '和', 'B'],
    # ['1', '搜', '轮', '船'],
    # ['1', '个', '人', '在', '玩', 'c', 'F']]
    for idx,i in enumerate(y):
        if idx >max_row:
            max_row=idx
        for jdx, j in enumerate(i):    #循环编码
            y[idx][jdx] = ord(y[idx][jdx])
            indices.append([idx,jdx])
            values.append(y[idx][jdx])
            if jdx>max_col:
                max_col=jdx
    shape=[max_row+1,max_col+1]
    return indices,values,shape
#完成
def save_to_pkl():
    file_image = "file_image/"
    file_text = "file_text/"
    f1= open("dataset.pkl","wb+")
    num_data = 4
    total = []
    for i in range(num_data):  #4为数据的个数
        image_path = file_image+str(i)+".jpg"
        text_path = file_text+str(i)+".txt"
        image = np.array(Image.open(image_path))
        f = open(text_path)
        label = f.readline().strip()
        f.close()
        total.append([image,label])
        print("已经拼接:%d/%d" % (i+1 , num_data))
    # print(total)
    try:
        pkl.dump(total,f1)
    except:
        print("保存失败！")
    f1.close()
    print("保存成功！")
#测试
def text_save_to_pkl():
    file = open('dataset.pkl','rb+')
    datalist = pkl.load(file)
    for i in datalist:
        print(i[1])
#完成
def read_data(type):
    if type == 'train':
        sl=seq_len
        f = open("dataset.pkl", "rb+")
        data = pkl.load(f)
        f.close()
        x_ = []
        # y = np.zeros(shape=[batch_size,])
        y = []
        for i in data:
            x_.append([i[0]])
            y.append([i[1]])
        x = []
        for i in x_:    #将所有x转化成[size,pic_h,pic_w,channel]    [bsize,32,192,3]
            x.append(i[0])
    elif type == 'test':
        sl=seq_len
        f = open("testdataset.pkl", "rb+")
        data = pkl.load(f)
        f.close()
        x_ = []
        y = []
        for i in data:
            x_.append([i[0]])
            y.append([i[1]])
        x = []
        for i in x_:    #将所有x转化成[size,pic_h,pic_w,channel]    [size,32,192,3]
            x.append(i[0])
    return x, y, sl   # y应该为稀疏矩阵  之后传入 tct前要进行转化成为SparseTensor
                      # sl=[time_step,time_step,,,,]长度为batch_size
#完成
def get_next_batch(type):
    if type == 'train':
        i = g.train_i
        b = 2
        x = g.x_train[i * b:(i + 1) * b]
        y_ = g.y_train[i:(i + b)]  # y要根据数据格式调整
        seq_len = g.sl_train[i:(i + 1)]
        g.train_i += 1
    elif type == 'test':
        i = g.train_i
        b = batch_size
        x = g.x_train[i * b:(i + 1) * b]
        y_ = g.y_train[i:(i + b)]  # y要根据数据格式调整
        seq_len = g.sl_train[i:(i + 1)]
        g.train_i += 1

    # 转化成SparseTensor
    indices, values, shape = ylist_to_sparse(y_)
    y = tf.SparseTensor(indices=indices, values=values, dense_shape=shape)
    # y 这里应该是SparseTensor         ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    return x, y, seq_len  # x:[2,h,w,3]   y:SparseTensor  seq_len=[7,7]


class g:
    def __init__(self):
        self.train_i=0
        self.test_i=0
        self.x_train,self.y_train,self.sl_train = read_data('train')


# with tf.Session() as sess:
#
#     g = g()
#     x1,y1,sl1 = get_next_batch('train')
#     x2,y2,sl2 = get_next_batch('train')
#     x,y,sl = read_data('train')
#     # print(sess.run(decode_sparse_tensor(y1)))
#     # print(sess.run(decode_sparse_tensor(y2)))
#     a = np.reshape(x1[0],newshape=[1,293*550*3])
#     b = np.reshape(x1[1], newshape=[1, 293 * 550 * 3])
#     a.__add__(b[0])
#     print(a)
save_to_pkl()
text_save_to_pkl()
tf.SparseTensorValue()