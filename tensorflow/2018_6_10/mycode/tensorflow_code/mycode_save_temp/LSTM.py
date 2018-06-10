import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist=input_data.read_data_sets("MNIST_data/",one_hot=True)

h_input = 28
seq_length = 28
num_hide = 100
num_classes = 10
batch_size=50#每个批次50个样本
n_batch = mnist.train.num_examples // batch_size

#None 可以是任意长度
x = tf.placeholder(tf.float32,[None,784])#why 784
y = tf.placeholder(tf.float32,[None,10]) #标签为10个

#初始化权值
weights = tf.Variable(tf.truncated_normal([num_hide,num_classes],stddev=0.1))
#初始化偏置
biases = tf.Variable(tf.constant(0.1,shape=[num_classes]))

def RNN(X,Weight,Biases):
    inputs = tf.reshape(X,[-1,seq_length,h_input])

    lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_hide)

    outputs,final_state = tf.nn.dynamic_rnn(lstm_cell,inputs,dtype=tf.float32)
    #final_state   = [state,batch_size,cell.state_size]
    #final_state[0] = cell state
    #final_state[1] = hidden_state
    #   state_size = num_hide
    #outputs:  RNN output tensor
    # If time_major = False   output = [batch_size,max_time,cell.output_size]  其中cell.output_size = num_hide
    # If time_major = True    output = [max_time,batch_size,cell.output_size]  同上
    #final_state[0]是cell state
    #final_state[1]是hidden_state
    results  = tf.nn.softmax(tf.matmul(final_state[1],weights)+biases)   #final_state[1] 不懂
    return results


predict = RNN(x,weights,biases)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predict,labels=y))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(predict,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

init = tf.global_variables_initializer();

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(6):#总共迭代6次
        for batch in range(n_batch):#循环完毕是完成一次遍历
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys})

        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels})
        print("Iter" + str(epoch) + ",Testing Accuracy= "+ str(acc))