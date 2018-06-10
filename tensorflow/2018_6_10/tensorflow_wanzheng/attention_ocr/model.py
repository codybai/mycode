import sys
import collections
import logging
import tensorflow as tf
from tensorflow.contrib import slim
from tensorflow.contrib.slim.nets import inception

import metrics
import sequence_layers
import utils

OutputEndpoints = collections.namedtuple('OutputEndpoints',['chars_logit',
                                                            'chars_log_prob',
                                                            'predicted_chars',
                                                            'predicted_scores',
                                                            'predicted_text'])
ModelParams = collections.namedtuple('ModelParams',['num_char_classes','seq_length','num_views','null_code'])

ConvTowerParams = collections.namedtuple('ConvTowerParams',['final_endpoint'])
SequenceLogitsParams = collections.namedtuple('SequenceLogistsParams',['use_attention','use_autoregression','num_lstm_units','weight_decay','lstm_state_clip_value'])
SequenceLossParams = collections.namedtuple('SequenceLossParams',['label_smoothing','ignore_nulls','average_across_timesteps'])
EncodeCoordinatesParams = collections.namedtuple('EncodeCoordinatesParams',['endabled'])

def _dict_to_array(id_to_char,default_character):
    num_char_classes = max(id_to_char.keys()) +1
    array = [default_character] * num_char_classes
    for k, v in id_to_char.iteritems():
        array[k] = v
    return array

class CharsetMapper(object):
    def __init__(self,charset,default_character='?'):
        mapping_strings = tf.constant(_dict_to_array(charset,default_character))
        self.table = tf.contrib.lookup.index_to_string_table_from_tensor(
            mapping = mapping_strings,default_value = default_character
        )
def get_text(self,ids):
    return tf.reduce_join(
        self.table.lookup(tf.to_int64(ids)),reduction_indices=1
    )

def get_softmax_loss_fn(label_smoothing):
    if label_smoothing > 0:
        def loss_fn(labels,logits):
            return (tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=labels))
    else:

        def loss_fn(labels,logits):
            return tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits=logits,labels = labels
            )
    return loss_fn
class Model(object):
    def __init__(self,
                 num_char_classes,  #字符的大小，类别
                 seq_length,        #一个序列中字符的长度
                 num_views,          #卷积towers的数量
                 null_code,         #sequence结束的标识符
                 mparams=None,      #一个字典，根据mparams来选择调用不同的函数
                 charset=None,):    #
        super(Model,self).__init__()
        self._params = ModelParams(
            num_char_classes=num_char_classes,
            seq_length= seq_length,
            num_views=num_views,
            null_code=null_code
        )
        self._mparams = self.default_mparams()
        if mparams:
            self._mparams.update(mparams)
        self._charset = charset
    def default_mparams(selfs):
        return{
            'conv_tower_fn':
            ConvTowerParams(final_endpoint='Mixed_5d')
            'sequence_logit_fn':
            SequenceLogitsParams(use_attention=True,
                                 use_autoregression=True,
                                 num_lstm_units=256,
                                 weight_decay=0.00004,
                                 lstm_state_clip_value=10.0),
            'sequence_loss_fn':
            SequenceLossParams(label_smoothing=0.1,
                               ignore_nulls=True,
                               average_across_timesteps=False),
            'encode_coordinates_fn':
            EncodeCoordinatesParams(endabled=False)
        }
    def set_mparam(self,function,**kwargs):
        self._mparams[function] = self._mparams[function]._replace(**kwargs)

    def conv_tower_fn(self,images, is_training = True, reuse = None):
        mparams = self._mparams['conv_tower_fn']
        logging.debug('Using final_endpoint=%s',mparams.final_endpoint)
        if reuse:
            tf.get_variable_scope().reuse_variables()
        with slim.arg_scope(inception.inception_v3_arg_scope()):  #用slim.arg_scope设置默认参数，但是，设置参数需要用于被@add_arg_scope修饰过的参数，见源码
            with slim.arg_scope([slim.batch_norm,slim.dropout],is_training=is_training):
                net,_ = inception.inception_v3_base(images,final_endpoint=mparams.final_endpoint)
                return net
    def _create_lstm_inputs(self,net):  #net好像是featuresmap  就是那个长特征向量
        num_features = net.get_shape().dims[1].value
        if num_features < self._params.seq_length:
            raise AssertionError('Incorrect dimension #1 of input tensor'
                                 '%d should be bigger than %d (shape=%s') % (num_features,self._params.seq_length,net.get_shape())
        elif num_features>self._params.seq_length:
            logging.warning('Ignoring some features: use %d of %d (shape=%s)',
                            self._params.seq_length,num_features,net.get_shape())
            net = tf.slice(net,[0,0,0],[-1,self._params.seq_length,-1])#？？？？？？？
        return tf.unstack(net,axis=1)
    def sequence_logit_fn(self,net,labels_one_hot):
        mparams = self._mparams['sequence_logit_fn']
        with tf.variable_scope('sequence_logit_fn/SQLR'):
            layer_class = sequence_layers.get_layer_class(mparams.use_attention,mparams.use_autoregression)
            layer = layer_class(net,labels_one_hot,self._params,mparams)
            return layer.create_logits()
    def max_pool_views(self,nets_list):
        batch_size,height,width,num_features = [d.value for d in nets_list[0].get_shape().dims]
        xy_flat_shape = (batch_size,1,height*width,num_features)
        nets_for_merge=[]
        with tf.variable_scope('max_pool_views',values=nets_list):
            for net in nets_list:
                nets_for_merge.append(tf.reshape(net,xy_flat_shape))
            merged_net = tf.concat(nets_for_merge,1)
            net = slim.max_pool2d(
                merged_net,kernel_size=[len(nets_list),1],stride=1
            )
            net = tf.reshape(net,(batch_size,height,width,num_features))
        return net
    def pool_views_fn(self,nets):#net = [batch_size,,,feature_size]
        with tf.variable_scope('pool_views_fn/STCK'):
            net = tf.concat(nets,1)
            bath_size = net.get_shape().dims[0].value
            feature_size = net.get_shape().dims[3].value
            return tf.reshape(net,[bath_size,-1,feature_size])
    def char_predictions(self,chars_logit):
        log_prob = utils.logits_to_log_prob(chars_logit)
        ids = tf.to_int32(tf.argmax(log_prob,axis=2),name = 'predicted_chars')
        mask = tf.cast(
            slim.one_hot_encoding(ids,self._params.num_char_classes),tf.bool
        )
        all_scores = tf.nn.softmax(chars_logit)
        selected_scores = tf.boolean_mask(log_prob,mask,name='char_scores')
        scores = tf.reshape(selected_scores,shape=(-1,self._params.seq_length))
        return ids,log_prob,scores
    def encode_coordinates_fn(self,net):
        mparams = self._mparams['encode_coordinates_fn']
        if mparams.enabled:
            batch_size,h,w,_=net.get_shape.as_list()
            x,y = tf.meshgrid(tf.range(w),tf.range(h))






















