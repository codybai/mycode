import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#载入数据集
mnist = input_data.read_data_sets("MNIST_data",one_hot=True)#one_hat 如： 0000000100

#定义每个批次的大小  训练模型时一次性放入的大小以矩阵的形式
batch_size = 100

#计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size

#定义两个placeholder
x= tf.placeholder(tf.float32,[None,784]) #None：代表每个批次的大小  784：图像变成一维向量的大小
y= tf.placeholder(tf.float32,[None,10])  #10个神经元

#创建一个简单的神经网络
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
prediction  = tf.nn.softmax(tf.matmul(x,W)+b)

#定义二次代价函数  用交叉熵？
# loss = tf.reduce_mean(tf.square(y-prediction))

#定义交叉熵代价函数   #调整比较合理，收敛比较快
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))

#使用梯度下降法
# train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

train_step = tf.train.AdamOptimizer(1e-3).minimize(loss) #1e-3 0.001

#初始化变量
init = tf.global_variables_initializer()

#结果存放在一个布尔型列表中
correct_prediction = tf.equal(tf.argmax(y,1),tf.arg_max(prediction,1))#argmax返回一维张量最大值（也就是1，不是0）所在的位置

#求准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))#case（a,b）a转化为b类型
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(20):
        for batch in range(n_batch):
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys})
        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels})
        print("iter " + str(epoch) + ",Testing Accuracy" + str(acc))
sess.close()