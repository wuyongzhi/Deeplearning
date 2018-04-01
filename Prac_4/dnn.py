# -*- coding: utf-8 -*-
from keras.layers import Input, Dense, Dropout
from keras import Model
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras import backend as K
from sklearn.metrics import average_precision_score
np.set_printoptions(suppress=True)


class DNN_Model(object):
    def __init__(self, data_x, batch_size):
        self.shape = data_x.shape[1]
        self.batch_size = batch_size

    def build_model(self):
        x_input = Input(shape=(self.shape,))
        x_dense_1 = Dense(units=64, activation='relu', use_bias=True)(x_input)
        x_dropout_1 = Dropout(rate=0.2)(x_dense_1)
        x_dense_2 = Dense(units=128, activation='relu')(x_dropout_1)
        x_dropout_2 = Dropout(rate=0.1)(x_dense_2)
        x_dense_3 = Dense(units=256, activation='relu', use_bias=True)(x_dropout_2)
        x_dense_4 = Dense(units=64, activation='relu', use_bias=True)(x_dense_3)
        y = Dense(units=1, activation='sigmoid')(x_dense_4)

        model = Model(inputs=x_input, outputs=y)
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        model.summary()
        self.model = model

    def train_model(self, x, y, epochs=30):
        if self.model is None:
            raise Exception("Please run obj.build_model() function")
        history = self.model.fit(x=x, y=y,
                                 batch_size=self.batch_size,
                                 epochs=epochs,
                                 verbose=2,
                                 validation_split=0.1)
        self.model.save("prac_4.h5")
        self.history = history

    def paint(self):
        print "刻画损失函数在训练与验证集的变化"
        plt.plot(self.history.history['loss'], label='train')
        plt.plot(self.history.history['val_loss'], label='valid')
        plt.legend()
        plt.show()

    def prediction(self, x):
        predicted = self.model.predict(x=x,
                                       batch_size=self.batch_size,
                                       verbose=2)
        return np.array(predicted)

    def score(self, x_t, y_t):
        score = self.model.evaluate(x_t, y_t,
                                    batch_size=self.batch_size)
        print(score)


if __name__ == '__main__':
    import load_file
    import write_file

    LoadData = load_file.LoadData()

    train_x, train_y, test_x, test_y = LoadData.train_test_data()

    dnn = DNN_Model(data_x=train_x, batch_size=64)
    dnn.build_model()
    dnn.train_model(train_x, train_y)
    dnn.paint()
    predictions = dnn.prediction(x=test_x)
    print(average_precision_score(y_true=test_y, y_score=predictions.flatten()))
    # write2file = write_file.Write_Csv()
    # write2file.write_file(predictions=predictions, title=['CaseId', 'Evaluation'], id=200001)