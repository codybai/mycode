import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/data/",one_hot=True)
global_step = tf.Variable(0,trainable=False)
global_step2 = tf.Variable(0,trainable=False)
global_step3 = tf.Variable(0,trainable=False)
global_step4 = tf.Variable(0,trainable=False)
train_x = mnist.train.images
train_y = mnist.train.labels
test_x = mnist.train.images
test_y = mnist.train.labels

n_input = 784
n_hidden_1 = 256
n_hidden_2 = 128
n_classes = 10

#第一层输入
x = tf.placeholder(tf.float32,[None,n_input])
y = tf.placeholder(tf.float32,[None,n_input])
dropout_keep_prob = tf.placeholder(tf.float32)
#第二层输入
l2x = tf.placeholder(tf.float32,[None,n_hidden_1])
l2y = tf.placeholder(tf.float32,[None,n_hidden_1])
#第三层输入
l3x = tf.placeholder(tf.float32,[None,n_hidden_2])
l3y = tf.placeholder(tf.float32,[None,n_classes])

#定义学习参数
weights = {
    #网络1 784-256-784
    'h1':tf.Variable(tf.random_normal([n_input,n_hidden_1])),
    'l1_h2':tf.Variable(tf.random_normal([n_hidden_1,n_hidden_1])),
    'l1_out':tf.Variable(tf.random_normal([n_hidden_1,n_input])),

    #网络2 256-128-256
    'l2_h1':tf.Variable(tf.random_normal([n_hidden_1,n_hidden_2])),
    'l2_h2':tf.Variable(tf.random_normal([n_hidden_2,n_hidden_2])),
    'l2_out':tf.Variable(tf.random_normal([n_hidden_2,n_hidden_1])),
    #网络3 128-10
    'out':tf.Variable(tf.random_normal([n_hidden_2,n_classes]))
}
biases = {
    'b1':tf.Variable(tf.zeros([n_hidden_1])),
    'l1_b2':tf.Variable(tf.zeros([n_hidden_1])),
    'l1_out':tf.Variable(tf.zeros([n_input])),
    'l2_b1':tf.Variable(tf.zeros([n_hidden_2])),
    'l2_b2':tf.Variable(tf.zeros([n_hidden_2])),
    'l2_out':tf.Variable(tf.zeros([n_hidden_1])),
    'out':tf.Variable(tf.zeros([n_classes]))
}

#第一层网络结构
#第一层的编码输出      784->256
l1_out = tf.nn.sigmoid(tf.add(tf.matmul(x,weights['h1']),biases['b1']))
#l1的解码器model
def noise_l1_autodecoder(layer_1,_weights,_biases,_keep_prob):
    layer_1out = tf.nn.dropout(layer_1,_keep_prob)
    # 256->256
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1out,_weights['l1_h2']),_biases['l1_b2']))
    layer_2out = tf.nn.dropout(layer_2,_keep_prob)
    #  256->784
    return tf.nn.sigmoid(tf.matmul(layer_2out,_weights['l1_out']) + _biases['l1_out'])
#第一层解码输出
l1_reconstruction = noise_l1_autodecoder(l1_out,weights,biases,dropout_keep_prob)

#计算COST
l1_cost = tf.reduce_mean(tf.pow(l1_reconstruction-y, 2))
#OPTIMIZER
l1_optm = tf.train.AdamOptimizer(0.01).minimize(l1_cost,global_step=global_step)


#第二层网络结构
#l2解码器model
def l2_autodecoder(layer1_2,_weights,_biases):
    #128->128
    layer1_2out = tf.nn.sigmoid(tf.add(tf.matmul(layer1_2,_weights['l2_h2']),_biases['l2_b2']))
    #128->256
    return tf.nn.sigmoid(tf.matmul(layer1_2out,_weights['l2_out'])+_biases['l2_out'])

#第二层的编码输出
l2_out = tf.nn.sigmoid(tf.add(tf.matmul(l2x,weights['l2_h1']),biases['l2_b1']))
#第二层的解码输出
l2_reconstruction = l2_autodecoder(l2_out,weights,biases)

#Cost 计算
l2_cost = tf.reduce_mean(tf.pow(l2_reconstruction-l2y,2))

#优化器
optm2 = tf.train.AdamOptimizer(0.01).minimize(l2_cost,global_step=global_step2)

#第三层网络
l3_out = tf.matmul(l3x,weights['out'])+biases['out']
l3_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=l3_out,labels=l3y))
l3_optm = tf.train.AdamOptimizer(0.01).minimize(l3_cost,global_step=global_step3)

