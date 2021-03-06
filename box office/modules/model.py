# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gk3AbWwY1hX3SibQCMjh4r6pcVQexVWD
"""

import tensorflow as tf
from keras import regularizers
from keras import optimizers
def create_model(input_size):

  model = tf.keras.Sequential([
          tf.keras.layers.Input(shape=(input_size, )),
          tf.keras.layers.Dense(356,activation='relu',kernel_regularizer=regularizers.l1(.001)),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(256,kernel_regularizer=regularizers.l1(.001),activation='relu'),
          tf.keras.layers.Dense(units = 1)

  ])

  model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=.001),loss='mse', metrics=['mean_squared_logarithmic_error'])
  return model