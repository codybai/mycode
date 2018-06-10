import  tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#使用numpy生成200个随机点
x_data = np.linspace(-0.5,0.5,200)[:,np.newaxis] #生成在-0.5～0.5之间的均匀分布的点
noise = np.random.normal(0,0.02,x_data.shape)
y_data = np.square(x_data)+noise

#定义两个占位符
x = tf.placeholder(tf.float32,[None,1]) #[None,1]指的是形状，1列  #会出现在喂值操作中
y = tf.placeholder(tf.float32,[None,1])

#定义神经网络中间层
Weights_L1 = tf.Variable(tf.random_normal([1,10]))
biases_L1 = tf.Variable(tf.zeros([1,10]))
Wx_plus_b_L1 = tf.matmul(x,Weights_L1)+biases_L1
L1 = tf.nn.tanh(Wx_plus_b_L1)

#定义输出层
Weights_L2 = tf.Variable(tf.random_normal([10,1]))
biases_L2 = tf.Variable(tf.zeros([1,1]))
Wx_plus_b_L2 = tf.matmul(L1,Weights_L2)+biases_L2
predection = tf.nn.tanh(Wx_plus_b_L2)

#定义代价函数
loss = tf.reduce_mean(tf.square(y-predection))

#使用梯度下降法优化代价函数
train_step  = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    #变量初始化
    sess.run(init)
    for _ in range(2000):
        sess.run(train_step,feed_dict={x:x_data,y:y_data})#喂值
    #获得预测值
    predection_value = sess.run(predection,feed_dict={x:x_data})

    #画图
    plt.figure()    #
    plt.scatter(x_data,y_data)  #scatter 定义散点图，打印样本点
    plt.plot(x_data,predection_value,'r-',lw=5)  #打印预测点 plot是连线
                                                 # 'r-': r = red   -=实线
                                                 # lw是粗细
    plt.show()

