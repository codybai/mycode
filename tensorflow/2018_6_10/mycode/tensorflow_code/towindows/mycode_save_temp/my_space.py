import numpy as np

# 转化一个序列列表为稀疏矩阵

def sparse_tuple_from(sequences, dtype=np.int32):
    """
    Create a sparse representention of x.
    Args:
        sequences: a list of lists of type dtype where each element is a sequence
    Returns:
        A tuple with (indices, values, shape)
    """
    indices = []
    values = []

    for n, seq in enumerate(sequences):
        indices.extend(zip([n] * len(seq), range(len(seq))))
        values.extend(seq)

    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray([len(sequences), np.asarray(indices).max(0)[1] + 1], dtype=np.int64)

    return indices, values, shape

string = ["世界卫生组织","AB是个好人","机器学习"]
dic = { "世":"1000000000000000",
        "界":"0100000000000000",
        "卫":"0010000000000000",
        "生":"0001000000000000",
        "组":"0000100000000000",
        "织":"0000010000000000",
        "A" :"0000001000000000",
        "B" :"0000000100000000",
        "是":"0000000010000000",
        "个":"0000000001000000",
        "好":"0000000000100000",
        "人":"0000000000010000",
        "机":"0000000000001000",
        "器":"0000000000000100",
        "学":"0000000000000010",
        "习":"0000000000000001"
}

def sparse_tuple_from_chinese(String):
    array = []
    for i in String:
        array.append(list(dic[i]))
    print(array)


import random
def create_sparse(batch_size, dtype=np.int32):


    indices = []
    values = []
    for i in range(batch_size):
      length = random.randint(150,180)
      for j in range(length):
         indices.append((i,j))
         value = random.randint(0,779)
         values.append(value)

    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray([batch_size, np.asarray(indices).max(0)[1] + 1], dtype=np.int64) #[64,180]

    return [indices, values, shape]
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = mnist = input_data.read_data_sets('MNIST_data',one_hot=True)
batch_size = 100
batch_xs, batch_ys = mnist.train.next_batch(batch_size)
def my_sparse_from(B):
    indices = []
    values = []
    dense_shape = [batch_size, 10]
    row = -1
    for i in B:
        row += 1
        col = 0
        for j in i:
            if j != 0.0:
                indices.append((row, col))
                values.append(col)
            col += 1
    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=np.int32)
    dense_shape = np.asarray([batch_size, 10], dtype=np.int64)  # [64,180]
    return [values,indices,dense_shape]
# values,indices,shape=my_sparse_from(batch_ys)
# st= tf.SparseTensor(values=values,indices=indices,dense_shape=shape)
# print(tf.sparse_to_dense(st.indices,st.dense_shape,st.values))
# print(st.values)
# print(st.dense_shape)
# print
def create_sparse(batch_size, dtype=np.int32):
    indices = []
    values = []
    for i in range(batch_size):
       length = random.randint(150,180)
       for j in range(length):
           indices.append((i,j))
           value = random.randint(0,779)
           values.append(int(str('柏')))

    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray([batch_size, np.asarray(indices).max(0)[1] + 1], dtype=np.int64) #[64,180]

    return indices, values, shape
# print(create_sparse(1))
# tf.SparseTensor
# str = '0'
# print([7]*2)
print(my_sparse_from(batch_ys))