#3层级联
#1联2
l1_l2out = tf.nn.sigmoid(tf.add(tf.matmul(l1_out,weights['l2_h1']),biases['l2_b1']))
#2联3
pred = tf.matmul(l1_l2out,weights['out']) + biases['out']
#定义loss和优化器
cost3 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=l3y))
optm3 = tf.train.AdamOptimizer(0.01).minimize(cost3,global_step=global_step4)
def test_first_net():
    with tf.Session() as sess:
        saver = tf.train.Saver()
        show_num = 10
        test_noisy = mnist.test.images[:show_num]+0.3*np.random.randn(show_num,784)
        saver.restore(sess,'model_1/model.ckpt-17589')
        encode_decode = sess.run(
            l1_reconstruction,feed_dict={x:test_noisy,dropout_keep_prob:1.})
        f,a = plt.subplots(3,10,figsize=(10,3))
        for i in range(show_num):
            a[0][i].imshow(np.reshape(test_noisy[i],(28,28)))
            a[1][i].imshow(np.reshape(mnist.test.images[i],(28,28)))
            a[2][i].matshow(np.reshape(encode_decode[i],(28,28)),cmap=plt.get_cmap('gray'))
            print(encode_decode[i])
        plt.show()

def train_first_net():
    #第一层网络训练
    epochs = 50
    batch_size = 128
    disp_step = 10
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print('开始训练')
        saver = tf.train.Saver()
        for epoch in range(epochs):
            num_batch  = int(mnist.train.num_examples/batch_size)
            total_cost = 0
            for i in range(num_batch):
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                batch_xs_noisy = batch_xs + 0.3*np.random.randn(batch_size,784)
                feeds = {x:batch_xs_noisy,y:batch_xs,dropout_keep_prob:0.5}
                sess.run(l1_optm,feed_dict=feeds)
                total_cost += sess.run(l1_cost,feed_dict=feeds)
            #display
            if epoch % disp_step ==0:
                print("Epoch % 02d/%02d average cost: %.6f" % (epoch,epochs,total_cost/num_batch))
                saver.save(sess,'model_1/model.ckpt',global_step=global_step)
        print('完成')

def train_second_net():
    #输入为上一个网络的输出
    epochs = 50
    batch_size = 128
    disp_step = 10
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        print('开始训练')
        for epoch in range(epochs):
            num_batch = int(mnist.train.num_examples/batch_size)
            total_cost = 0
            for i in range(num_batch):
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                l1_h = sess.run(l1_out,feed_dict={x:batch_xs,y:batch_xs,dropout_keep_prob:1.})
                _,l2cost = sess.run([optm2,l2_cost],feed_dict={l2x:l1_h,l2y:l1_h})
                total_cost += l2cost
            #log输出
            if epoch % disp_step == 0:
                print("Epoch",epoch,"/",epochs,"average cost:",total_cost/num_batch)
                saver.save(sess,'model_2/model.ckpt',global_step=global_step2)
        print("完成 layer2 训练")
def test_second_net():
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        show_num = 10
        testvec = mnist.test.images[:show_num]
        saver.restore(sess,'model_2/model.ckpt-17589')
        out1vec =sess.run(l1_out,feed_dict={x:testvec,y:testvec,dropout_keep_prob:1.})
        out2vec = sess.run(l2_reconstruction,feed_dict={l2x:out1vec})

        f,a = plt.subplots(3,10,figsize=(10,3))
        for i in range(show_num):
            a[0][i].imshow(np.reshape(testvec[i],(28,28)))
            a[1][i].imshow(np.reshape(out1vec[i],(16,16)))
            a[2][i].matshow(np.reshape(out2vec[i],(16,16)),cmap=plt.get_cmap('gray'))
        plt.show()
def train_third_net():
    epochs = 50
    batch_size = 128
    disp_step = 10
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print('开始训练')
        saver = tf.train.Saver()
        for epoch in range(epochs):
            num_batch = int(mnist.train.num_examples/batch_size)
            total_cost = 0.
            for i in range(num_batch):
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                l1_h = sess.run(l1_out,feed_dict={x:batch_xs,y:batch_xs,dropout_keep_prob:1.})
                l2_h = sess.run(l2_out,feed_dict={l2x:l1_h,l2y:l1_h})
                _,l3_cost = sess.run([l3_optm,l3_cost],feed_dict={l3x:l2_h,l3y:batch_ys})
                total_cost+=l3_cost
            #输出cost
            if epoch % disp_step == 0:
                print("Epoch", epoch, "/", epochs, "average cost:", total_cost / num_batch)
                saver.save(sess,'model_3/model.ckpt',global_step=global_step3)
        print("完成 layer3 训练")

if __name__ =='__main__':
    # test_first_net()
    # train_second_net()
    # test_second_net()
    train_third_net()