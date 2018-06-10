import  tensorflow as tf

a = 57
b = tf.one_hot(indices=tf.cast(a,tf.int32),depth=100)

c = 57
dd = 59
d = tf.one_hot(indices=tf.cast(dd,tf.int32),depth=100)

equal = tf.equal(tf.argmax(b,1),tf.argmax(d,1))
sum = tf.reduce_mean(tf.cast(equal,tf.float32))
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    aa=sess.run(sum)

