# -*- coding: utf-8 -*-
from keras.layers import Input, Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Flatten, BatchNormalization, Permute, TimeDistributed, Dense, Bidirectional, GRU
from keras.models import Model, load_model
from keras import backend as K
from keras.layers import Lambda
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import os
import numpy as np
import pickle as pk


img_row = 32
img_col = 256
max_steps = 30
img_channel = 3
batch_size = 128
hideen_units = 256         #每个lstm中神经元个数
num_classes = 10 + 1       #最大文字长度 + blank

epochs = 50

img_shape = (img_row, img_col, img_channel)
tar_shape = []

mean = [125.307, 122.95, 113.865]
std  = [62.9932, 62.0887, 66.7048]


def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    y_pred = y_pred[:, 2:, :]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


def get_model():
    input = Input(img_shape, name='the_input')
    m = Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', name='conv1')(input)
    m = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='pool1')(m)
    m = Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same', name='conv2')(m)
    m = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='pool2')(m)
    m = Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same', name='conv3')(m)
    m = Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same', name='conv4')(m)

    m = ZeroPadding2D(padding=(0, 1))(m)
    m = MaxPooling2D(pool_size=(2, 2), strides=(2, 1), padding='valid', name='pool3')(m)

    m = Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same', name='conv5')(m)
    m = BatchNormalization(axis=1)(m)
    m = Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same', name='conv6')(m)
    m = BatchNormalization(axis=1)(m)
    m = ZeroPadding2D(padding=(0, 1))(m)
    m = MaxPooling2D(pool_size=(2, 2), strides=(2, 1), padding='valid', name='pool4')(m)
    m = Conv2D(512, kernel_size=(2, 2), activation='relu', padding='valid', name='conv7')(m)

    m = Permute((2, 1, 3), name='permute')(m)
    m = TimeDistributed(Flatten(), name='timedistrib')(m)

    m = Bidirectional(GRU(hideen_units, return_sequences=True), name='blstm1')(m)
    m = Dense(hideen_units, name='blstm1_out', activation='linear')(m)
    m = Bidirectional(GRU(hideen_units, return_sequences=True), name='blstm2')(m)
    y_pred = Dense(num_classes, name='blstm2_out', activation='softmax')(m)

    basemodel = Model(inputs=input, outputs=y_pred)

    labels = Input(name='the_labels', shape=[None, ], dtype='float32')
    input_length = Input(name='input_length', shape=[1], dtype='int64')
    label_length = Input(name='label_length', shape=[1], dtype='int64')
    loss_out = Lambda(ctc_lambda_func, output_shape=(1,), name='ctc')([y_pred, labels, input_length, label_length])
    model = Model(inputs=[input, labels, input_length, label_length], outputs=[loss_out])
    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True, clipnorm=5)
    # model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer='adadelta')
    model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=sgd)
    model.summary()
    return model, basemodel



def color_preprocessing(x_train,x_test):
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    for i in range(3):
        x_train[:,:,:,i] = (x_train[:,:,:,i] - mean[i]) / std[i]
        x_test[:,:,:,i] = (x_test[:,:,:,i] - mean[i]) / std[i]

    return x_train, x_test


# def gen(x_train, y_train):
#     while True:
#         for i in range(0,128,len(x_train)-128):
#             yield [x_train[i:i+128], y_train[i:i+128],
#                    np.ones(batch_size) * max_steps,
#                    np.ones(batch_size) * (num_classes-1)], \
#                    np.ones(batch_size)


def gen(x_train, y_train):
    length = int(img_col / 4) - 1
    while True:
        for i in range(0,128,len(x_train)-128):
            yield [x_train[i:i+128], y_train[i:i+128],
                   np.ones(batch_size) * length,
                   np.ones(batch_size) * max_steps], \
                   np.ones(batch_size)



def decode(label_arr):
    raw = ''
    res = ''
    for label in label_arr:
        index = list(label).index(max(label))
        char = str(index)
        raw += char
    print(raw)
    i = 0
    while i < len(raw)-2:
        if raw[i]==raw[i+1] and raw[i+1]==raw[i+2]:
            res += raw[i]
            i = i+3
        elif raw[i]==raw[i+1]:
            res += raw[i]
            i = i+2
        else:
            i += 1
    return res

if __name__ == '__main__':
    with open("dataset_only_num.pkl", "rb+") as f:
        data = pk.load(f)
        x_ = []
        y = []
        for i in data:
            x_.append(np.array(i[0]))
            y.append(np.array(i[1]))


    x = np.array(x_)
    y = np.array(y)
    x = x.reshape(len(x), img_row, img_col, 3)
    d = int(2 / 3 * len(x))

    x_train, x_test = x[:d], x[d:]
    y_train, y_test = y[:d], y[d:]
    x_train, x_test = color_preprocessing(x_train, x_test)

    model, basemodel = get_model()
    model.fit_generator(gen(x_train, y_train), steps_per_epoch=50,
                        epochs=epochs, verbose=1)
    basemodel.save('basemodel.h5')
    # basemodel = load_model('basemodel.h5')
    #
    # y_arr = basemodel.predict(x_test)
    # print(len(y_arr[0]))
    # print(decode(y_arr[0]))
    # print(y_test[0])
    # for y, y_p in zip(y_test, y_arr):
    #     pass

