import collections
import logging
import tensorflow as tf
from tensorflow.contrib import slim
from tensorflow import app                              #运行mian函数用到
from tensorflow.python.platform import flags            #命令行参数
from tensorflow.contrib.tfprof import model_analyzer
import data_provider
import common_flags

FLAGS = flags.FLAGS
common_flags.define()
#yapf:disable

flags.DEFINE_integer('task',0,'The Task ID')
flags.DEFINE_integer('ps_tasks',0,'The number of parameter servers')
flags.DEFINE_integer('save_summaries_secs',60,'The frequency with which summaries are saved')
flags.DEFINE_integer('save_interval_secs',600,'保存模型的时间间隔（s）')
flags.DEFINE_integer('最大步数',int(1e10),'梯度步数的最大值')
flags.DEFINE_string('checkpoint_inception','','恢复inception权重的来源（估计是恢复模型吧）')
flags.DEFINE_float('梯度修正',2.0,'如果比零大，这个梯度就将被这个数字修正')
flags.DEFINE_bool('同步复制',False,'如果为真，在训练途中将会被同步这些付复制')
flags.DEFINE_integer('replicas_to_aggregate',1,'更新参数前梯度更新的数值')
flags.DEFINE_integer('复制备份的总数',1,'工作备份的总数')
flags.DEFINE_integer('启动衰减步数',15,'Number of training steps between replicas startup')
flags.DEFINE_boolean('重置训练目录',False,'如果为真，将会删除训练日志目录里面的所有文件')
flags.DEFINE_boolean('显示图状态',False,'在控制台输出模型大小的状态')
#yapf:enable
TrainingHParams = collections.namedtuple('TrainingHParams',[
    'learing_rate',
    'optimizer',
    'momentum',
    'use_augment_input',
])

def prepare_training_dir():
    if not tf.gfile.Exists(FLAGS.train_log_dir):
        logging.info('Create a new training directory %s', FLAGS.train_log_dir)
        tf.gfile.MakeDirs(FLAGS.train_log_dir)
    else:
        if FLAGS.reset_train_dir:
            logging.info('Reset the training directory %s',FLAGS.train_log_dir)
            tf.gfile.DeleteRecursively(FLAGS.train_log_dir)
        else:
            logging.info('Use already existing training directory %s',FLAGS.train_log_dir)

def main(_):
    prepare_training_dir()
    dataset = common
if __name__ == '__main__':
    app.run()