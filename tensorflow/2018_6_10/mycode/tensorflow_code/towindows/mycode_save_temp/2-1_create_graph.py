import tensorflow as tf

m1 = tf.constant([[3,3]]) #op1
m2 = tf.constant([[2],[3]])#op2
result = tf.matmul(m1,m2)#op3

sess = tf.Session()

print(sess.run(result))
sess.close()