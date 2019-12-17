#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import tensorflow as tf
from tensorflow import keras


def tf_demo1():
    # Create 100 phony x, y data points in NumPy, y = x * 0.1 + 0.3
    x_data = np.random.rand(100).astype(np.float32)
    y_data = x_data * 0.1 + 0.3

    # Try to find values for W and b that compute y_data = W * x_data + b
    # (We know that W should be 0.1 and b 0.3, but TensorFlow will
    # figure that out for us.)
    W = tf.Variable(tf.random_uniform_initializer([1], -1.0, 1.0))
    b = tf.Variable(tf.zeros([1]))
    y = W * x_data + b

    # Minimize the mean squared errors.
    loss = tf.reduce_mean(tf.square(y - y_data))
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

    # Before starting, initialize the variables.  We will 'run' this first.
    init = tf.global_variables_initializer()

    # Launch the graph.
    sess = tf.Session()
    sess.run(init)

    # Fit the line.
    for step in range(201):
        sess.run(train)
        if step % 20 == 0:
            print("[TF_DEMO1] ==> ", step, sess.run(W), sess.run(b))

            # Learns best fit is W: [0.1], b: [0.3]


def tf_demo2():
    # 创建一个常量 op, 产生一个 1x2 矩阵. 这个 op 被作为一个节点
    # 加到默认图中.
    # 构造器的返回值代表该常量 op 的返回值.
    matrix1 = tf.constant([[3., 3.]])

    # 创建另外一个常量 op, 产生一个 2x1 矩阵.
    matrix2 = tf.constant([[2.], [2.]])

    # 创建一个矩阵乘法 matmul op , 把 'matrix1' 和 'matrix2' 作为输入.
    # 返回值 'product' 代表矩阵乘法的结果.R
    product = tf.matmul(matrix1, matrix2)

    # 启动默认图.
    sess = tf.Session()

    # 调用 sess 的 'run()' 方法来执行矩阵乘法 op, 传入 'product' 作为该方法的参数.
    # 上面提到, 'product' 代表了矩阵乘法 op 的输出, 传入它是向方法表明, 我们希望取回
    # 矩阵乘法 op 的输出.
    #
    # 整个执行过程是自动化的, 会话负责传递 op 所需的全部输入. op 通常是并发执行的.
    #
    # 函数调用 'run(product)' 触发了图中三个 op (两个常量 op 和一个矩阵乘法 op) 的执行.
    #
    # 返回值 'result' 是一个 numpy `ndarray` 对象.
    result = sess.run(product)
    print("[TF_DEMO2] ==> ", result)
    # ==> [[ 12.]]

    # 任务完成, 关闭会话.
    sess.close()


if __name__ == '__main__':
    mnist = keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')])
    model.summary()
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5)
    model.evaluate(x_test, y_test)
    # tf_demo1()
    # tf_demo2()
