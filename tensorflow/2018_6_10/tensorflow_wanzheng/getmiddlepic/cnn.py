import tensorflow as tf
import os
total_images = 25000
batch_size = 10
n_batchs = total_images // batch_size
min_after_dequeue=1000
global_step = tf.Variable(tf.constant(0),trainable=False)
def get_next_batch(type,batch_size):
    assert type in ['test','train']

    TFRECORD_DIR = './tfrecord/'
    filename = os.path.join(TFRECORD_DIR,type+'.tfrecords')
    file_queue = tf.train.string_input_producer([filename])
    read = tf.TFRecordReader()
    _,serialize_example = read.read(queue=file_queue)

    features = tf.parse_single_example(serialize_example,features={
        'image':tf.FixedLenFeature([],tf.string),
        'label':tf.FixedLenFeature([],tf.int64)
    })

    image_data = features['image']
    image_data = tf.image.decode_png(image_data, channels=3)

    image_data = tf.reshape(image_data,[256,256,3])
    label_data = features['label']

    batch_image,batch_label = tf.train.shuffle_batch([image_data,label_data],
                                                     batch_size=batch_size,
                                                     capacity=min_after_dequeue+3*batch_size,
                                                     min_after_dequeue=min_after_dequeue,
                                                     num_threads=1)
    return batch_image,batch_label

x,y= get_next_batch('train',batch_size)
x = tf.cast(x,tf.float32)
y = tf.one_hot(y,2)
init = tf.global_variables_initializer()

# conv1[256,256,3]
in_conv1 = tf.reshape(x, shape=[batch_size, 256, 256, 3])
w_conv1 = tf.Variable(tf.truncated_normal(shape=[3, 3, 3, 64], stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1, shape=[64]))
result_conv1 = tf.nn.relu(tf.nn.conv2d(in_conv1, w_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
pool_conv1 = tf.nn.max_pool(result_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# conv2[128,128,64]
w_conv2 = tf.Variable(tf.truncated_normal(shape=[3, 3, 64, 128], stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1, shape=[128]))
result_conv2 = tf.nn.relu(tf.nn.conv2d(pool_conv1, w_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2)
pool_conv2 = tf.nn.max_pool(result_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# conv3[64,64,128]
w_conv3 = tf.Variable(tf.truncated_normal(shape=[3, 3, 128, 256], stddev=0.1))
b_conv3 = tf.Variable(tf.constant(0.1, shape=[256]))
result_conv3 = tf.nn.relu(tf.nn.conv2d(pool_conv2, w_conv3, strides=[1, 1, 1, 1], padding='SAME') + b_conv3)
# conv4[64,64,256]
w_conv4 = tf.Variable(tf.truncated_normal(shape=[3, 3, 256, 256], stddev=0.1))
b_conv4 = tf.Variable(tf.constant(0.1, shape=[256]))
result_conv4 = tf.nn.relu(tf.nn.conv2d(result_conv3, w_conv4, strides=[1, 1, 1, 1], padding='SAME') + b_conv4)
pool_conv4 = tf.nn.max_pool(result_conv4,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
# conv5[32,32,256]
w_conv5 = tf.Variable(tf.truncated_normal(shape=[3, 3, 256, 512], stddev=0.1))
b_conv5 = tf.Variable(tf.constant(0.1, shape=[512]))
result_conv5 = tf.nn.relu(tf.nn.conv2d(pool_conv4, w_conv5, strides=[1, 1, 1, 1], padding='SAME') + b_conv5)

w_conv6 = tf.Variable(tf.truncated_normal(shape=[3, 3, 512, 512], stddev=0.1))
b_conv6 = tf.Variable(tf.constant(0.1, shape=[512]))
result_conv6 = tf.nn.relu(tf.nn.conv2d(result_conv5, w_conv6, strides=[1, 1, 1, 1], padding='SAME') + b_conv6)
pool_conv6 = tf.nn.max_pool(result_conv6,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
#[16,16,512]

w_conv8 = tf.Variable(tf.truncated_normal(shape=[3, 3, 512, 512], stddev=0.1))
b_conv8 = tf.Variable(tf.constant(0.1, shape=[512]))
result_conv8 = tf.nn.relu(tf.nn.conv2d(pool_conv6, w_conv8, strides=[1, 1, 1, 1], padding='SAME') + b_conv8)
pool_conv7 = tf.nn.max_pool(result_conv8,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
infcl = tf.reshape(pool_conv7,[batch_size,8*8*512])
#[bs,8*8*512]
#fc1
w_fcl = tf.Variable(tf.truncated_normal(shape=[8*8*512,1024],stddev=0.1))
b_fcl = tf.Variable(tf.constant(0.1,shape=[1024]))
result_fcl = tf.matmul(infcl,w_fcl)+b_fcl
#[bs,1024]
#fc2
w_fcl2 = tf.Variable(tf.truncated_normal(shape=[1024,2],stddev=0.1))
b_fcl2= tf.Variable(tf.constant(0.1,shape=[2]))
result_fcl2 = tf.matmul(result_fcl,w_fcl2)+b_fcl2
result_fcl2 = tf.nn.softmax(result_fcl2)
#[bs,2]


cost  = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=result_fcl2))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cost)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess, coord)
    sess.run(init)
    saver = tf.train.Saver()

    for epoch in range(3):
        for batch in range(n_batchs):
            train_step_,cost_,global_step_ = sess.run([train_step,cost,global_step])
            print('epoch:',epoch,',batchs:',batch,'/',n_batchs,',global_step:',global_step_,',cost:',cost_,',learn_rate:',1e-3)
            if batch % 100 == 0:
                saver.save(sess,'./model/model.ckpt',global_step=global_step)
    coord.request_stop()
    coord.join(threads)