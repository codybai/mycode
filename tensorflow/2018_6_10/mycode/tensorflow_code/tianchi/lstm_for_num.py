import tensorflow as tf
import pickle as pk
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.training import moving_averages

input_height = 32
input_wide = 256
batch_size = 100
time_steps = 256
num_hiden = 64
num_classes = 10+1+1
lstm_layers = 4
epochs = 100000
# num_data = 1000
# n_batch = num_data // batch_size

input = tf.placeholder(tf.float32,shape=[None,32,256,3])
yto_beam = tf.sparse_placeholder(dtype=tf.int32)
ground_truth = tf.sparse_placeholder(tf.int32)
#学习率设置
INITIAL_LEARNING_RATE = 1e-3
DECAY_STEPS = 5000
REPORT_STEPS = 100
LEARNING_RATE_DECAY_FACTOR = 0.9 # The learning rate decay factor
MOMENTUM = 0.9

global_step = tf.Variable(0, trainable=False)
learning_rate = tf.train.exponential_decay(INITIAL_LEARNING_RATE, global_step, DECAY_STEPS,LEARNING_RATE_DECAY_FACTOR, staircase=True)
###

#BN need
MOVING_AVERAGE_DECAY = 0.9997
BN_DECAY = MOVING_AVERAGE_DECAY
BN_EPSILON = 0.001
RESNET_VARIABLES = 'model_variables'
UPDATE_OPS_COLLECTION = 'model_update_ops'
IMAGENET_MEAN_BGR = [103.062623801, 115.902882574, 123.151630838, ]
###


class Global:
    def __init__(self):
        path = ''
        self.is_training = tf.convert_to_tensor(False, dtype='bool', name='is_training')
        with open(path + "dataset_only_num.pkl", "rb+") as f:
            data = pk.load(f)
            x_ = []
            y = []
            self.j = 0  # 记录总的数据量
            for i in data:
                x_.append([i[0]])
                y.append([i[1]])
                self.j += 1

            x = []
            for i in x_:
                x.append(i[0])

        d = int(2 / 3 * len(x))

        self.x_train, self.x_test = x[:], x[:]
        self.y_train, self.y_test = y[:], y[:]

    def train(self):
        self.is_training = tf.convert_to_tensor(True, dtype='bool', name='is_training')
        self.train_batchs = int(len(self.x_train) / batch_size)
        self.train_size = self.train_batchs * batch_size
        self.train_i = 0

    def test(self):
        self.is_training = tf.convert_to_tensor(False, dtype='bool', name='is_training')
        self.test_batchs = int(len(self.x_test) / batch_size)
        self.test_size = self.test_batchs * batch_size
        self.test_i = 0


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


def ylist_to_sparse(labellist):  #  直接用读取出来的data变成SparseTensor 所有的y    # called by get_next_batch
    indices = []
    values=[]
    max_row = 0
    max_col = 0
    y = []
    for j in labellist:
        y.append(list(j[0]))

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

def get_next_batch(type):
    if type == 'train':
        i = g.train_i
        b = batch_size
        x = g.x_train[i*b : (i+1)*b]
        y = g.y_train[i : (i+b)]     #y要根据数据格式调整
        g.train_i += 1
    elif type == 'test':
        i = g.test_i
        b = batch_size
        x = g.x_test[i*b : (i+1)*b]
        y = g.y_test[i:(i + b)]  # y要根据数据格式调整
        g.test_i += 1

    indices, values, shape = ylist_to_sparse(y)

    y = [indices, values, shape]

    return x, y


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
def show_indices_values_shape(list):
    print(decode_sparse_tensor(list))

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

g = Global()

in_lstm = tf.reshape(input,shape=[batch_size,time_steps,32*3])

