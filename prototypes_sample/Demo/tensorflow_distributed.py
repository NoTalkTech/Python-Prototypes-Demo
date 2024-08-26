# -*- coding: UTF-8 -*-
"""
Description: Tensorflow Distributed Cluster Mode
Author: Wallace Huang
Date: 2019/12/13
Version: 1.0
Requirements: tensorflow(<= 1.12.0)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os

# 导入 TensorFlow 和 TensorFlow 数据集
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras


# tfds.disable_progress_bar()


def main(argv):
    FLAGS = tf.app.flags.FLAGS
    tf.app.flags.DEFINE_string("job_name", "worker", "启动服务类型，ps或者worker")
    tf.app.flags.DEFINE_integer("task_index", 0, "指定是哪一台服务器索引")
    # 集群描述
    cluster = tf.train.ClusterSpec({
        "ps": ["127.0.0.1:4466"],
        "worker": ["127.0.0.1:4455"]
    })

    # 创建不同的服务
    server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

    if FLAGS.job_name == "ps":
        server.join()
    else:
        work_device = "/job:worker/task:0/cpu:0"
        with tf.device(tf.train.replica_device_setter(worker_device=work_device, cluster=cluster)):
            # 全局计数器
            global_step = tf.train.get_or_create_global_step()

            # 准备数据
            mnist = keras.datasets.mnist

            # 建立数据的占位符
            with tf.variable_scope("data"):
                x = tf.placeholder(tf.float32, [None, 28 * 28])
                y_true = tf.placeholder(tf.float32, [None, 10])

            # 建立全连接层的神经网络
            with tf.variable_scope("fc_model"):
                # 随机初始化权重和偏重
                weight = tf.Variable(tf.random_normal([28 * 28, 10], mean=0.0, stddev=1.0), name="w")
                bias = tf.Variable(tf.constant(0.0, shape=[10]))
                # 预测结果
                y_predict = tf.matmul(x, weight) + bias

            # 所有样本损失值的平均值
            with tf.variable_scope("soft_loss"):
                loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

            # 梯度下降
            with tf.variable_scope("optimizer"):
                train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss, global_step=global_step)

            # 计算准确率
            with tf.variable_scope("acc"):
                equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
                accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

        # 创建分布式会话
        with tf.train.MonitoredTrainingSession(
                checkpoint_dir="./temp/ckpt/test",
                master="grpc://127.0.0.1:4455",
                is_chief=(FLAGS.task_index == 0),
                config=tf.ConfigProto(log_device_placement=True),
                hooks=[tf.train.StopAtStepHook(last_step=100)]
        ) as mon_sess:
            while not mon_sess.should_stop():
                mnist_x, mnist_y = mnist.train.next_batch(4000)

                mon_sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})

                print("训练第%d步, 准确率为%f" % (
                    global_step.eval(session=mon_sess),
                    mon_sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y})))


def scale(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255
    return image, label


# 衰减学习率的函数。
# 您可以定义所需的任何衰减函数。
def decay(epoch):
    if epoch < 3:
        return 1e-3
    elif 3 <= epoch < 7:
        return 1e-4
    else:
        return 1e-5


# 在每个 epoch 结束时打印LR的回调（callbacks）。
class PrintLR(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print('\nLearning rate for epoch {} is {}'.format(epoch + 1, model.optimizer.lr.numpy()))


if __name__ == '__main__':
    # tf.app.run()

    # 下载数据集
    datasets, info = tfds.load(name='mnist', with_info=True, as_supervised=True)
    mnist_train, mnist_test = datasets['train'], datasets['test']

    # 定义分配策略
    strategy = tf.distribute.MirroredStrategy()
    print('Number of devices: {}'.format(strategy.num_replicas_in_sync))

    # 设置输入管道（pipeline）
    num_train_examples = info.splits['train'].num_examples
    num_test_examples = info.splits['test'].num_examples
    BUFFER_SIZE = 10000
    BATCH_SIZE_PER_REPLICA = 64
    BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync
    train_dataset = mnist_train.map(scale).cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    eval_dataset = mnist_test.map(scale).batch(BATCH_SIZE)

    # 创建和编译 Keras 模型
    with strategy.scope():
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=tf.keras.optimizers.Adam(),
                      metrics=['accuracy'])

    # 定义回调（callback)
    '''定义检查点（checkpoint）目录以存储检查点（checkpoints）'''
    checkpoint_dir = './training_checkpoints'
    '''检查点（checkpoint）文件的名称'''
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir='./logs'),
        tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix,
                                           save_weights_only=True),
        tf.keras.callbacks.LearningRateScheduler(decay),
        PrintLR()
    ]

    # 训练和评估
    model.fit(train_dataset, epochs=12, callbacks=callbacks)

    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
    eval_loss, eval_acc = model.evaluate(eval_dataset)
    print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))

    # 导出到 SavedModel
    path = 'saved_model/'
    tf.keras.experimental.export_saved_model(model, path)

    # 加载模型
    unreplicated_model = tf.keras.experimental.load_from_saved_model(path)
    unreplicated_model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam(),
        metrics=['accuracy'])

    eval_loss, eval_acc = unreplicated_model.evaluate(eval_dataset)
    print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))
