from .config import *
from .Conv import *
from .Attention import *


#inputs
inputs = tf.placeholder(tf.float32, shape=inputs_shape)
yto_beam = tf.sparse_placeholder(dtype=tf.int64)
ground_truth = tf.sparse_placeholder(tf.int64)

#从文件读取数据
#train_batch_xs    shape=[32,256,3]
#train_batch_ys    shape=tf.SparseTensor
train_batch_xs, train_batch_ys = get_next_batch('train',batch_size)
test_batch_xs, test_batch_ys = get_next_batch('test',batch_size)

#dense_net  kears
x = dense_net(inputs)


#计算lstm和ctc输入参数
#x_shape = tf.shape(x)    #动态shape
x_shape = list(x.get_shape())     #不变长  静态shape
x_shape = [int(e) for e in x_shape]
dynamic_row, dynamic_col = x_shape[1], x_shape[2]
batch_size, dynamic_channel = x_shape[0], x_shape[3]
time_steps = dynamic_col




#seq2seq模型         [bs,time_steps,-1]   变长 todo
x = tf.reshape(x, [batch_size, time_steps, dynamic_row*dynamic_channel])  #规范lstm输入
x = seq2seq(x, batch_size)      #输出 [bs,time_steps,num_classes]
logits = tf.transpose(x, [1,0,2])

'''#lstm部分要手写实现动态，先用w,b把最后一维转成num_classes     test
x = tf.reshape(x,[batch_size*time_steps, dynamic_row*dynamic_channel])
w = tf.Variable(tf.truncated_normal(shape=[dynamic_row*dynamic_channel, num_classes],stddev=0.1))
b = tf.Variable(tf.constant(0.1,shape=[num_classes]))
logits = tf.matmul(x, w) + b  #[time_steps*batch_size,num_classes]
logits = tf.reshape(logits, shape=[time_steps,batch_size,num_classes])'''


#计算ctc
loss = tf.nn.ctc_loss(labels=ground_truth,
                      inputs=logits,
                      sequence_length=[max_label_len]*batch_size)
cost = tf.reduce_mean(loss)
train_step  = tf.train.AdamOptimizer(learning_rate).minimize(
    cost,global_step=global_step)


decoded, log_probs = tf.nn.ctc_beam_search_decoder(
    inputs=logits, sequence_length=[time_steps]*batch_size, merge_repeated=False)
acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), yto_beam))


