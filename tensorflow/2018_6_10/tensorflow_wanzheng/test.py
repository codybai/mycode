import tensorflow as tf



def get_next_batch(type, batch_size):
    assert type in ['test', 'train']

    min_after_dequeue = 1000
    reader = tf.TFRecordReader()
    tfrecord = 'C:/Users/baicol/PycharmProjects/tensorflow/learn_tfrecord_file/tfrecord/'
    file_queue = tf.train.string_input_producer([tfrecord+type+'.tfrecords'])
    _, serialize_example = reader.read(queue=file_queue)

    features = tf.parse_single_example(serialize_example, features={
        'image': tf.FixedLenFeature([], tf.string),
        'label': tf.VarLenFeature(tf.int64)
    })

    image = tf.decode_raw(features['image'], tf.uint8)
    image1 = tf.reshape(image, [32,256,3])
    label_sp = features['label']

    input, target_sp = tf.train.shuffle_batch([image1, label_sp],
                                              batch_size=batch_size,
                                              capacity=min_after_dequeue + 3 * batch_size,
                                              min_after_dequeue=min_after_dequeue,
                                              num_threads=1)
    # target = tf.sparse_to_dense(sparse_indices=target_sp.indices, output_shape=target_sp.dense_shape,
    #                             sparse_values=target_sp.values)
    return input, target_sp


def tell_accuracy(predict, ground_truth):
    predict_ = tf.sparse_to_dense(sparse_indices=predict.indices, output_shape=predict.dense_shape,sparse_values=predict.values)
    ground_truth_ =tf.sparse_to_dense(sparse_indices=ground_truth.indices, output_shape=ground_truth.dense_shape,sparse_values=ground_truth.values)

    equal = tf.equal(predict_, ground_truth_)
    acc = tf.reduce_mean(tf.cast(equal, dtype=tf.float32))
    return acc
x,y = get_next_batch('test',200)

epoch=12
with tf.Session() as sess:
    coord = tf.train.Coordinator()

    threads = tf.train.start_queue_runners(sess=sess,coord=coord)
    acc = tell_accuracy(y, y)
    print('epoch:', epoch, 'Accuracy:', acc.eval())

    coord.request_stop()
    coord.join(threads)