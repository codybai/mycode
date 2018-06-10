import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
import time
import numpy as np

img_row = 32
img_col = max_steps = 192
img_channel = 3
batch_szie = 128
hideen_units = 64    #每个lstm中神经元个数
num_layers = 1       #lstm层数
num_classes = 15 + 1 #最大文字长度 + blank

img_shape = [batch_szie, img_col, img_row, img_channel]   #转化成1维输入不是更好
tar_shape = []
seq_len = np.ones(batch_szie) * max_steps

#readdata

#getnextbatch

epochs = 100


MOVING_AVERAGE_DECAY = 0.9997
BN_DECAY = MOVING_AVERAGE_DECAY
BN_EPSILON = 0.001
RESNET_VARIABLES = 'model_variables'
UPDATE_OPS_COLLECTION = 'model_update_ops'
IMAGENET_MEAN_BGR = [103.062623801, 115.902882574, 123.151630838, ]

INITIAL_LEARNING_RATE = 1e-3
DECAY_STEPS = 5000
REPORT_STEPS = 100
LEARNING_RATE_DECAY_FACTOR = 0.9 # The learning rate decay factor
MOMENTUM = 0.9
DIGITS = '0123456789'

global_step = tf.Variable(0, trainable=False)
learning_rate = tf.train.exponential_decay(INITIAL_LEARNING_RATE, global_step, DECAY_STEPS,
                                               LEARNING_RATE_DECAY_FACTOR, staircase=True)


class Global:
    def train(self):
        self.is_training = tf.convert_to_tensor(1, dtype='bool', name='is_training')
        self.x_train, self.y_train, self.sl_train = read_data('train')               #写read_data  sl_train=[time_step,time_step,...]长度为等于batchsize,
        self.train_batchs = int(len(self.x_train) / batch_szie)
        self.train_size = self.batchs * batch_szie
        self.train_i = 0

    def test(self):
        self.is_training = tf.convert_to_tensor(0, dtype='bool', name='is_training')
        self.x_test, self.y_test, self.sl_test = read_data('test')
        self.test_batchs = int(len(self.x_test) / batch_szie)
        self.test_size = self.batchs * batch_szie
        self.test_i = 0

g = Global()

def read_data(type):
    if type == 'train':
        pass
    elif type == 'test':
        pass
    return x, y, sl


def decode_sparse_tensor(sparse_tensor):
    return tf.sparse_to_dense(sparse_tensor.indices, sparse_tensor.dense_shape, sparse_tensor.values)

def bn(x, name):
    with tf.variable_scope(name) as scope:
        x_shape = x.get_shape()
        params_shape = x_shape[-1:]
        axis = list(range(len(x_shape) - 1))

        beta = tf.get_variable('beta', params_shape,
                               initializer=tf.zeros_initializer())
        gamma = tf.get_variable('gamma', params_shape,
                                initializer=tf.ones_initializer())

        moving_mean = tf.get_variable('moving_mean', params_shape,
                                      initializer=tf.zeros_initializer(),
                                      trainable=False)
        moving_variance = tf.get_variable('moving_variance', params_shape,
                                          initializer=tf.ones_initializer(),
                                          trainable=False)

        # These ops will only be preformed when training.
        mean, variance = tf.nn.moments(x, axis)
        update_moving_mean = tf.moving_averages.assign_moving_average(moving_mean, mean, BN_DECAY)
        update_moving_variance = tf.moving_averages.assign_moving_average(moving_variance, variance, BN_DECAY)
        tf.add_to_collection(UPDATE_OPS_COLLECTION, update_moving_mean)
        tf.add_to_collection(UPDATE_OPS_COLLECTION, update_moving_variance)

        mean, variance = control_flow_ops.cond(
            g.is_training, lambda: (mean, variance),
            lambda: (moving_mean, moving_variance))

        x = tf.nn.batch_normalization(x, mean, variance, beta, gamma, BN_EPSILON)
    return x


#f_h: filter_height   i_s: input_spaces
def conv(x, f_h, f_w, i_s, o_s, name):
    with tf.variable_scope(name) as scope:
        shape = [f_h, f_w, i_s, o_s]
        w = tf.get_variable('w', shape,
                            tf.truncated_normal_initializer(stddev=0.5))
        b = tf.get_variable('b', [o_s],
                            tf.constant_initializer(0.1))
        x = tf.nn.conv2d(x, w, strides=[1,1,1,1], padding='SAME')
        x = tf.nn.relu(x + b)
        x = bn(x, name)
    return x

def max_pool(x, ksize=(2, 2), stride=(2, 2)):
    x = tf.nn.max_pool(x, ksize=[1, ksize[0], ksize[1], 1],
                          strides=[1, stride[0], stride[1], 1], padding='SAME')
    return x

def create_model():
    inputs = tf.placeholder(tf.float32, img_shape)
    targets = tf.placeholder(tf.float32)
    seq_len = tf.placeholder(tf.int32, None)

    x = conv(inputs, 3, 3, 3, 32, 'conv0')
    for i in range(1, 5):
        x = conv(x, 3, 3, 32, 32, 'conv'+str(i))  #厚度 3*32*32*32...32乘五次
    x = max_pool(x)
    x = conv(x, 3, 3, 32, 1, 'conv_to_lstm')      #要是接下去应该是x=conv(x,3,3,0.5*（3*32^5）,1)

    #此时x的shape是[batch_size, 192, 32, 1]        #LSTM接受的格式为[batch_size,time_step,feature_num]
    #应该可以直接输入到lstm中                        #其中feature_num = num_hiden

    cell = tf.contrib.rnn.LSTMCell(hideen_units, state_is_tuple=True)
    stack = tf.contrib.rnn.MultiRNNCell([cell] * num_layers, state_is_tuple=True)
    x, _ = tf.nn.dynamic_rnn(stack, x, seq_len, dtype=tf.float32)

    x = tf.reshape(x, [-1, hideen_units])
    with tf.variable_scope('lstm_output') as scope:
        W = tf.get_variable('W', [hideen_units, num_classes],
                            tf.truncated_normal_initializer(stddev=0.1))
        b = tf.get_variable('b', [num_classes],
                            tf.constant_initializer(0))
        logits = tf.matmul(x, W) + b


    logits = tf.reshape(logits, [batch_szie, -1, num_classes])
    logits = tf.transpose(logits, (1, 0, 2))

    return inputs, targets, logits, seq_len

