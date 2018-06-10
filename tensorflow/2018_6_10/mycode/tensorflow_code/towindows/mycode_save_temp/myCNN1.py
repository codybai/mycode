import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data',one_hot = True)
batch_size = 100
n_batch = mnist.train.num_examples // batch_size

keep_prob = tf.placeholder(tf.float32)
x = tf.placeholder(tf.float32,[None,28*28])
y = tf.placeholder(tf.float32,[None,10])

#layer 1
in_conv1 = tf.reshape(x,shape=[-1,28,28,1])
w_conv1 = tf.Variable(tf.truncated_normal(shape=[5,5,1,32],stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1,shape=[32]))
h_conv1 = tf.nn.relu(tf.nn.conv2d(in_conv1,w_conv1,strides=[1,1,1,1],padding='SAME')+b_conv1)
h_pool1 = tf.nn.max_pool(h_conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#layer 2
w_conv2 = tf.Variable(tf.truncated_normal(shape=[5,5,32,64]))
b_conv2 = tf.Variable(tf.constant(0.1,shape=[64]))
h_conv2 = tf.nn.relu(tf.nn.conv2d(h_pool1,w_conv2,strides=[1,1,1,1],padding='SAME'))
h_pool2 = tf.nn.max_pool(h_conv2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#fcl
in_fcl1 = tf.reshape(h_pool2,shape=[-1,7*7*64])
w_fcl1 = tf.Variable(tf.truncated_normal(shape=[7*7*64,1024],stddev=0.1))
b_fcl1 = tf.Variable(tf.constant(0.1,shape=[1024]))
h_fcl1 = tf.nn.relu(tf.matmul(in_fcl1,w_fcl1)+b_fcl1)
h_fcl1_dropout = tf.nn.dropout(h_fcl1,keep_prob=keep_prob)

#fcl
w_fcl2 = tf.Variable(tf.truncated_normal(shape=[1024,10],stddev=0.1))
b_fcl2 = tf.Variable(tf.constant(0.1,shape=[10]))

# prediction = tf.nn.softmax(tf.matmul(h_fcl1_dropout,w_fcl2)+b_fcl2)
prediction = tf.nn.softmax(tf.matmul(h_fcl1_dropout,w_fcl2)+b_fcl2)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction  = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(21):
        for batch in range(n_batch):
            _x,_y = mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:_x,y:_y,keep_prob:0.7})
        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.})
        print("Iter:"+str(epoch)+"acc:"+str(acc))


