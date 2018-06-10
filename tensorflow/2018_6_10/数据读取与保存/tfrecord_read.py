
import tensorflow as tf
import os
from PIL import Image
batch_size = 100
min_after_dequeue=1000     #无论数据集是什么0，1，100000000，多大，都可以设置成1000
def get_next_batch(type,batch_size):
    assert type in ['test','train']

    TFRECORD_DIR = 'C:/Users/codyb/PycharmProjects/net_homework/tfrecord/'
    filename = os.path.join(TFRECORD_DIR,type+'.tfrecords')
    file_queue = tf.train.string_input_producer([filename])
    read = tf.TFRecordReader()
    _,serialize_example = read.read(queue=file_queue)

    features = tf.parse_single_example(serialize_example,features={
        'image':tf.FixedLenFeature([],tf.string),
        'label':tf.VarLenFeature(tf.int64)    #可变的，不管是什么类型的都行
    })

    image_data = features['image']      #不用强转成tf.uint8,直接使用tf.string格式，因为decode_jped/png()函数会吧string格式解析成图片格式
    image_data = tf.image.decode_jpeg(image_data, channels=3)   #与tf.FastFile配对使用
    #总结：
    image_data = tf.reshape(image_data,[256,256,3])   #这里的大小，必须与生成tfrecordfile的image的原始尺寸相等，不然报错
    label_data = features['label']    #不用转换成tf.int32或者其他类型                #sparse_tensor 类型，用这中类型比较灵活，可以同时存放定长和不定长的数据label，凡是label,非常推荐使用sparse_tensor
    #因为要放入shufflebatch里面时候，需要确定长度大小，直接使用sparsetensor,就不用强制确定长度了
    batch_image,batch_label = tf.train.shuffle_batch([image_data,label_data],
                                                     batch_size=batch_size,
                                                     capacity=min_after_dequeue+3*batch_size,
                                                     min_after_dequeue=min_after_dequeue,
                                                     num_threads=1)     #这个函数里面的基本不用变，报错基本上是其他地方的原因
    return batch_image,batch_label
x,y = get_next_batch('train',batch_size)
init = tf.global_variables_initializer()
y=tf.sparse_to_dense(y.indices,y.dense_shape,y.values)
with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess,coord)
    sess.run(init)
    for i in range(100000):
        xx,yy = sess.run([x,y])
        print(xx,yy)
    # for i in xx:
    #     print(tf.shape(i).eval())

    coord.request_stop()
    coord.join(threads)