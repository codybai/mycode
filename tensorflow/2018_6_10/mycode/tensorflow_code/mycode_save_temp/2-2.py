import tensorflow as tf

#################################
# x = tf.Variable([1,2])
# a = tf.constant([3,3])
#
# sub = tf.subtract(x,a)
# add = tf.add(x, sub)
# init = tf.global_variables_initializer()
# with tf.Session() as sess:
#     # print sess.run(sub)
#     # print sess.run(add)
#     sess.run(init)
#     print(sess.run(sub))
#     print(sess.run(add))
##################################

##################################
#init variable
state = tf.Variable(0,name="counter")#初始化变量
new_value = tf.add(state,1) # new_value = 1+new_value
update = tf.assign(state,new_value)#相当于复制  state = new_value
init = tf.global_variables_initializer()#初始化全局变量
with tf.Session() as sess:#打开Session
    sess.run(init)
    print(sess.run(state))
    for _ in range(5):
        sess.run(update)
        print(sess.run(state))
sess.close() #关闭session
