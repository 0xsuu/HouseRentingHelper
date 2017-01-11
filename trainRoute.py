#!/usr/bin/env python

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

import numpy as np

def train():
    model = Sequential()
    model.add(Dense(5, input_dim=3))
    model.add(Activation('sigmoid'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer=SGD(lr=0.1),
                  metrics=['accuracy'])

    X_train = []
    Y_train = []
    for distance in np.arange(0, 5, 0.1):
        for wT in range(0, 30):
            for bT in range(0, 25):
                X_train += [[distance, wT, bT]]
                Y_train += [[1]]
    for wT in range(0, 20):
        for distance in np.arange(2, 10, 0.1):
            for bT in range(0, 20):
                X_train += [[distance, wT, bT]]
                Y_train += [[1]]
    for bT in range(0, 15):
        for distance in np.arange(2,15, 0.2):
            for wT in range(15, 50):
                X_train += [[distance, wT, bT]]
                Y_train += [[1]]

    for distance in np.arange(10, 20, 0.1):
        for wT in range(20, 100):
            for bT in range(26, 100):
                X_train += [[distance, wT, bT]]
                Y_train += [[0]]

    model.fit(X_train, Y_train, batch_size=128, nb_epoch=6)

    X_cv = [[1, 5, 5], [3, 15, 4], [5, 35, 12], [4, 45, 25], [2, 10, 3], [6, 35, 35], [7, 50, 40], [3, 50, 50], [10, 60, 40], [6, 55, 35]]
    Y_cv = [[1], [1], [1], [1], [1], [0], [0], [0], [0], [0]]

    print model.predict(X_cv)
    print model.evaluate(X_cv, Y_cv)

