import sys
from tensorflow.python.platform import flags
import logging
import datasets
import model
FLAGE = flags.FLAGS

logging.basicConfig(
    level = logging.DEBUG,
    stream = sys.stderr,
    format = '%(levelname)s  '
             '%(asctime)s.%(msecs)06d: '
             '%(filename)s: '
             '%(lineno)d  '
             '%(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S')
def define():
    """定义通用FLAGE"""
    #yaph: disable  #好像是一个谷歌开源的工具，整理python代码用的
    flags.DEFINE_integer('batch_size',32,'Batch_size的大小.')
    flags.DEFINE_integer('crop_width',None,'Width of the central crop for images.')
    flags.DEFINE_integer('crop_height',None,'Height of the central crop for images')
    flags.DEFINE_string('train_log_dir','tmp/attention_ocr/train','保存是日志的路径')
    flags.DEFINE_string('dataset_name','fsns','数据集的名字，由fsns支持')
    flags.DEFINE_string('split_name','train','Dataset split name to run evaluation for :test,train.')
    flags.DEFINE_string('dataset_dir',None,'Dataset root folder.')
    flags.DEFINE_string('checkpoint','',"恢复模型的路径")
    flags.DEFINE_string('master','','BNS name of the tenforflow master to use')


    #超参数
    flags.DEFINE_float('learning_rate',0.004,'learning rate')
    flags.DEFINE_string('optimizer','momentum','the optimizer to use')
    flags.DEFINE_float('momentum',0.9,'momentum value for the momentum optimizer if used')
    flags.DEFINE_bool('use_augment_input',True,'If True will use image augmentation')


    #超参数方法
    #conv_tower_fn
    flags.DEFINE_string('final_endpoint','Mixed_5d','Endpoint to cut inception tower')

    #sequence_logit_fn
    flags.DEFINE_bool('use_attention',True,'If True will use the attention mechanism')
    flags.DEFINE_bool('use_autoregression',True,'If True will use autoregression(a feedback link)')
    flags.DEFINE_integer('num_lstm_units',256,'number of LSTM units for sequence LSTM')
    flags.DEFINE_float('weight_decay',0.00004,'字符预测全连接层权重的衰减')
    flags.DEFINE_float('lstm_state_clip_value',10.0,'单元状态在输出被激活前被修正')


    #sequence_loss_fn
    flags.DEFINE_float('label_smoothing',0.1,'标签平滑移动的权重')
    flags.DEFINE_bool('ignore_nulls',True,'计算loss的时候，忽略空字符串')
    flags.DEFINE_bool('average_across_timesteps',False,'通过总的标签的权重来分割返回来的代价')

def get_crop_size():
    if FLAGE.crop_width and FLAGE.crop_height:
        return (FLAGE.crop_width,FLAGE.crop_height)
    else:
        None
def create_dataset(split_name):
    ds_module  = getattr(datasets,FLAGE.dataset_name)
    return ds_module.get_split(split_name,dataset_dir=FLAGE.dataset_dir)
def create_mparams():
    return{
        'conv_tower_fn':
            model.
    }











































