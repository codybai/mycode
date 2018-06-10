import time
from .finalmodel import *

with tf.Session() as sess:

    init = tf.global_variables_initializer()
    sess.run(init)
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)

    for epoch in range(epochs):
        print('total epoch num:' + str(epochs) + '   now epoch:', epoch + 1)
        for batch in range(N_TRAIN_BATCH):#一轮的批次数
            time1 = time.time()
            # 从文件读取数据
            batch_train_x,batch_train_y = sess.run([train_batch_xs,train_batch_ys])
            b_loss, mean_cost, _, predict_label = sess.run(
                [loss,cost,train_step,logits],
                feed_dict={inputs: batch_train_x, ground_truth: batch_train_y})
            time2 = time.time()
            batch_seconds = time2 - time1
            print('------total batch num:', str(N_TRAIN_BATCH) +
                  '   now batch:', batch + 1, 'batch seconds:', batch_seconds,
                  'mean_loss:', mean_cost)

            if epoch%100==0 and batch==0:   #每100个epoch测试一次
                if epoch == 0:
                    continue
                saver.save(sess, 'model/' + model_name,global_step=global_step)  # 100次保存一次模型

                print(epoch,":is predicting...")
                batch_test_x, batch_test_y = sess.run([test_batch_xs, test_batch_ys])
                predict_label, _ = sess.run(
                    [decoded[0],acc], feed_dict={inputs: batch_test_x, yto_beam:batch_test_y})
                    #decoded为经过ctc搜索到的矩阵标签，为SparseTensor
                report_accuracy(predict_label,test_batch_ys)

                # accuracy = tell_accuracy(predict=predict_label,ground_truth=test_batch_ys)   #后期改造用到
                # print('Epoch:', epoch, 'Accuracy:', acc.eval())                              #后期改造用到
    saver.save(sess, 'model/' + model_name,global_step=global_step)






