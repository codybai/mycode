import tensorflow as tf
#9
a=[ [1,-2,3],
    [4,-5,6],
    [-7,8,9],
    [1,-2,3],
    [4,-5,6],
    [-7,8,9],
    [1,-2,3],
    [4,-5,6],
    [-7,8,9]]
#13
b=[ [1,-2,3],
    [4,-5,6],
    [-7,8,9],
    [1,-2,3],
    [4,-5,6],
    [-7,8,9],
    [1,-2,3],
    [4,-5,6],
    [4,-5,6],
    [-7,8,9],
    [1,-2,3],
    [4,-5,6],
    [-7,8,9]]
true_numer = 0
total_numer = len(a)
tf.nn.bidirectional_dynamic_rnn()
tf.nn.dynamic_rnn()
for origianal, detect in zip(a, b):
    if origianal == detect:
        true_numer += 1
        print('--------------------------------')
        print('原始序列：', origianal)
        print('预测序列：', detect,'（正确）')
    else:
        print('原始序列：', origianal)
        print('预测序列：', detect,'（错误）')
print('测试总数：',total_numer,'\n正确个数：',true_numer,"，\n正确率:", true_numer * 1.0 / total_numer)
