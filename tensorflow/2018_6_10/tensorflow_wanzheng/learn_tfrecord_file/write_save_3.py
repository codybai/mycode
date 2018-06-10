import tensorflow as tf
import os
from PIL import Image

TFRECORD_DIR = 'tfrecord'
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
    image_data = Image.open(image_item).tobytes()  #血的教训
    return image_data

def _processing_label(label_item):
    label_text = tf.gfile.FastGFile(label_item).readline().strip('\n')
    label_data = [dic.index(x) + 1 for x in label_text]
    return label_data

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

def _get_tfrecords_file(type,image_paths,label_paths):
    assert type in ['test','train']
    trecords_full_path = os.path.join(TFRECORD_DIR,type+'.tfrecords')
    with tf.python_io.TFRecordWriter(trecords_full_path) as tf_writer:
        for image_item,label_item in zip(image_paths,label_paths):
            try:
                print(image_item)
                print(label_item)
                image_data = _processing_image(image_item)
                label_data = _processing_label(label_item)

                example = _get_example(image_data,label_data)
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
        #获取label_path_list
        all_label_path_list = _get_paths_list_image_or_label(LABEL_DIR)

        #划分训练集和测试集
        train_image_path_list = all_image_path_list[NUM_TEST:]
        train_label_path_list = all_label_path_list[NUM_TEST:]

        test_image_path_list = all_image_path_list[:NUM_TEST]
        test_label_path_list = all_label_path_list[:NUM_TEST]

        # _get_tfrecords_file('train',train_image_path_list,train_label_path_list)
        _get_tfrecords_file('test',test_image_path_list,test_label_path_list)

        print('create tfrecord file successfully!')