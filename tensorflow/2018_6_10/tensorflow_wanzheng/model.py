import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.training import moving_averages
import time
import numpy as np
import pickle as pk

img_row = 32
img_col = 192
max_steps = 96
img_channel = 3
batch_szie = 128
hideen_units = 64        #每个lstm中神经元个数
num_layers = 1           #lstm层数
num_classes = 2239 + 1 #最大文字长度 + blank

img_shape = [batch_szie, img_col, img_row, img_channel]
tar_shape = []


epochs = 10


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
    def __init__(self):
        with open("dataset.pkl", "rb+") as f:
            data = pk.load(f)
            x_ = []
            y = []
            self.j = 0  # 记录总的数据量
            for i in data:
                x_.append([i[0]])
                y.append([i[1]])
                self.j += 1

            x = []
            print(self.j)
            for i in x_:
                x.append(i[0])

        d = int(2/3 * len(x))

        self.x_train, self.x_test = x[:d], x[d:]
        self.y_train, self.y_test = y[:d], y[d:]

    def train(self):
        self.is_training = tf.convert_to_tensor(True, dtype='bool', name='is_training')
        self.train_batchs = int(len(self.x_train) / batch_szie)
        self.train_size = self.train_batchs * batch_szie
        self.train_i = 0

    def test(self):
        self.is_training = tf.convert_to_tensor(False, dtype='bool', name='is_training')
        self.test_batchs = int(len(self.x_test) / batch_szie)
        self.test_size = self.test_batchs * batch_szie
        self.test_i = 0

g = Global()




def bn(x, name):
    with tf.variable_scope(name) as scope:
        x_shape = x.get_shape()
        params_shape = x_shape[-1:]
        axis = list(range(len(x_shape) - 1))

        beta = tf.get_variable('beta', params_shape, dtype=tf.float32,
                               initializer=tf.zeros_initializer())
        gamma = tf.get_variable('gamma', params_shape, dtype=tf.float32,
                                initializer=tf.ones_initializer())

        moving_mean = tf.get_variable('moving_mean', params_shape,
                                      dtype=tf.float32,
                                      initializer=tf.zeros_initializer(),
                                      trainable=False)
        moving_variance = tf.get_variable('moving_variance', params_shape,
                                          dtype=tf.float32,
                                          initializer=tf.ones_initializer(),
                                          trainable=False)

        # These ops will only be preformed when training.
        mean, variance = tf.nn.moments(x, axis)
        update_moving_mean = moving_averages.assign_moving_average(moving_mean, mean, BN_DECAY)
        update_moving_variance = moving_averages.assign_moving_average(moving_variance, variance, BN_DECAY)
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
        w = tf.get_variable('w', shape, dtype=tf.float32,
                            initializer=tf.truncated_normal_initializer(stddev=0.5))
        b = tf.get_variable('b', [o_s], dtype=tf.float32,
                            initializer=tf.constant_initializer(0.1, dtype=tf.float32))
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
    targets = tf.sparse_placeholder(tf.int32)
    seq_len = tf.placeholder(tf.int32, None)

    x = conv(inputs, 3, 3, 3, 32, 'conv0')
    for i in range(1, 5):
        x = conv(x, 3, 3, 32, 32, 'conv'+str(i))
    x = max_pool(x)
    x = conv(x, 3, 3, 32, 1, 'conv_to_lstm')

    shape = x.get_shape()
    shape = [int(i) for i in shape]
    x = tf.reshape(x, [shape[0], shape[1], shape[2]])
    #此时x的shape是[batch_size, 192, 32, 1]
    #应该可以直接输入到lstm中

    cell = tf.contrib.rnn.LSTMCell(hideen_units, state_is_tuple=True)
    stack = tf.contrib.rnn.MultiRNNCell([cell] * num_layers, state_is_tuple=True)
    x, _ = tf.nn.dynamic_rnn(stack, x, seq_len, dtype=tf.float32)

    x = tf.reshape(x, [-1, hideen_units])
    with tf.variable_scope('lstm_output') as scope:
        W = tf.get_variable('W', [hideen_units, num_classes], dtype=tf.float32,
                            initializer=tf.truncated_normal_initializer(stddev=0.1))
        b = tf.get_variable('b', [num_classes], dtype=tf.float32,
                            initializer=tf.constant_initializer(0))
        logits = tf.matmul(x, W) + b


    logits = tf.reshape(logits, [batch_szie, -1, num_classes])
    logits = tf.transpose(logits, (1, 0, 2))

    return inputs, targets, logits, seq_len

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
        result.append(sparse_tensor[1][index])
    return result


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

