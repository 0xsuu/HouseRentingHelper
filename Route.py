#!/usr/bin/env python

import numpy as np

class Route:
    def __init__(self, dist, wTime, bTime, MLPredictAcceptableRate=False):
        self.mDistance = dist
        self.mWalkTime = wTime
        self.mBusTime = bTime
        if MLPredictAcceptableRate:
            from keras.models import load_model
            self.mModel = load_model("RouteModel.h5")
            self.mModel.load_weights("RouteModelWeights.h5")

    # This function requires MLPredictAcceptableRate to be true.
    def getAcceptablePossibility(self):
        return self.mModel.predict(np.array([[self.mDistance, self.mWalkTime, self.mBusTime]]))[0][0]

    # This function requires MLPredictAcceptableRate to be true.
    def getAcceptable(self):
        return self.getAcceptablePossibility() >= 0.5

    # This function requires MLPredictAcceptableRate to be true.
    def __lt__(self, other):
        return self.getAcceptablePossibility() < other.getAcceptablePossibility()
    # This function requires MLPredictAcceptableRate to be true.
    def __gt__(self, other):
        return self.getAcceptablePossibility() > other.getAcceptablePossibility()

