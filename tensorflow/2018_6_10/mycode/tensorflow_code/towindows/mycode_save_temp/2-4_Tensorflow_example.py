import tensorflow as tf
import numpy as np

#使用numpy生成100个随机点
x_data = np.random.rand(100)
y_data = x_data*0.1 + 0.2  #直线

#构造一个线性模型  拟合上面直线
b = tf.Variable(0.)  #0.0随便什么值都可以
k = tf.Variable(0.)
y = k*x_data + b

#二次代价函数
loss = tf.reduce_mean(tf.square(y_data-y))#取平均值（一个平方）
#定义一个梯度下降进行优化（优化器）
optimizer = tf.train.GradientDescentOptimizer(0.2)#梯度下降学习率0.2
#最小化代价函数
train =optimizer.minimize(loss)  #最小化损失函数
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for step in range(201):
        sess.run(train)
        if step%20 == 0:
            print(step,sess.run([k,b]))
