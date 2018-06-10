import tensorflow as tf


##########################################
#fetch:就是能够同时运行两个op
# input1 = tf.constant(3.)
# input2 = tf.constant(2.)
# input3 = tf.constant(5.)
#
# add = tf.add(input2,input3)    #op1
# mul = tf.multiply(input1,add)  #op2
# init = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     result = sess.run([mul,add])
#     print(result)
##########################################


##########################################
#feed

input1 = tf.placeholder(tf.float32)#定义32位的浮点占位符
input2 = tf.placeholder(tf.float32)#同上
output = tf.multiply(input1,input2)#变量还没有赋值，可以通过feed来传值

with tf.Session() as sess:
    print(sess.run(output,feed_dict={input1:[7.],input2:[2.]}))#feed的数据以字典的形式传入
sess.close()
