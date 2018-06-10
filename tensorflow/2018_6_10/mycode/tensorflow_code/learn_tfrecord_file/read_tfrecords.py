import tensorflow as tf
from matplotlib import pyplot as plt
batch_size=200
min_after_dequeue=1000

reader = tf.TFRecordReader()
filename_queue = tf.train.string_input_producer(['tfrecord/train.tfrecords'])

_,serialized_example = reader.read(queue=filename_queue)

features = tf.parse_single_example(serialized_example,features = {
            'image':tf.FixedLenFeature([],tf.string),
            'image_h':tf.FixedLenFeature([],tf.int64),
            'image_w':tf.FixedLenFeature([],tf.int64),
            'image_channel':tf.FixedLenFeature([],tf.int64),
            'label':tf.VarLenFeature(tf.int64)
            })

image = tf.decode_raw(features['image'],tf.uint8)

image_h = tf.cast(features['image_h'],tf.int64)
image_w = tf.cast(features['image_w'],tf.int64)
image_channel = tf.cast(features['image_channel'],tf.int64)
shape = tf.stack([image_h,image_w,image_channel])
image = tf.reshape(image,[32,192,3])
label_data = features['label']


image_batch,label_batch  = tf.train.shuffle_batch([image,label_data],batch_size=batch_size,min_after_dequeue=1000,capacity=min_after_dequeue+3*batch_size,num_threads=1)


with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)

    for _ in range(10):
        img,lab = sess.run([image_batch,label_batch])
        print(sess.run(tf.sparse_to_dense(lab.indices,lab.dense_shape,lab.values)))
        print('---------')

    coord.request_stop()
    coord.join(threads)