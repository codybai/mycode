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

keep_prob = tf.placeholder(tf.float32)
lr = tf.Variable(0.001,dtype=tf.float32)
#创建一个简单的神经网络
# W1 = tf.Variable(tf.zeros([784,10]))#这种初始化不是很好
# b1 = tf.Variable(tf.zeros([10]))#这种初始化不是很好
W1 = tf.Variable(tf.truncated_normal([784,500],stddev=0.1))#截断正态分布初始化
b1 = tf.Variable(tf.zeros([500])+0.1)
L1 = tf.nn.tanh(tf.matmul(x,W1)+b1)
L1_drop = tf.nn.dropout(L1,keep_prob) #keep_prob表示有百分之几的神经元是工作的keep_prob=1表示百分之百

W2 = tf.Variable(tf.truncated_normal([500,300],stddev=0.1))#截断正态分布初始化
b2 = tf.Variable(tf.zeros([300])+0.1)
L2 = tf.nn.tanh(tf.matmul(L1_drop,W2)+b2)
L2_drop = tf.nn.dropout(L2,keep_prob)#keep_prob表示有百分之几的神经元是工作的keep_prob=1表示百分之百

W3 = tf.Variable(tf.truncated_normal([300,10],stddev=0.1))#截断正态分布初始化
b3 = tf.Variable(tf.zeros([10])+0.1)
prediction  = tf.nn.softmax(tf.matmul(L2_drop,W3)+b3)

#定义二次代价函数  用交叉熵？
# loss = tf.reduce_mean(tf.square(y-prediction))

#定义交叉熵代价函数   #调整比较合理，收敛比较快
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))

#使用梯度下降法
train_step = tf.train.AdamOptimizer(lr).minimize(loss)#非常非常的关键啊

#初始化变量
init = tf.global_variables_initializer()

#结果存放在一个布尔型列表中
correct_prediction = tf.equal(tf.argmax(y,1),tf.arg_max(prediction,1))#argmax返回一维张量最大值（也就是1，不是0）所在的位置

#求准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))#cast（a,b）a转化为b类型
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(51):
        # sess.run(tf.assign(lr,0.001 *(0.95 ** epoch))) #tf.assign(a,b) 每次调用tf.assign,b都执行一次，并且赋值给a
        #开始时数混乱，所以学习率大，然后随着收敛则学习率越来越少
        for batch in range(n_batch):
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:1.0})
        learning_rate = sess.run(lr)
        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.0})
        print("iter " + str(epoch) + ",Testing Accuracy" + str(acc)+",Learning Rate="+str(learning_rate))
sess.close()