import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

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



mnist = input_data.read_data_sets('MNIST_data',one_hot=True)

#每个批次的大小
batch_size = 100
#计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size
x = tf.placeholder(tf.float32,shape=[None,28*28])
# y = tf.placeholder(tf.float32,shape=[None,10])

h_input = 28
num_hiden = 512
num_classes = 10
num_seq = 7

#cnn_layer1
in_conv1 = tf.reshape(x,shape=[-1,28,28,1])
w_conv1 = tf.Variable(tf.truncated_normal(shape=[5,5,1,32],stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1,shape=[32]))
result_conv1 = tf.nn.conv2d(in_conv1,w_conv1,strides=[1,1,1,1],padding='SAME')
result_pool1 = tf.nn.max_pool(result_conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
#cnn_layer2
w_conv2 = tf.Variable(tf.truncated_normal(shape=[5,5,32,64],stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1,shape=[64]))
result_conv2 = tf.nn.conv2d(result_pool1,w_conv2,strides=[1,1,1,1],padding='SAME')
result_pool2 = tf.nn.max_pool(result_conv2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

result_pool3 = tf.nn.max_pool(result_pool2,ksize=[1,1,7,1],strides=[1,7,1,1],padding='SAME')
#LSTM
w_lstm = tf.Variable(tf.truncated_normal(shape=[num_hiden,num_classes],stddev=0.1))
b_lstm = tf.Variable(tf.constant(0.1,shape=[num_classes]))
in_lstm = tf.reshape(result_pool2,[-1,num_seq,64*7])
cell = tf.nn.rnn_cell.BasicLSTMCell(num_hiden)
outputs,final_state = tf.nn.dynamic_rnn(cell,in_lstm,dtype=tf.float32)
#因为取得是最后一个所以直接用final_state
#如果每个输出都要用则需要用outputs,同时需要变形  outputs.reshap(outputs,[batch_size*max_time_step,num_hiden])

outputs = tf.reshape(outputs,shape=[batch_size*num_seq,num_hiden])
outputs_after_xwb =tf.matmul(outputs,w_lstm)+b_lstm
# testout= tf.nn.softmax(tf.matmul(final_state[1],w_lstm)+b_lstm)
outputs_after_xwb = tf.reshape(outputs_after_xwb,shape=[batch_size,num_seq,num_classes])
outputs_after_xwb = tf.transpose(outputs_after_xwb,[1,0,2])
indices = tf.placeholder(tf.int64)
value = tf.placeholder(tf.int32)
shape = tf.placeholder(tf.int64)
# outputs_after_xwb = tf.reshape(outputs_after_xwb,shape=[batch_size,num_seq,num_classes])
st = tf.SparseTensor(indices=indices,values=value, dense_shape=shape)
ctc_loss = tf.nn.ctc_loss(labels=st,inputs=outputs_after_xwb,sequence_length=[7]*batch_size)
cost = tf.reduce_mean(ctc_loss)
#
train_step = tf.train.AdamOptimizer(1e-4).minimize(cost)
decoded, log_prob = tf.nn.ctc_beam_search_decoder(outputs_after_xwb, [7]*batch_size, merge_repeated=False)
# acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), targets))
a= tf.sparse_to_dense(decoded[0].indices,decoded[0].dense_shape,decoded[0].values)
y = tf.placeholder(tf.float32)
# correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(testout,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))


with tf.Session() as sess:
#     sess.run(tf.global_variables_initializer())
#
#     batch_xs,batch_ys = mnist.train.next_batch(batch_size)
#     t=my_sparse_frotf.shape(batch_xs)m(batch_ys)
#     print(sess.run(a,feed_dict={indices:t[1],value:t[0],shape:t[2],x:batch_xs}))
     batch_xs,batch_ys = mnist.train.next_batch(batch_size)
     # print(batch_ys[0])
     print(chr(49))
     # print(sess.run(in_conv1,feed_dict={x:batch_xs}))



