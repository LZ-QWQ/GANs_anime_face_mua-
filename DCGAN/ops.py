import math
import numpy as np 
import tensorflow as tf

class batch_norm(object):
  def __init__(self, name,epsilon=1e-5, momentum = 0.9 ):
    with tf.variable_scope(name):
      self.epsilon  = epsilon
      self.momentum = momentum
      self.name = name

  def __call__(self, x, training):
    return tf.contrib.layers.batch_norm(x,
                      decay=self.momentum, 
                      updates_collections=None,#这里None就强制更新了
                      epsilon=self.epsilon,
                      scale=True,
                      is_training=training,
                      scope=self.name)

def conv2d(input_, output_dim, 
       k_h=5, k_w=5, d_h=2, d_w=2, stddev=0.02,
       name="conv2d"):
  with tf.variable_scope(name):
    w = tf.get_variable('kernel', [k_h, k_w, input_.get_shape()[-1], output_dim],
              initializer=tf.truncated_normal_initializer(stddev=stddev))
    conv = tf.nn.conv2d(input_, w, strides=[1, d_h, d_w, 1], padding='SAME')

    biases = tf.get_variable('bias', [output_dim], initializer=tf.constant_initializer(0.0))
    conv = tf.reshape(tf.nn.bias_add(conv, biases), conv.get_shape())
    return conv

def deconv2d(input_, output_shape,name,
       k_h=5, k_w=5, d_h=2, d_w=2, stddev=0.02):
    with tf.variable_scope(name):
    # filter : [height, width, output_channels, in_channels]
        w = tf.get_variable('kernel', [k_h, k_w, output_shape[-1], input_.get_shape()[-1]],
              initializer=tf.random_normal_initializer(stddev=stddev))    
        deconv = tf.nn.conv2d_transpose(input_, w, output_shape=output_shape,
                strides=[1, d_h, d_w, 1])

        biases = tf.get_variable('bias', [output_shape[-1]], initializer=tf.constant_initializer(0.0))
        deconv = tf.nn.bias_add(deconv, biases)
    return deconv
     
def linear(input_, output_size,name, stddev=0.02, bias_start=0.0):
    shape = input_.get_shape().as_list()
    with tf.variable_scope(name):
        matrix = tf.get_variable("kernel", [shape[1], output_size], tf.float32,
                 tf.random_normal_initializer(stddev=stddev))
        bias = tf.get_variable("bias", [output_size],
        initializer=tf.constant_initializer(bias_start))
    return tf.matmul(input_, matrix) + bias