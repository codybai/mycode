import tensorflow as tf
from nets import nets_factory
import os
from PIL import Image
import numpy as np


#不同字符数量
CHAR_SET_LEN = 10
#
IMAGE_HEIGHT = 60

IMAGE_WIDTH = 160

BATCH_SIZE = 25

#tfrecord directory
TFRECORD_FILE = 'tfrecord/captcha/train.tfrecords'

#placeholder

x = tf.placeholder(tf.float32,[None,224,224])
y0 = tf.placeholder(tf.float32,[None])
y1 = tf.placeholder(tf.float32,[None])
y2 = tf.placeholder(tf.float32,[None])
y3 = tf.placeholder(tf.float32,[None])

#学习率
lr = tf.Variable(0.03,dtype=tf.float32)

#reads from tfrecords files

def read_and_decode(filename):
    #根据文件名生成一个队列
    filename_queue =  tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    #返回文件名和文件
    _,serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'image':tf.FixedLenFeature([],tf.string),
                                           'label0':tf.FixedLenFeature([],tf.int64),
                                           'label1':tf.FixedLenFeature([],tf.int64),
                                           'label2':tf.FixedLenFeature([],tf.int64),
                                           'label3':tf.FixedLenFeature([],tf.int64),
                                       })
    #获取照片数据
    image = tf.decode_raw(features['image'],tf.uint8)
    #tf.train.shuffle_batch必须确定shape
    image = tf.reshape(image,[224,224])
    #照片预处理
    image = tf.cast(image,tf.float32) / 255.0  #图片归一化
    image = tf.subtract(image,0.5)
    image = tf.multiply(image,2.0)
    #获取label
    label0 = tf.cast(features['label0'],tf.int32)
    label1 = tf.cast(features['label1'],tf.int32)
    label2 = tf.cast(features['label2'],tf.int32)
    label3 = tf.cast(features['label3'],tf.int32)

    return image,label0,label1,label2,label3

#获取图片数据和标签
image,label0,label1,label2,label3 = read_and_decode(TFRECORD_FILE)

#使用shuffle_batch可以随机打乱
image_batch,label_batch0,label_batch1,label_batch2,label_batch3 = tf.train.shuffle_batch(
    [image,label0,label1,label2,label3],
    batch_size= BATCH_SIZE,
    capacity=50000,
    min_after_dequeue=10000,
    num_threads=1)

#定义网络结构
train_network_fn = nets_factory.get_network_fn(
    'alexnet_v2',
    num_classes=CHAR_SET_LEN,
    weight_decay=0.0005,
    is_training=True)

with tf.Session() as sess:
    #[bs,h,w,channels]
    input = tf.reshape(x,[BATCH_SIZE,224,224,1])
    #数据输入网络，获得输出值
    logits0,logits1,logits2,logits3,end_points = train_network_fn(input)

    #把标签换成one_hot形式
    one_hot_label0 = tf.one_hot(indices=tf.cast(y0,tf.int32),depth=CHAR_SET_LEN)
    one_hot_label1 = tf.one_hot(indices=tf.cast(y1,tf.int32),depth=CHAR_SET_LEN)
    one_hot_label2 = tf.one_hot(indices=tf.cast(y2,tf.int32),depth=CHAR_SET_LEN)
    one_hot_label3 = tf.one_hot(indices=tf.cast(y3,tf.int32),depth=CHAR_SET_LEN)


    #计算Loss
    loss0 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=one_hot_label0,logits=logits0))
    loss1 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=one_hot_label1,logits=logits1))
    loss2 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=one_hot_label2,logits=logits2))
    loss3 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=one_hot_label3,logits=logits3))


    total_loss = (loss0+loss1+loss2+loss3) / 4.0

    optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(total_loss)

    #计算准确率
    correct_predict0 = tf.equal(tf.argmax(input=one_hot_label0,axis=1),tf.argmax(input=logits0,axis=1))
    correct_predict1 = tf.equal(tf.argmax(input=one_hot_label1,axis=1),tf.argmax(input=logits1,axis=1))
    correct_predict2 = tf.equal(tf.argmax(input=one_hot_label2,axis=1),tf.argmax(input=logits2,axis=1))
    correct_predict3 = tf.equal(tf.argmax(input=one_hot_label3,axis=1),tf.argmax(input=logits3,axis=1))

    accuracy0 = tf.reduce_mean(tf.cast(correct_predict0, tf.float32))
    accuracy1 = tf.reduce_mean(tf.cast(correct_predict1, tf.float32))
    accuracy2 = tf.reduce_mean(tf.cast(correct_predict2, tf.float32))
    accuracy3 = tf.reduce_mean(tf.cast(correct_predict3, tf.float32))

    #用于保存模型
    saver = tf.train.Saver()

    #初始化
    sess.run(tf.global_variables_initializer())

    #创建一个线程协调器管理线程
    coord = tf.train.Coordinator()

    #启动QueueRunner 此时文件名已经进入队列
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)

    for i in range(6001):
        #获得一个批次的数据和标签
        b_image,b_label0,b_label1,b_label2,b_label3 = sess.run([image_batch,label_batch0,label_batch1,label_batch2,label_batch3])

        #优化模型
        sess.run(optimizer,feed_dict={x:b_image,y0:b_label0,y1:b_label1,y2:b_label2,y3:b_label3})

        #每迭代二十次计算一次loss和准确率
        if i %20 == 0:
            #每迭代2000次降低一次学习率
            if i% 2000 == 0:
                sess.run(tf.assign(lr,lr/3))
            acc0,acc1,acc2,acc3,loss_ = sess.run([accuracy0,accuracy1,accuracy2,accuracy3,total_loss,],feed_dict={
                                                                                                                x :b_image,
                                                                                                                y0:b_label0,
                                                                                                                y1:b_label1,
                                                                                                                y2:b_label2,
                                                                                                                y3:b_label3
                                                                                                            })
            learning_rate = sess.run(lr)
            print('Iter:%d Loss:%.3f Accuracy:%.2f,%.2f,%.2f,%.2f  Learning_rate: %.4f' % (i,loss_,acc0,acc1,acc2,acc3,learning_rate))
        if i == 6000:
            saver.save(sess,'/yzmmodel/model.model',global_step=i)
            break
    #线程关闭
    coord.request_stop()
    #等待所有线程关闭之后，这一函数才会返回
    coord.join(threads=threads)






















