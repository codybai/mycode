import tensorflow as tf
import numpy as np
from PIL import Image
import os
TFRECORD_DIR = 'tfrecord'
imagepath='C:/Users/baicol/Desktop/tianchi/part2/all_image'
labelpath=''
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
with tf.Session() as sess:
    tfrecordpath = os.path.join(TFRECORD_DIR,'.tfrecords')
    with tf.python_io.TFRecordWriter(tfrecordpath) as writer:
        for imagename in os.listdir(imagepath):
            im_dir = os.path.join(imagepath,imagename)
            # image = Image.open(im_dir)
            image_data = tf.gfile.FastGFile(im_dir,'rb').read()
            image = tf.image.decode_png(image_data)
            print(im_dir)
            writer.write(tf.train.Example(features = tf.train.Features(feature={
                'image':_bytes_feature(np.array(image).tobytes())
            })).SerializeToString())


