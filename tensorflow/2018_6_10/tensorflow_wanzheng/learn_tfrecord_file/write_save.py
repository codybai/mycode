import tensorflow as tf
import os
import numpy as np
TFRECORD_DIR = 'tfrecord'
IMAGE_DIR = 'C:/Users/baicol/Desktop/tianchi/part2/all_image'
LABEL_DIR = 'C:/Users/baicol/Desktop/tianchi/part2/all_text'
NUM_TEST = 4066  #测试集有4066个

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

def _tfrecord_exist(dir):
    for type in ['test','train']:
        path = os.path.join(dir,type+'.tfrecords')
        if tf.gfile.Exists(path):
            return True
    return False

def _get_paths_image_or_label(dir):
    path_list = []
    for filename in os.listdir(dir):
        path = os.path.join(dir,filename)
        path_list.append(path)
    return path_list
def _processing_image(image_dir_name):
    image_raw_data = tf.gfile.FastGFile(image_dir_name,'rb').read()

    image_data = tf.image.decode_png(image_raw_data)
    image_data = tf.image.convert_image_dtype(image_data,dtype=tf.float32)   #已经归一化了
    #此处添加对图像的处理
    return image_data
def _processing_label(label_dir_name):
    #此处根据数据调整标签处理方式
    with open(label_dir_name,encoding='utf-8') as label_file:
        ###################################################################
        text = label_file.readline().strip('\n')

        label_data = [dic.index(x) + 1 for x in text]
        ###################################################################
    return label_data

def _byte_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))#c
def _int64_feature(value):
    if not isinstance(value,(tuple,list)):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))#c

def _gen_example(image_data,label_data):
    return tf.train.Example(features =tf.train.Features(feature={
        'image':_byte_feature(np.array(image_data).tobytes()),
        'image_h':_int64_feature(32),
        'image_w':_int64_feature(256),
        'image_channel':_int64_feature(3),
        'label':_int64_feature(label_data)
    }))
def _get_tfrecords(type,image_list,label_list):
    assert type in ['train','test']

    with tf.Session() as sess:
        tfrecord_file_path = os.path.join(TFRECORD_DIR,type+'.tfrecords')
        with tf.python_io.TFRecordWriter(tfrecord_file_path) as write:
            for image_item,label_item in zip(image_list,label_list):
                print(image_item)
                print(label_item)
                image_data = _processing_image(image_item)
                label_data = _processing_label(label_item)
                example = _gen_example(image_data,label_data)
                write.write(example.SerializeToString())

if __name__ == '__main__':
    if _tfrecord_exist(TFRECORD_DIR):
        print('tfrecord exist!')
    else:
        #获取image label 文件目录列表
        all_image_path_list = _get_paths_image_or_label(IMAGE_DIR)
        all_label_path_list = _get_paths_image_or_label(LABEL_DIR)

        #划分数据集 假设有一个独立的数集，没有被划分
        train_image_path_list = all_image_path_list[NUM_TEST:]
        train_label_path_list = all_label_path_list[NUM_TEST:]

        test_image_path_list  = all_image_path_list[:NUM_TEST]
        test_label_path_list  = all_label_path_list[:NUM_TEST]

        #创建Tfrecord文件
        #创建训练集文件
        _get_tfrecords('train',train_image_path_list,train_label_path_list)
        #创建测试集文件
        _get_tfrecords('test',test_image_path_list,test_label_path_list)



