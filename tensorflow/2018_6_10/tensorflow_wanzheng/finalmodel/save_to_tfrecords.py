import tensorflow as tf
import os
from PIL import Image

TFRECORD_DIR = 'C:/Users/baicol/PycharmProjects/tensorflow/learn_tfrecord_file/tfrecord'
IMAGE_DIR = 'C:/Users/baicol/Desktop/tianchi/part2/all_image'
LABEL_DIR = 'C:/Users/baicol/Desktop/tianchi/part2/all_text'
NUM_TEST = 1000

###################################################################
filePath = "C:/Users/baicol/Desktop/tianchi/part2/label/"   #所有的汉字的目录文件
def _gen_dict():
    dic = []
    for filename in os.listdir(filePath):
        if not filename.startswith("."):
            with open(filePath + filename, encoding='utf-8') as file:
                for line in file.readlines():
                    content = line.split(",")[8]
                    if "###" not in content:
                        for c in content:
                            if c != '\n':
                                dic.append(c)
    for c in [chr(x) for x in range(33, 127)]:
        dic.append(c)
    d = list(set(dic))
    with open("tf_dictset_test.txt", 'w+', encoding='utf-8') as out:  #所有汉字集中存放文件
        for c in d:
            out.write(c + '\n')
    return d

dic = _gen_dict()
###################################################################


def _tfrecord_exist(tfrecord_dir):
    for type in ['train','test']:
        path = os.path.join(tfrecord_dir,type+'.tfrecords')
        if tf.gfile.Exists(path):
            return True
    return False

def _get_path_image_or_label(image_dir):
    image_path_list=[]
    for image_name in os.listdir(image_dir):
        path = os.path.join(image_dir,image_name)
        image_path_list.append(path)
    return image_path_list

def _processing_image(image_path_item):
    # image_data= Image.open(image_path_item).tobytes()
    image_data = tf.gfile.FastGFile(image_path_item, 'rb').read()
    return image_data

def _processing_label(label_path_item):
    text = tf.gfile.FastGFile(label_path_item).readline().strip('\n')  #重要
    label_data = [dic.index(x) + 1 for x in text]
    return label_data

def _byte_feature(value):
    return tf.train.Feature(bytes_list = tf.train.BytesList(value=[value]))
def _int64_feature(value):
    if not isinstance(value,(tuple,list)):
        value=[value]
    return tf.train.Feature(int64_list = tf.train.Int64List(value=value))

def _get_example(image_data,label_data):
    return tf.train.Example(features = tf.train.Features(feature={
        'image':_byte_feature(image_data),
        'label':_int64_feature(label_data)
    }))

def _create_tfrecord_file(type,image_list,label_list):
    assert type in ['test','train']
    tfrecord_file_path = os.path.join(TFRECORD_DIR,type+'.tfrecords')
    with tf.python_io.TFRecordWriter(tfrecord_file_path) as tf_write:
        for image_path_item,label_path_item in zip(image_list,label_list):
            print(image_path_item)
            print(label_path_item)

            image_data = _processing_image(image_path_item)
            lable_data = _processing_label(label_path_item)

            example = _get_example(image_data,lable_data)

            tf_write.write(example.SerializeToString())

if __name__=='__main__':
    if _tfrecord_exist(TFRECORD_DIR):
        print('tfrecord exists!')
    else:
        all_image_path_list = _get_path_image_or_label(IMAGE_DIR)
        all_label_path_list = _get_path_image_or_label(LABEL_DIR)

        train_image_path_list = all_image_path_list[NUM_TEST:]
        train_label_path_list = all_label_path_list[NUM_TEST:]

        test_image_path_list = all_image_path_list[:NUM_TEST]
        test_label_path_list = all_label_path_list[:NUM_TEST]

        _create_tfrecord_file('test',test_image_path_list,test_label_path_list)
        # _create_tfrecord_file('train',train_image_path_list,train_label_path_list)

        print('train_set_len',len(train_image_path_list))
        print('test_set_len',len(test_image_path_list))
        print('tfrecord file created successfully!')