import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

mnist = input_data.read_data_sets('MNIST_data',one_hot=True)

#每个批次的大小
batch_size = 100
#计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size
x = tf.placeholder(tf.float32,shape=[None,28*28])
y = tf.placeholder(tf.float32,shape=[None,10])

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
prediction = tf.nn.softmax(tf.matmul(final_state[1],w_lstm)+b_lstm)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y,1),tf.argmax(prediction,1)),tf.float32))

# with tf.Session() as sess:
#     sess.run(tf.global_variables_initializer())
#     for epoch in range(10):
#         for batch in range(n_batch):
#             batch_xs,batch_ys = mnist.train.next_batch(batch_size)
#             sess.run(train_step,feed_dict={y:batch_ys,x:batch_xs})
#         acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
#
#         print("Iter:"+str(epoch)+"acc:"+str(acc))


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



with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(10):
        for batch in range(n_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # print(sess.run(tf.shape(result_pool3),feed_dict={x:batch_xs,y:batch_ys}))
            # print(sess.run(outputs,feed_dict={x:batch_xs,y:batch_ys}))
            a=[]
            for i in range(100):
                a.append(list(batch_ys[0]))
                b=sparse_tuple_from(a)
            print(b)
            break
        break
