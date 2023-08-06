import tensorflow as tf


class Model(tf.keras.Model):
    def __init__(self,final_activation,out_units,hp):
        super().__init__()

        self.layer_list = []
        hidden_layers = []

        for i in range(hp.Int('num_layers', 1, 5)):
            hidden_layers.append(hp.Int('units_' + str(i),
                                        min_value=32,
                                        max_value=512,
                                        step=32))

        a = hidden_layers

        for i,units in enumerate(hidden_layers):

            if i != len(hidden_layers) -1:   #不是最后一层的时候，激活函数为rule
                exec("self.layer{} = tf.keras.layers.Dense(units=units,activation='relu' )".format(i))
            else:
                exec("self.layer{} = tf.keras.layers.Dense(units=out_units,activation='{}')".format(i,final_activation))

            exec('self.layer_list.append(self.layer{})'.format(i))
            self.layer_list.append(tf.keras.layers.Dropout(hp.Choice('drop_rate', values=[0.1, 0.2, 0.3, 0.4])))

        self.layer_list = self.layer_list[:-1]

    def call(self, x):

        for layer in  self.layer_list:
            x = layer(x)


        return x



