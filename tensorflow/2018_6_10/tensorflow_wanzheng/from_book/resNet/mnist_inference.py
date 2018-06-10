import tensorflow as tf

INPUT_NODE   = 784
OUTPUT_NODE  = 10

IMAGE_SIZE   = 28
NUM_CHANNELS = 1
NUM_LABELS   = 10

#第一层卷积的尺寸和深度
CONV1_DEEP = 32
CONV1_SIZE = 5
#第二层的卷积的尺寸和深度
CONV2_DEEP = 64
CONV2_SIZE = 5
#全连接层的节点个数
FC_SIZE = 512

#定义前向传播过程
#dropout防止过拟合
def inference(input_tensor, train, regularizer):
    # 第一层前向传播定义
    with tf.variable_scope('layer1-conv1'):
        #定义变量
        conv1_weights = tf.get_variable('weight',
                                        [CONV1_SIZE,CONV1_SIZE,NUM_CHANNELS,CONV1_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_biases = tf.get_variable('biases',[CONV1_DEEP],initializer=tf.constant_initializer(0.0))
        #开始卷积
        conv1  = tf.nn.bias_add(tf.nn.conv2d(input_tensor,conv1_weights,strides=[1,1,1,1],padding='SAME'),conv1_biases)
        #添加激活函数
        relu1 = tf.nn.relu(conv1)

    #第二层池化前向传播定义
    with tf.variable_scope('layer2-pool1'):
        pool1 = tf.nn.max_pool(relu1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

    #第二层前向传播定义
    with tf.variable_scope('layer3-conv2'):
        #定义变量
        conv2_weights = tf.get_variable('weight',
                                        [CONV2_SIZE,CONV2_SIZE,CONV1_DEEP,CONV2_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_biases = tf.get_variable('biases',
                                       [CONV2_DEEP],
                                       initializer=tf.constant_initializer(0.0))
        conv2 = tf.nn.bias_add(tf.nn.conv2d(pool1,conv2_weights,strides=[1,1,1,1],padding='SAME'),conv2_biases)

        relu2 = tf.nn.relu(conv2)
    #第四层池化层的前向传播定义
    with tf.variable_scope('layer4-pool2'):
        pool2 = tf.nn.max_pool(relu2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

    #变形
    pool_shape = pool2.get_shape().as_list()
    nodes = pool_shape[1]*pool_shape[2]*pool_shape[3]
    reshaped = tf.reshape(pool2,[pool_shape[0],nodes])

    #全连接层的前向传播定义
    with tf.variable_scope('layer5-fcl'):

        fcl_weight = tf.get_variable('weights',
                                     [nodes,FC_SIZE],
                                     initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('loss',regularizer(fcl_weight))

        fcl_biases = tf.get_variable('biases',
                                     [FC_SIZE],
                                     initializer=tf.constant_initializer(0.0))

        fcl = tf.nn.relu(tf.nn.bias_add(tf.matmul(reshaped,fcl_weight),fcl_biases))
        if train:fcl = tf.nn.dropout(fcl,0.5)

    #全连接层的前向传播定义
    with tf.variable_scope('layer6-fcl2'):
        fcl2_weights = tf.get_variable('weights',
                                       [FC_SIZE,NUM_LABELS],
                                       initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('loss',regularizer(fcl2_weights))
        fcl2_biases = tf.get_variable('biases',
                                      [NUM_LABELS],
                                      tf.constant_initializer(0.0))
        logit = tf.nn.bias_add(tf.matmul(fcl,fcl2_weights),fcl2_biases)

        #返回logit结果
        return logit























































































