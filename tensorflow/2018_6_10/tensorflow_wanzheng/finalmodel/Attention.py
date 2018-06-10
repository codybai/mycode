from .config import *


def lstm_layer(x, batch_size, name):
    with tf.name_scope(name) as scope:
        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(lstm_hidden, reuse=False)
        init = lstm_cell.zero_state(batch_size, tf.float32)
        x, state = tf.nn.dynamic_rnn(lstm_cell, inputs=x, initial_state=init, scope=scope)
    return x


def seq2seq(x, batch_size):
    x = lstm_layer(x, batch_size, 'lstm1')
    x = lstm_layer(x, batch_size, 'lstm2')
    return x


