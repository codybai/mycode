import tensorflow as tf
import os
from PIL import Image

TFRECORD_DIR = 'tfrecord'
# IMAGE_DIR = 'C:/BaiduyunDownLoad/猫狗大战数据集/train'
# NUM_TEST = 1000
IMAGE_DIR = 'C:/BaiduyunDownLoad/猫狗大战数据集/test1/'


def _tfrecords_exist(tfrecord_dir):
    for type in ['train','test']:
        tfrecord_name = os.path.join(tfrecord_dir,type+'.tfrecords')
        if tf.gfile.Exists(tfrecord_name):
            return True
    return False

def _get_paths_list_image_or_label(dir):
    path_list=[]
    for filename in os.listdir(dir):
        path = os.path.join(dir,filename)
        path_list.append(path)
    return path_list

def _processing_image(image_item):
    image_data = tf.gfile.FastGFile(image_item,'rb').read()
    return image_data


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    if not isinstance(value,(tuple,list)):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def _get_example(image_data,label_data):
    return tf.train.Example(features = tf.train.Features(feature={
        'image':_bytes_feature(image_data),
        'label':_int64_feature(label_data)
    }))

def _get_tfrecords_file(type,image_paths):
    assert type in ['test','train']
    trecords_full_path = os.path.join(TFRECORD_DIR,type+'.tfrecords')
    with tf.python_io.TFRecordWriter(trecords_full_path) as tf_writer:
        i = 0
        label = 0  #0是猫  1是狗
        for image_item in image_paths:
            try:
                # print(image_item)
                if  'dog' in image_item:
                    label=1
                # print(image_item,'type:',label)
                i+=1
                print(i)
                image_data = _processing_image(image_item)

                example = _get_example(image_data,label)
                tf_writer.write(example.SerializeToString())
            except:
                print('convert to tfreacords failed!')
                return

if __name__=='__main__':
    if _tfrecords_exist(TFRECORD_DIR):
        print('tfrecords exists!')
    else:
        #获取image path list
        all_image_path_list = _get_paths_list_image_or_label(IMAGE_DIR)

        # _get_tfrecords_file('train',train_image_path_list,train_label_path_list)
        _get_tfrecords_file('test',all_image_path_list)

        print('create tfrecord file successfully!')