w_lstm = tf.Variable(tf.truncated_normal(shape=[num_hiden,num_classes],stddev=0.1))
b_lstm = tf.Variable(tf.constant(0.1,shape=[num_classes]))
cell = tf.nn.rnn_cell.BasicLSTMCell(num_hiden)
# state = tf.nn.rnn_cell.MultiRNNCell([cell]*lstm_layers,state_is_tuple=True)
outputs,_= tf.nn.dynamic_rnn(cell,inputs=in_lstm,sequence_length=[time_steps]*batch_size,dtype=tf.float32)

outputs = tf.reshape(outputs,shape=[batch_size*time_steps,num_hiden])
logits = tf.matmul(outputs,w_lstm)+b_lstm  #[batch_size*time_steps,num_classes]
logits = tf.reshape(logits,shape=[batch_size,time_steps,num_classes])

logits = tf.transpose(logits,[1,0,2])
#CTC
# 由y转化而来,是从数据集合中直接获取到， 为logits的实际标签。类型是SparseTensor
# logits为神经网络输出的预测，格式为[time_steps,batch_size,num_classes]
loss = tf.nn.ctc_loss(labels=ground_truth,inputs=logits,sequence_length=[time_steps]*batch_size)

#loss求平均
cost = tf.reduce_mean(loss)
#最小化cost
train_step  = tf.train.AdamOptimizer(learning_rate).minimize(cost,global_step=global_step)

#测试时候的ctc寻路策略
#decoded是测试时候由模型预测返回的标签,类型为SparseTensor,log_probs和accuracy类型未知，用处未知
decoded,log_probs=tf.nn.ctc_beam_search_decoder(inputs=logits,sequence_length=[time_steps]*batch_size)
acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), yto_beam))
init = tf.global_variables_initializer()


#训练网络
with tf.Session() as sess:   #完成get_next_batc()就可以训练了
    g.train()
    g.test()
    sess.run(init)
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)#保存模型

    for epoch in range(epochs):     #总共训练轮数
        g.train_i=0
        g.test_i=0
        for batch in range(g.train_batchs):#一轮的批次数
            batch_xs,batch_ys = get_next_batch('train')
            print('total epoch num:'+str(epochs)+'   now epoch:',epoch)
            print('total batch num:',str(g.train_batchs-1)+'   now batch:',batch)
            print(batch_ys)
            b_loss,_=sess.run([loss,train_step],feed_dict={input:batch_xs,ground_truth:batch_ys})
            print('loss:',b_loss)
        print("is predicting...")
        #此处填写测试精度代码batch_xs,batch_ys = get_next_batch('test')
        # show_indices_values_shape(batch_ys)
        batch_xs, batch_ys = get_next_batch('test')
        predict_label,_ = sess.run([decoded[0],acc],feed_dict={input:batch_xs,yto_beam:tf.SparseTensorValue(batch_ys[0],batch_ys[1],batch_ys[2])}) #decoded为经过ctc搜索到的矩阵标签，为SparseTensor

        report_accuracy(predict_label,batch_ys)

    saver.save(sess,"mymodel/model.ckpt")  #保存




#测试网络
# with tf.Session() as sess:  #完成精度计算就可以测试精度了
#     g.test()
#     g.test_i=0
#     #模型恢复
#     saver = tf.train.Saver()
#     saver.restore(sess,"mymodel/model.ckpt")
#     #精度测试
#     for batch in range(g.test_batchs-1):#一轮的批次数
#         batch_xs,batch_ys = get_next_batch('test')
#         # show_indices_values_shape(batch_ys)
#         predict_label,_ = sess.run([decoded[0],acc],feed_dict={input:batch_xs,yto_beam:tf.SparseTensorValue(batch_ys[0],batch_ys[1],batch_ys[2])}) #decoded为经过ctc搜索到的矩阵标签，为SparseTensor
#         report_accuracy(predict_label,batch_ys)
#     #decoded到底为标签的概率矩阵还是数值矩阵？  估计是概率矩阵
#     #batch_ys到底为标签的什么样式的稀疏矩阵？ 概率的稀疏矩阵还是数值的稀疏矩阵
























