import tensorflow as tf
import os
from PIL import Image

TFRECORD_DIR = './tfrecord'
IMAGE_DIR = 'C:/Users/codyb/Desktop/dataset_kaggledogvscat/dir'
NUM_TEST = 1000

#使用此文件前请确保已经保证照片大小一致。

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
    image_data = tf.gfile.FastGFile(image_item,'rb').read()  #此处不要用PIL等一些其他的库，效率太低，用FastGFile效率搞，直接就是string\bytes了
    return image_data

def _processing_label(label_item):
    label_data = [label_item]    #加不加中括号无所谓A中有判断
    return label_data

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    if not isinstance(value,(tuple,list)):  #A
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def _get_example(image_data,label_data):
    return tf.train.Example(features = tf.train.Features(feature={
        'image':_bytes_feature(image_data),
        'label':_int64_feature(label_data)
    }))

def _get_tfrecords_file(type,image_paths):
    assert type in ['test','train']
    dog_num = 0
    cat_num = 0
    trecords_full_path = os.path.join(TFRECORD_DIR,type+'.tfrecords')
    with tf.python_io.TFRecordWriter(trecords_full_path) as tf_writer:
        i = 0
        for image_item in image_paths:
            # try:
            # print(image_item)
            # print(label_item)
            i+=1
            if "\cat." in image_item:
                if cat_num<2000:
                    label_item=1
                    cat_num += 1
                    print(i)
                    print("cat",cat_num)
            else:
                if dog_num<2000:
                    label_item=0
                    dog_num += 1
                    print("dog",dog_num)

            image_data = _processing_image(image_item)
            label_data = _processing_label(label_item)
            # print(image_data)
            # print(label_data)
            example = _get_example(image_data,label_data)
            tf_writer.write(example.SerializeToString())
            # except:
            #     print('convert to tfreacords failed!')
            #     return

if __name__=='__main__':
    if _tfrecords_exist(TFRECORD_DIR):
        print('tfrecords exists!')
    else:
        #获取image path list
        all_image_path_list = _get_paths_list_image_or_label(IMAGE_DIR)


        #划分训练集和测试集
        train_image_path_list = all_image_path_list[:]
        _get_tfrecords_file('train',train_image_path_list)

        print('create tfrecord file successfully!')