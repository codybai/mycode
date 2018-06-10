import numpy as np
import tensorflow as tf
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt

HIDDEN_SIZE = 30
NUM_LAYERS = 2
TIMESTEPS = 10
TRAINING_STEPS = 10000
BATCH_SIZE = 32

TRAINING_EXAMPLES = 10000
TESTING_EXAMPLES = 1000
SAMPLE_GAP = 0.01

def generate_data(seq):
    x = []
    y = []
    for i in range(len(seq)-TIMESTEPS):
        x.append([seq[i:i+TIMESTEPS]])
        y.append([seq[i+TIMESTEPS]])
    return np.array(x,dtype=np.float32),np.array(y,dtype=np.float32)

def lstm_model(x,y,is_training):
    cell = tf.nn.rnn_cell.MultiRNNCell([tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE) for _ in range(NUM_LAYERS)])
    outputs,_ = tf.nn.dynamic_rnn(cell,x,dtype=tf.float32)
    output = outputs[:,-1,:]
    predictions  = tf.contrib.layers.fully_connected(output,1,activation_fn=None)
    if not is_training:
        return predictions,None,None

    loss = tf.losses.mean_squared_error(labels=y,predictions=predictions)

    train_op = tf.contrib.layers.optimize_loss(
        loss,tf.train.get_global_step(),
        optimizer='Adagrad',learning_rate = 0.1)
    return predictions,loss,train_op

def train(sess,train_x,train_y):
    #将数据以数据集的方式提供给计算图
    ds = tf.contrib.data.Dataset.from_tensor_slices((train_x,train_y))
    ds = ds.repeat().shuffle(1000).batch(BATCH_SIZE)
    x,y = ds.make_one_shot_iterator().get_next()

    #调用模型，得到预测结果、损失函数、和训练操作
    with tf.variable_scope('model'):
        predictions,loss,train_op = lstm_model(x,y,True)
    #初始化变量
    sess.run(tf.global_variables_initializer())
    for i in range(TRAINING_STEPS):
        _, l = sess.run([train_op,loss])
        if i % 100 ==0:
            print("train step:",i,'loss:',l)
def run_eval(sess,test_x,test_y):
    #将数据以数据集的方式提供给计算图
    ds = tf.contrib.data.Dataset.from_tensor_slices((test_x,test_y))
    ds = ds.batch(1)
    x,y = ds.make_one_shot_iterator().get_next()
    #进行预测，不需要y值
    with tf.variable_scope('model',reuse=True):
        prediction,_,_ = lstm_model(x,[0.0],False)
        #将预测结果存入一个数组
        predictions=[]
        labels=[]
        for i in  range(TESTING_EXAMPLES):
            p,l=sess.run([prediction,y])
            predictions.append(p)
            labels.append(l)
        #计算rmse作为评价指标
        predictions=np.array(predictions).squeeze()#去掉维度为1的维度
        labels = np.array(labels).squeeze()
        rmse = np.sqrt(((predictions - labels) ** 2).mean(axis = 0))
        print('Mean Square Error is :',rmse)

        #对预测的结果进行绘图
        plt.figure()
        plt.plot(predictions,label='predictions')
        plt.plot(labels,label = 'real_sin')
        plt.legend()
        plt.show()

test_start = (TRAINING_EXAMPLES+TIMESTEPS)*SAMPLE_GAP
test_end = test_start +(TESTING_EXAMPLES + TIMESTEPS) * SAMPLE_GAP
train_x, train_y = generate_data(np.sin(np.linspace(
    0,test_start,TRAINING_EXAMPLES + TIMESTEPS,dtype=np.float32
)))
test_x,test_y = generate_data(np.sin(np.linspace(
    test_start,test_end,TESTING_EXAMPLES + TIMESTEPS,dtype=np.float32
)))

with tf.Session() as sess:
    train(sess,train_x,train_y)
    run_eval(sess,test_x,test_y)
































































