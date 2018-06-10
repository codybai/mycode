
import tensorflow as tf
import pickle as pk
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.training import moving_averages
import  numpy as np

input_height = 32
input_wide = 256
batch_size = 128
time_steps = 256
num_hidden = 256*32
epochs = 1000

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
mean = [125.307, 122.95, 113.865]
std  = [62.9932, 62.0887, 66.7048]
def color_preprocessing(x):
    x = x.astype('float32')
    for i in range(3):
        x[:,:,:,i] = (x[:,:,:,i] - mean[i]) / std[i]
    return x

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

        y = np.array(y)
        x = np.array(x)

        x = color_preprocessing(x)
        d = int(2 / 3 * len(x))

        self.x_train, self.y_train = np.array(x[:d]), y[:d]
        self.x_test, self.y_test = np.array(x[d:]), y[d:]

        dict_path = '../util/dictset.pkl'
        with open(dict_path, 'rb') as f:
            data = pk.load(f)
            self.dictset = data

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
g = Global()
num_classes = len(g.dictset)+1

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




# conv1[32,256,3]
in_conv1 = tf.reshape(input, shape=[-1, 32, 256, 3])
w_conv1 = tf.Variable(tf.truncated_normal(shape=[3, 3, 3, 64], stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1, shape=[64]))
result_conv1 = tf.nn.relu(tf.nn.conv2d(in_conv1, w_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
#[32,256,64]
w_conv2 = tf.Variable(tf.truncated_normal(shape=[3, 3, 64, 128], stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1, shape=[128]))
result_conv2 = tf.nn.relu(tf.nn.conv2d(result_conv1, w_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2)
#[32,256,128]
w_conv3 = tf.Variable(tf.truncated_normal(shape=[3, 3, 128, 256], stddev=0.1))
b_conv3 = tf.Variable(tf.constant(0.1, shape=[256]))
result_conv3 = tf.nn.relu(tf.nn.conv2d(result_conv2, w_conv3, strides=[1, 1, 1, 1], padding='SAME') + b_conv3)
#[32,256,256]
w_conv4 = tf.Variable(tf.truncated_normal(shape=[3, 3, 256, 256], stddev=0.1))
b_conv4 = tf.Variable(tf.constant(0.1, shape=[256]))
result_conv4 = tf.nn.relu(tf.nn.conv2d(result_conv3, w_conv4, strides=[1, 1, 1, 1], padding='SAME') + b_conv4)
#[32,256,256]
w_conv5 = tf.Variable(tf.truncated_normal(shape=[3, 3, 256, 512], stddev=0.1))
b_conv5 = tf.Variable(tf.constant(0.1, shape=[512]))
result_conv5 = tf.nn.relu(tf.nn.conv2d(result_conv4, w_conv5, strides=[1, 1, 1, 1], padding='SAME') + b_conv5)
#[32,256,512]
bn1 = bn(result_conv5, 'BN1')
#[32,256,512]
w_conv6 = tf.Variable(tf.truncated_normal(shape=[3, 3, 512, 512], stddev=0.1))
b_conv6 = tf.Variable(tf.constant(0.1, shape=[512]))
result_conv6 = tf.nn.relu(tf.nn.conv2d(bn1, w_conv6, strides=[1, 1, 1, 1], padding='SAME') + b_conv6)

bn2 = bn(result_conv6, 'BN2')
#[32,256,512]

w_conv8 = tf.Variable(tf.truncated_normal(shape=[3, 3, 512, 512], stddev=0.1))
b_conv8 = tf.Variable(tf.constant(0.1, shape=[512]))
result_conv8 = tf.nn.relu(tf.nn.conv2d(bn2, w_conv8, strides=[1, 1, 1, 1], padding='SAME') + b_conv8)
#[32,256,512]


#BLSTM+CTC
in_lstm = tf.transpose(result_conv8,[0,2,1,3])
in_lstm = tf.reshape(in_lstm,[batch_size,time_steps,32*512])
result_conv8 = tf.transpose(in_lstm,[1,0,2])     #[time_steps,bs,512*32]
result_conv8 = tf.reshape(result_conv8,[time_steps*batch_size,32*512])
result_conv8 = tf.split(result_conv8,time_steps)      #[time_steps个[bs,512*32]] 为了满足blstm的输入要求


lstm_fw_cell = tf.nn.rnn_cell.GRUCell(num_hidden)
lstm_bw_cell = tf.nn.rnn_cell.GRUCell(num_hidden)
outputs,_,_=tf.nn.static_bidirectional_rnn(cell_fw=lstm_fw_cell,cell_bw=lstm_bw_cell,inputs=result_conv8,sequence_length=[time_steps]*batch_size,dtype=tf.float32)#output=[time_steps个[bs,2*num_hidden]]
w_lstm = tf.Variable(tf.truncated_normal(shape=[2*num_hidden,num_classes],stddev=0.1))
b_lstm = tf.Variable(tf.constant(0.1,shape=[num_classes]))
outputs = tf.reshape(outputs,shape=[time_steps*batch_size,2*num_hidden])
logits = tf.matmul(outputs,w_lstm)+b_lstm  #[time_steps*batch_size,num_classes]
logits = tf.reshape(logits,shape=[time_steps,batch_size,num_classes])

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
decoded,log_probs=tf.nn.ctc_beam_search_decoder(inputs=logits,sequence_length=[time_steps]*batch_size,merge_repeated=False)
acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), yto_beam))
init = tf.global_variables_initializer()



#训练网络
with tf.Session() as sess:
    g.train()
    g.test()
    sess.run(init)
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)#保存模型
    #saver.restore(sess,'cnn_blstm_ctc/model.ckpt')
    for epoch in range(epochs):     #总共训练轮数
        g.train_i=0
        g.test_i=0
        for batch in range(g.train_batchs):#一轮的批次数
            batch_xs,batch_ys = get_next_batch('train')
            print('>total epoch num:'+str(epochs)+'   now epoch:',epoch+1)
            print('>>total batch num:',str(g.train_batchs)+'   now batch:',batch+1)
            b_loss,mean_cost,_,predict_label=sess.run([loss,cost,train_step,logits],feed_dict={input:batch_xs,ground_truth:batch_ys})
            if batch == g.train_batchs-1: #last batch to show means loss
                print('mean_loss:',mean_cost)
            if epoch %100 == 0: #predict per 100 epoch
                if epoch == 0: #first time not save
                    continue
                saver.save(sess, "cnn_blstm_ctc/model.ckpt",global_step=1)  # 100次保存一次模型
    saver.save(sess,"cnn_blstm_ctc/model.ckpt")  #保存

'''
with tf.Session() as sess:
    g.test()
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)#保存模型
    saver.restore(sess,'cnn_blstm_ctc/model.ckpt')
    for batch in range(g.test_batchs):
        print('test...')
        x,y = get_next_batch('test')
        predict_y  = sess.run(decoded[0],feed_dict={input:x,yto_beam:tf.SparseTensorValue(y[0],y[1],y[2])})
        report_accuracy(predict_y,y)

'''


