def ylist_to_sparse(labellist):  #  直接用读取出来的data变成SparseTensor 所有的y    # called by get_next_batch
    indices = []
    values=[]
    max_row = 0
    max_col = 0
    y = []
    for j in labellist:
        y.append(list(j[0]))

    for idx,i in enumerate(y):
        if idx >max_row:
            max_row=idx
        for jdx, j in enumerate(i):
            y[idx][jdx] = j
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
        x = g.x_train[i*b : (i+1)*b]
        y = g.y_train[i : (i+b)]     #y要根据数据格式调整
        g.train_i += 1
    elif type == 'test':
        i = g.test_i
        b = batch_szie
        x = g.x_test[i*b : (i+1)*b]
        y = g.y_test[i:(i + b)]  # y要根据数据格式调整
        g.test_i += 1

    x = [i.reshape(img_col, img_row, img_channel) for i in x]

    indices, values, shape = ylist_to_sparse(y)


    seq_len = np.ones(batch_szie) * max_steps
    y = [indices, values, shape]

    return x, y, seq_len

def train_model():
    g.train()

    inputs, targets, logits, seq_len = create_model()
    loss = tf.nn.ctc_loss(inputs=logits, labels=targets, sequence_length=seq_len)
    cost = tf.reduce_mean(loss)

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost,global_step=global_step)
    init = tf.global_variables_initializer()


    with tf.Session() as session:
        session.run(init)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)
        for curr_epoch in range(epochs):
            g.train_i = 0     #baichao modify
            print("Epoch.......", curr_epoch)
            train_cost = train_ler = 0
            for batch in range(g.train_batchs ):   #baichao modify
                start = time.time()

                train_inputs, train_targets, train_seq_len = get_next_batch('train')
                print(batch)    #baichao modify
                feed = {inputs: train_inputs, targets: train_targets, seq_len: train_seq_len}
                '''b_loss, b_targets, b_logits, b_seq_len, b_cost, steps, _ = \
                    session.run([loss, targets, logits, seq_len, cost,global_step, optimizer], feed)'''
                b_cost, steps = session.run([loss, optimizer], feed)
                train_cost += b_cost * batch_szie
                seconds = time.time() - start
                print("cost: ", b_cost,"Step: ", steps, ", batch seconds:", seconds)
            train_cost /= g.train_size
            log = "Epoch {}/{}, steps = {}, train_cost = {:.3f}, " \
                  "train_ler = {:.3f}, val_cost = {:.3f}, " \
                  "val_ler = {:.3f}, time = {:.3f}s, learning_rate = {}"
            #print(log.format(curr_epoch + 1, epochs, steps,              #baichao modify
            #                 train_cost, train_ler, 0.0,
            #                 0.0, time.time() - start, 0.0))
        saver.save(session, "model/model.ckpt")


def test_model():
    g.test()

    inputs, targets, logits, seq_len = create_model()
    decoded, log_prob = tf.nn.ctc_beam_search_decoder(logits, seq_len, merge_repeated=False)
    acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), targets))

    with tf.Session() as session:
        saver = tf.train.Saver()
        saver.restore(session, "model/model.ckpt")

        for batch in range(g.test_batchs - 1):
            test_inputs, test_targets, test_seq_len = get_next_batch('test')
            '''test_feed = {inputs: test_inputs, 
                         targets: tf.SparseTensorValue(indices=test_targets[0],
                                    values=test_targets[1], dense_shape=test_targets[2]), 
                         seq_len: test_seq_len}'''
            test_feed = {inputs: test_inputs, targets: test_targets, seq_len: test_seq_len}
            dd, log_probs, accuracy = session.run([decoded[0], log_prob, acc], test_feed)
            report_accuracy(dd, test_targets)



def report_accuracy(decoded_list, test_targets):
    original_list = decode_sparse_tensor(test_targets)
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
    # test_model()


