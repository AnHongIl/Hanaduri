import tensorflow as tf
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, output_size, learning_rate):
        with tf.variable_scope("main"):
            self.input_size = input_size
            self.output_size = output_size

            self.inputs = tf.placeholder(tf.float32, [None, input_size], name='inputs')
            self.targets = tf.placeholder(tf.int32, [None], name='targets')
            self.one_hot_targets = tf.one_hot(self.targets, output_size)

            self.hidden1 = tf.layers.dense(self.inputs, 10000, tf.nn.relu, name='hidden1')
            self.hidden2 = tf.layers.dense(self.hidden1, 1000, tf.nn.relu, name='hidden2')
            self.hidden3 = tf.layers.dense(self.hidden2, 100, tf.nn.relu, name='hidden3')

            self.output = tf.layers.dense(self.hidden3, output_size, tf.nn.softmax, name='output')

            self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.one_hot_targets, logits=self.output))
            self.opt = tf.train.AdamOptimizer(learning_rate).minimize(self.loss)


