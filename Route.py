#!/usr/bin/env python

class Route:
    def __init__(self, dist, wTime, bTime):
        self.mDistance = dist
        self.mWalkTime = wTime
        self.mBusTime = bTime

    def getAcceptablePossibility(self):
        return 0.5

    def getAcceptable(self):
        return self.getAcceptablePossibility() >= 0.5

    def __lt__(self, other):
        return self.getAcceptablePossibility() < other.getAcceptablePossibility()
    def __gt__(self, other):
        return self.getAcceptablePossibility() > other.getAcceptablePossibility()