def ylist_to_sparse(labellist):  #  直接用读取出来的data变成SparseTensor 所有的y
    indices = []
    values=[]
    max_row = 0
    max_col = 0
    y = []
    for j in labellist[:]:
        y.append(list(j[1]))
    # y:#[
    # ['大', '飞', '机'],
    # ['大', '写', '的', 'A', '和', 'B'],
    # ['1', '搜', '轮', '船'],
    # ['1', '个', '人', '在', '玩', 'c', 'F']]
    for idx,i in enumerate(y):
        if idx >max_row:
            max_row=idx
        for jdx, j in enumerate(i):    #循环编码
            y[idx][jdx] = ord(y[idx][jdx])
            indices.append([idx,jdx])
            values.append(y[idx][jdx])
            if jdx>max_col:
                max_col=jdx

    shape=[max_row+1,max_col+1]
    return indices,values,shape


def get_next_batch(type):
    if type == 'train':
        i = g.train_i
        b = batch_szie
        x = g.x_train[i*b:(i+1)*b, :, :, :]
        y = g.y_train[i:(i+1)]     #y要根据数据格式调整
        seq_len = g.sl_train[i:(i+1)]
        g.train_i += 1
    elif type == 'test':
        i = g.test_i
        b = batch_szie
        x_ = g.x_test[i * b:(i + 1) * b, :, :, :]
        y_ = g.y_test[i:(i + 1)]  # y要根据数据格式调整

        seq_len = g.sl_test[i:(i+1)]
        g.test_i += 1

        #转化成SparseTensor
        indices,values,shape=ylist_to_sparse(y_)
        y=tf.SparseTensor(indices=indices,values=values,dense_shape=shape)
        #y 这里应该是SparseTensor         ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    return x, y, seq_len
tf.SparseTensor
def train_model():
    g.train()

    inputs, targets, logits, seq_len = create_model()
    loss = tf.nn.ctc_loss(labels=targets,inputs=logits, sequence_length=seq_len)  #targets应该为SparseTensor
    cost = tf.reduce_mean(loss)

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss,global_step=global_step)
    init = tf.global_variables_initializer()


    with tf.Session() as session:
        session.run(init)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)
        for curr_epoch in range(epochs):
            print("Epoch.......", curr_epoch)
            train_cost = train_ler = 0
            for batch in range(g.train_batchs - 1):
                start = time.time()
                train_inputs, train_targets, train_seq_len = get_next_batch('train')
                feed = {inputs: train_inputs, targets: train_targets, seq_len: train_seq_len}
                b_loss, b_targets, b_logits, b_seq_len, b_cost, steps, _ = \
                    session.run([loss,targets, logits, seq_len, cost,global_step, optimizer], feed)
                train_cost += b_cost * batch_szie
                seconds = time.time() - start
                print("cost: ", b_cost,"Step: ", steps, ", batch seconds:", seconds)
            train_cost /= g.train_size
            log = "Epoch {}/{}, steps = {}, train_cost = {:.3f}, " \
                  "train_ler = {:.3f}, val_cost = {:.3f}, " \
                  "val_ler = {:.3f}, time = {:.3f}s, learning_rate = {}"
            print(log.format(curr_epoch + 1, epochs, steps,
                             train_cost, train_ler, 0.0,
                             0.0, time.time() - start, 0.0))
        saver.save(session, "model.ckpt")


def test_model():
    g.test()

    inputs, targets, logits, seq_len = create_model()
    decoded, log_prob = tf.nn.ctc_beam_search_decoder(logits, seq_len, merge_repeated=False)#decoded[0] = SparesTensor
    acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), targets))

    with tf.Session() as session:
        saver = tf.train.Saver()
        saver.restore(session, 'model.ckpt')

        for batch in range(g.test_batchs - 1):
            test_inputs, test_targets, test_seq_len = get_next_batch('test')
            test_feed = {inputs: test_inputs, targets: test_targets, seq_len: test_seq_len}
            dd, log_probs, accuracy = session.run([decoded[0], log_prob, acc], test_feed)
            report_accuracy(dd, test_targets)  # 读出来的数据直接到了这里



def report_accuracy(decoded_list, test_targets):
    original_list = decode_sparse_tensor(test_targets)  #把SparseTensor转化成稀疏矩阵
    detected_list = decode_sparse_tensor(decoded_list)
    true_numer = 0
    if len(original_list) != len(detected_list):
        print("len(original_list)", len(original_list), "len(detected_list)",
              len(detected_list), " test and detect length desn't match")
        return
    print("T/F: original(length) <-------> detectcted(length)")

    for idx, number in enumerate(original_list):
        detect_number = detected_list[idx]
        hit = (number == detect_number)
        print(hit, number, "(", len(number), ") <-------> ",
              detect_number, "(", len(detect_number), ")")
        if hit:
            true_numer = true_numer + 1
    print("Test Accuracy:", true_numer * 1.0 / len(original_list))


if __name__ == '__main__':
    train_model()
    test_model()

