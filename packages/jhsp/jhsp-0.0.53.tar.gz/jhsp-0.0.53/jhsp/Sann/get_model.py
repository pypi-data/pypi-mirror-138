import tensorflow as tf
import pandas as pd
import sys
import os

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

from Sann.models import sann,sanntuner,anntuner
from Sann import getweights,weights22netweights
import tensorflow_addons as tfa



class GetSannModel():
    """
    返回SANN模型和网络结构一样的ANN模型
    """
    def __init__(self,x,y,how,weights):


        self.weights = weights
        self.out_units = y.shape[1]


        if how == 'mull':
            self.final_activation = 'sigmoid'
            self.loss = 'binary_crossentropy'
            self.metrics = 'accuracy'
        if how == 'mulc':
            self.final_activation = 'softmax'
            self.loss = 'categorical_crossentropy'
            self.metrics = 'accuracy'
        if how =='2c':
            self.final_activation = 'sigmoid'
            self.loss = 'binary_crossentropy'
            self.metrics = 'accuracy'

    # 标签还是分类 ，加一个参数
    def GetSann(self,hp):

        model = sanntuner.Model(self.weights, self.final_activation,hp)
        model.compile(loss=self.loss, optimizer='adam', metrics=[self.metrics])

        return model

    def GetAnn(self,hp):
        """
        获得与SANN网络结构一致的ANN
        :return:
        """

        model = anntuner.Model(self.final_activation,self.out_units,hp)
        model.compile(loss=self.loss, optimizer='adam', metrics=[self.metrics])

        return model

    def GetSannmyself(self,hidden_layers,drop_rate):


        weights = weights22netweights.W22NW().Weights2HW(self.weights,hidden_layers,save=False)[0]




        model = sann.Model(weights, self.final_activation,drop_rate)
        model.compile(loss=self.loss, optimizer=tf.keras.optimizers.Adam(0.3), metrics=['accuracy'])

        return model





