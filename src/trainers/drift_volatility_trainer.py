from trainers.trainer import TrainerException
from trainers.trainer import Trainer
from math import log, sqrt


class DriftVolatilityTrainerException(TrainerException):
    pass


class DriftVolatilityTrainer(Trainer):
    # ---  INIT  --- #
    # -------------- #
    def __init__(self, f=None, y=None, tDelta=1.0):
        if f is None:
            raise DriftVolatilityTrainerException(
                'Can not initialize DriftVolatilityTrainer with None '
                'drift volatility function'
            )
        if y is None:
            raise DriftVolatilityTrainerException(
                'Can not initialize DriftVolatilityTrainer with None y'
            )
        if len(y) < 1:
            raise DriftVolatilityTrainerException(
                'Can not initialize DriftVolatilityTrainer with y having '
                'less than 1 element'
            )
        if len(y[0]) < 2:
            raise DriftVolatilityTrainerException(
                'Can not initialize DriftVolatilityTrainer with y elements '
                'not having at least:\n'
                '\t[t, v] as first and second elements'
            )
        if tDelta is None:
            raise DriftVolatilityTrainerException(
                'Can not initialize DriftVolatilityTrainer with None tDelta'
            )
        if tDelta < 0.0:
            raise DriftVolatilityTrainerException(
                'Can not initialize DriftVolatilityTrainer with tDelta < 0.0'
            )
        self.f = f
        self.y = y
        self.tDelta = tDelta

    # ---  TRAIN  --- #
    # --------------- #
    def train(self):
        r = self.calcR(self.y)
        mu = self.calcMu(r)
        variance = self.calcVariance(r, mu)
        sigma = self.calcSigma(variance, self.tDelta)
        return mu, sigma

    # ---  INNER FUNCTIONS  --- #
    # ------------------------- #
    def calcR(self, y):
        return [
            log(y[i][1]/y[i-1][1]) for i in range(1, len(y))
        ]

    def calcMu(self, r):
        return sum(r) / len(r)

    def calcVariance(self, r, mu):
        return sum([
            (ri-mu) * (ri-mu) for ri in r
        ]) / (len(r)-1)

    def calcSigma(self, variance, tDelta):
        return sqrt(variance)/sqrt(tDelta)
