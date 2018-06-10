import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data',one_hot=True)

#每个批次的大小
batch_size = 100
#计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size


#定义两个placeholder
x = tf.placeholder(tf.float32,[None,784])#28*28
y = tf.placeholder(tf.float32,[None,10])

#改变x的格式转为4D的向量[batch,in_height,in_width,in_channel]
x_image = tf.reshape(x,[-1,28,28,1])#-1：样本数量不固定。1为黑白图像 若为3则为彩色图像

#------layer 1
W_conv1 = tf.Variable(tf.truncated_normal([5,5,1,32],stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1,shape=[32]))

h_conv1 = tf.nn.relu(tf.nn.conv2d(x_image,W_conv1,strides=[1,1,1,1],padding='SAME')+b_conv1)
h_pool1 = tf.nn.max_pool(h_conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
#------layer 2
W_conv2 = tf.Variable(tf.truncated_normal([5,5,32,64]))
b_conv2 = tf.Variable(tf.constant(0.1,shape=[64]))

h_conv2 = tf.nn.relu(tf.nn.conv2d(h_pool1,W_conv2,strides=[1,1,1,1],padding='SAME')+b_conv2)
h_pool2 = tf.nn.max_pool(h_conv2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#-------为转化成全连接层做准备
h_pool2_flat = tf.reshape(h_pool2,shape=[-1,7*7*64])
#-------全连接层
W_fcl = tf.Variable(tf.truncated_normal([7*7*64,1024]))
b_fcl = tf.Variable(tf.constant(0.1,shape=[1024]))

tf.nn.relu(tf.matmul(h_pool2_flat,W_fcl)+b_fcl)

#求第一个全连接层的输出
h_fcl = tf.nn.relu(tf.matmul(h_pool2_flat,W_fcl)+b_fcl)
keep_prob = tf.placeholder(tf.float32)
h_fcl_drop = tf.nn.dropout(h_fcl,keep_prob)
#防止过拟合，适当丢掉一些链接
# fcl2
W_fcl2 = tf.Variable(tf.truncated_normal([1024,10]))
b_fcl2 = tf.Variable(tf.constant(0.1,shape=[10]))

prediction = tf.nn.softmax(tf.matmul(h_fcl_drop,W_fcl2)+b_fcl2)



#交叉熵代价函数
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))

#使用AdamOptimizer进行优化
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

#结果存放在一个布尔列表中
correct_prediction  = tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))#argmax 返回一维张量中最大的值所在的位置

#求准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(21):
        for batch in range(n_batch):
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:0.7})
        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.0})
        print("Iter" + str(epoch)+", Testing Accuracy= "+ str(acc))