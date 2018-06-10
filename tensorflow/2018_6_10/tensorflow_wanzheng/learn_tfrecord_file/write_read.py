import tensorflow as tf
batch_size=200

def get_next_batch(type,batch_size):
    assert type in ['test','train']
    #定义变量
    print('定义变量')
    min_after_dequeue = 1000
    reader = tf.TFRecordReader()

    #开始读取
    print('开始读取')
    file_queue = tf.train.string_input_producer(['tfrecord/'+type+'.tfrecords'])
    _,serialize_example = reader.read(queue=file_queue)
    #接收特征
    print('接收特征')
    features = tf.parse_single_example(serialize_example,features={
        'image':tf.FixedLenFeature([],tf.string),
        'image_h':tf.FixedLenFeature([],tf.int64),
        'image_w':tf.FixedLenFeature([],tf.int64),
        'image_channel':tf.FixedLenFeature([],tf.int64),
        'label':tf.VarLenFeature(tf.int64)
    })
    #解析特征
    print('解析特征')
    image = tf.decode_raw(features['image'],tf.uint8)
    image_h = tf.cast(features['image_h'],tf.int64)
    image_w = tf.cast(features['image_w'],tf.int64)
    image_channel = tf.cast(features['image_channel'],tf.int64)
    shape = tf.stack([image_h,image_w,image_channel])
    image1 = tf.reshape(image,shape)  #必须
    label_sp = features['label']
    #封装batch
    print('封装batch')
    input,target_sp = tf.train.shuffle_batch([image1,label_sp],
                                          batch_size=batch_size,
                                          capacity=min_after_dequeue+3*batch_size,
                                          min_after_dequeue=min_after_dequeue,
                                          num_threads=10)
    target = tf.sparse_to_dense(sparse_indices=target_sp.indices,output_shape=target_sp.dense_shape,sparse_values=target_sp.values)
    return input,target

batch_x, batch_y = get_next_batch('test',batch_size=batch_size)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)


    for _ in range(60):
        print(batch_x.eval())
    coord.request_stop()
    coord.join(threads)