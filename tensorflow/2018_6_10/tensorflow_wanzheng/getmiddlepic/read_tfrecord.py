
import tensorflow as tf
import os
batch_size = 100
min_after_dequeue=1000
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
    return batch_image,batch_label,_
x,y ,_= get_next_batch('train',batch_size)
init = tf.global_variables_initializer()
with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess,coord)
    sess.run(init)
    for i in range(100000):
        xx,yy = sess.run([x,y])
        for xs,ys in zip(xx,yy):
            print(xs,ys)

    # for i in xx:
    #     print(tf.shape(i).eval())

    coord.request_stop()
    coord.join(threads)