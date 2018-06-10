import tensorflow as tf
import numpy as np
import mnist_inference
import os
from tensorflow.examples.tutorials.mnist import input_data
BATCH_SIZE = 100

#神经网络的参数
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY= 0.99
REGULARAZTION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY=0.99  #滑动平均的值为接近1的值
# global_step = tf.Variable(0.0,trainable=False)
# learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE,
#                                            global_step,
#                                            TRAINING_STEPS,
#                                            LEARNING_RATE_DECAY,
#                                            staircase=True)
#模型保存的路径和文件名
MODEL_SAVE_PATH = ''
MODEL_NAME = 'model.ckpt'

def train(mnist):
    #定义输入输出placeholder.
    # x = tf.placeholder(tf.float32,[None,mnist_inference.INPUT_NODE],name='x-input')
    y_=tf.placeholder(tf.float32,[None,mnist_inference.OUTPUT_NODE],name='y-input')
    x = tf.placeholder(tf.float32, [BATCH_SIZE,
                                    mnist_inference.IMAGE_SIZE,
                                    mnist_inference.IMAGE_SIZE,
                                    mnist_inference.NUM_CHANNELS],
                       name='x-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)

    y=mnist_inference.inference(x,True,regularizer)
    global_step = tf.Variable(0,trainable=False)
    #定义滑动平均
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY,global_step)
    #tf.trainable_variables()是所有可以训练变量的列表
    #tf.all_variables()是返回所有变量的列表，所有才有trainable = bool这个参数
    variable_averages_op = variable_averages.apply(tf.trainable_variables())

    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=tf.arg_max(y_,1),logits=y)

    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean+tf.add_n(tf.get_collection(name='loss'))#对应

    learning_rate = tf.train.exponential_decay(learning_rate=LEARNING_RATE_BASE,
                                               global_step=global_step,
                                               decay_steps=mnist.train.num_exples / BATCH_SIZE,  #本质就是多少轮衰减一次，这里取的是所有的训练集跑完一遍然后衰减一次
                                               decay_rate=LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss=loss,global_step=global_step)

    with tf.control_dependencies([train_step,variable_averages_op]):  #借鉴
        train_op = tf.no_op(name='train')

    #初始化Tensorflow持久化类
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(TRAINING_STEPS):
            xs,ys  = mnist.train.next_batch(BATCH_SIZE)
            reshaped_xs = np.reshape(xs, (BATCH_SIZE,
                                          mnist_inference.IMAGE_SIZE,
                                          mnist_inference.IMAGE_SIZE,
                                          mnist_inference.NUM_CHANNELS))
            _,loss_value,step = sess.run([train_op,loss,global_step],feed_dict={x:reshaped_xs,y_:ys})
            #每1000轮保存一次模型
            if i % 1000 ==0:
                print("After %d training step(s), loss on training batch is %g." % (step,loss_value))
                saver.save(sess,os.path.join(MODEL_SAVE_PATH,MODEL_NAME),global_step=global_step)
def main(argv=None):
    mnist = input_data.read_data_sets('/path/to/mnist_data',one_hot=True)
    train(mnist)
if __name__ == '__main__':
    tf.app.run()











































