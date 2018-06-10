# import tensorflow as tf
# from .config import data_path
# from .config import min_after_dequeue
def ylist_to_sparse(labellist):  #  直接用读取出来的data变成SparseTensor 所有的y    # called by get_next_batch
    indices = []
    values=[]
    max_row = 0
    max_col = 0
    y = labellist

    for idx,i in enumerate(y):
        if idx > max_row:
            max_row=idx
        for jdx, j in enumerate(i):    #循环编码
            y[idx][jdx] =j
            indices.append([idx,jdx])
            values.append(y[idx][jdx])
            if jdx>max_col:
                max_col=jdx
    shape=[max_row+1,max_col+1]
    return indices,values,shape



def decode_sparse_tensor(sparse_tensor):
    decoded_indexes = list()
    current_i = 0
    current_seq = []
    for offset, i_and_index in enumerate(sparse_tensor[0]):
        i = i_and_index[0]
        if i != current_i:
            decoded_indexes.append(current_seq)
            current_i = i
            current_seq = list()
        current_seq.append(offset)
    decoded_indexes.append(current_seq)
    result = []
    for index in decoded_indexes:
        result.append(decode_a_seq(index, sparse_tensor))
    return result


def decode_a_seq(indexes, spars_tensor):
    decoded = []
    for m in indexes:
        str = spars_tensor[1][m]
        decoded.append(str)
    return decoded

def report_accuracy(decoded_list, test_targets):
    original_list = decode_sparse_tensor(test_targets)
    detected_list = decode_sparse_tensor(decoded_list)
    original_list_len  = len(original_list)
    detected_list_len = len(detected_list)
    print('原始序列大小:',original_list_len)
    print('预测序列大小:',detected_list_len)
    true_numer = 0
    total_numer = original_list_len

    for origianal,detect in zip(original_list,detected_list):
        if origianal == detect:
            true_numer += 1
            print('--------------------------------')
            print('原始序列：', origianal)
            print('预测序列：', detect, '（正确）')
        else:
            print('原始序列：', origianal)
            print('预测序列：', detect, '（错误）')
    print('测试总数：', total_numer, '\n正确个数：', true_numer, "，\n正确率:", true_numer * 1.0 / total_numer)


def get_next_batch(type, batch_size):
    assert type in ['test', 'train']


    reader = tf.TFRecordReader()

    file_queue = tf.train.string_input_producer([data_path+ type + '.tfrecords'])
    _, serialize_example = reader.read(queue=file_queue)

    features = tf.parse_single_example(serialize_example, features={
        'image': tf.FixedLenFeature([], tf.string),
        'label': tf.VarLenFeature(tf.int64)
    })

    image = tf.decode_raw(features['image'], tf.uint8)
    image = tf.reshape(image, [32, 256, 3])
    label_sp = features['label']

    input, target_sp = tf.train.shuffle_batch([image, label_sp],
                                              batch_size=batch_size,
                                              capacity=min_after_dequeue + 3 * batch_size,
                                              min_after_dequeue=min_after_dequeue,
                                              num_threads=10)
    return input, target_sp

def tell_accuracy(predict,ground_truth):   #暂时未用，后面用到

    predict_ = tf.sparse_to_dense(sparse_indices=predict.indices, output_shape=predict.dense_shape,sparse_values=predict.values)
    ground_truth_ =tf.sparse_to_dense(sparse_indices=ground_truth.indices, output_shape=ground_truth.dense_shape,sparse_values=ground_truth.values)

    equal = tf.equal(predict_, ground_truth_)
    acc = tf.reduce_mean(tf.cast(equal, dtype=tf.float32))
    return acc
