import tensorflow as tf
batch_size = 128
tfrecord_dir = 'C:/Users/baicol/PycharmProjects/tensorflow/learn_tfrecord_file/tfrecord/'
min_after_dequeue=1000
max_steps = 64
num_classes = 4349
num_hidden = 256
global_step = tf.Variable(0,trainable=False)
def get_next_batch(type, batch_size):
    assert type in ['test', 'train']

    reader = tf.TFRecordReader()

    file_queue = tf.train.string_input_producer([tfrecord_dir+ type + '.tfrecords'])
    _, serialize_example = reader.read(queue=file_queue)

    features = tf.parse_single_example(serialize_example, features={
        'image': tf.FixedLenFeature([], tf.string),
        'label': tf.VarLenFeature(tf.int64)
    })
    image_data = features['image']
    image_data = tf.image.decode_png(image_data, channels=3)
    image = tf.reshape(image_data, [32, 256, 3])
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

in_conv1, y = get_next_batch('train', batch_size)
in_conv1 = tf.cast(in_conv1,tf.float32)
y = tf.cast(y,tf.int32)

w_conv0 = tf.Variable(tf.truncated_normal([3,3,3,32],stddev=0.1))
b_conv0 = tf.Variable(tf.constant(0.1,shape=[32]))
conv0 = tf.nn.relu(tf.nn.conv2d(in_conv1,w_conv0,strides=[1,1,1,1],padding='SAME')+b_conv0)
pool0 =  tf.nn.max_pool(conv0,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
# bsx16x128x32

w_conv1 = tf.Variable(tf.truncated_normal([3,3,32,64],stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1,shape=[64]))
conv1 = tf.nn.relu(tf.nn.conv2d(pool0,w_conv1,strides=[1,1,1,1],padding='SAME')+b_conv1)
pool1 =  tf.nn.max_pool(conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
# bsx8x64x64
w_conv2 = tf.Variable(tf.truncated_normal([3,3,64,128],stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1,shape=[128]))
conv2 = tf.nn.relu(tf.nn.conv2d(pool1,w_conv2,strides=[1,1,1,1],padding='SAME')+b_conv2)
pool2 =  tf.nn.max_pool(conv2,ksize=[1,2,1,1],strides=[1,2,1,1],padding='SAME')
# bsx4x64x64
w_conv3 = tf.Variable(tf.truncated_normal([3,3,128,256],stddev=0.1))
b_conv3 = tf.Variable(tf.constant(0.1,shape=[256]))
conv3 = tf.nn.relu(tf.nn.conv2d(pool2,w_conv3,strides=[1,1,1,1],padding='SAME')+b_conv3)
pool3 =  tf.nn.max_pool(conv3,ksize=[1,2,1,1],strides=[1,2,1,1],padding='SAME')
# bsx2x64x256
w_conv4 = tf.Variable(tf.truncated_normal([3,3,256,512],stddev=0.1))
b_conv4 = tf.Variable(tf.constant(0.1,shape=[512]))
conv4 = tf.nn.relu(tf.nn.conv2d(pool3,w_conv4,strides=[1,1,1,1],padding='SAME')+b_conv4)
pool4 =  tf.nn.max_pool(conv4,ksize=[1,2,1,1],strides=[1,2,1,1],padding='SAME')
# bsx1x64x512

#[bs,1,64,512]
in_blstm = tf.transpose(pool4,[0,2,1,3])
in_blstm = tf.reshape(in_blstm,[batch_size,max_steps,512*1])
cell_fw = tf.nn.rnn_cell.GRUCell(num_hidden)
cell_bw = tf.nn.rnn_cell.GRUCell(num_hidden)
init_cell_fw = cell_bw.zero_state(batch_size,dtype=tf.float32)
init_cell_bw=cell_bw.zero_state(batch_size,dtype=tf.float32)

output,_ = tf.nn.bidirectional_dynamic_rnn(cell_fw=cell_fw,cell_bw=cell_bw,inputs=in_blstm,sequence_length=[max_steps]*batch_size,initial_state_fw=init_cell_fw,initial_state_bw=init_cell_bw)
#output:[bs,ms,1*512]
output = tf.reshape(output,[batch_size*max_steps,2*num_hidden])
w_blstm = tf.Variable(tf.truncated_normal([2*num_hidden,num_classes]))
b_lstm = tf.Variable(tf.constant(0.1,shape=[num_classes]))
output = tf.matmul(output,w_blstm)+b_lstm
logit = tf.reshape(output,[batch_size,max_steps,num_classes])
logit = tf.transpose(logit,[1,0,2])
loss = tf.nn.ctc_loss(labels=y,inputs=logit,sequence_length=[max_steps]*batch_size)
coss = tf.reduce_mean(loss)
train_step = tf.train.AdamOptimizer(learning_rate=1e-3).minimize(coss,global_step=global_step)

decoded, log_probs = tf.nn.ctc_beam_search_decoder(
    inputs=logit, sequence_length=[max_steps]*batch_size, merge_repeated=False)
acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), y))

init = tf.global_variables_initializer()

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)
    sess.run(init)
    saver = tf.train.Saver()
    for epoch in range(10000):
        coss_ ,_= sess.run([coss,train_step])
        print("Iter:",epoch,'coss:',coss_,'global_step:',global_step.eval())
        if epoch % 10 ==0:
            saver.save(sess,'model/model.ckpt',global_step=global_step)
    coord.request_stop()
    coord.join(threads=threads)