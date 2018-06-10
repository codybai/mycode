import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist=input_data.read_data_sets("MNIST_data/",one_hot=True)

h_input = 28
seq_length = 28
num_hide = 100
num_classes = 10
batch_size=50#每个批次50个样本
n_batch = mnist.train.num_examples // batch_size
x = tf.placeholder(tf.float32,shape=[None,28*28])
y = tf.placeholder(tf.float32,shape=[None,10])

weight = tf.Variable(tf.truncated_normal(shape=[num_hide,num_classes],stddev=0.1))
bias = tf.Variable(tf.constant(0.1,shape=[num_classes]))
input = tf.reshape(x,shape=[-1,seq_length,h_input])


cell = tf.nn.rnn_cell.BasicLSTMCell(num_hide)
ouputs,last_state = tf.nn.dynamic_rnn(cell,input,dtype=tf.float32)

predict = tf.nn.softmax(tf.matmul(last_state[1],weight)+bias)



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