import tensorflow as tf

batch_size=100

def get_next_batch(batch_size):

    min_after_dequeue=1000
    reader = tf.TFRecordReader()
    filename_queue = tf.train.string_input_producer(['tfrecord/test.tfrecords'])

    _,serialized_example = reader.read(queue=filename_queue)

    features = tf.parse_single_example(serialized_example,features = {
                'image':tf.FixedLenFeature([],tf.string),

                'label':tf.VarLenFeature(tf.int64)
                })

    image = tf.decode_raw(features['image'],tf.uint8)



    image = tf.reshape(image,[32,256,3])
    label_data = features['label']
    image_batch,label_batch  = tf.train.shuffle_batch([image,label_data],
                                                      batch_size=batch_size,
                                                      min_after_dequeue=1000,
                                                      capacity=min_after_dequeue+3*batch_size,
                                                      num_threads=10)
    label_batch = tf.sparse_to_dense(label_batch.indices,label_batch.dense_shape,label_batch.values)
    return image_batch,label_batch

x, y = get_next_batch(1)
with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)

    for _ in range(1000):
        print(x.eval())
        print(y.eval())

    coord.request_stop()
    coord.join(threads)