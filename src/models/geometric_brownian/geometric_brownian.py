from models.model import ModelException
from models.model import Model
import numpy as np


class GeometricBrownianMotionException(ModelException):
    pass


class GeometricBrownianMotion(Model):
    # ---  I N I T  --- #
    # ----------------- #
    def __init__(self, **kwargs):
        super(GeometricBrownianMotion, self).__init__()
        self.mu = kwargs['mu']
        self.sigma = kwargs['sigma']

    # ---  VALIDATE  --- #
    # ------------------ #
    def validate(self):
        if not isinstance(self.mu, float):
            raise GeometricBrownianMotionException(
                'MU is not a valid decimal number'
            )
        if not isinstance(self.sigma, float):
            raise GeometricBrownianMotionException(
                'SIGMA is not a valid decimal number'
            )

    # ---  CALCULUS  --- #
    # ------------------ #
    def calc(self, data0=None, n=10, seed=5):
        # Check
        if not isinstance(data0, float):
            raise GeometricBrownianMotionException(
                'Can not apply GeometricBrownianMotion to None data'
            )

        if n < 1:
            raise GeometricBrownianMotionException(
                'GeometricBrownianMotion does not make sense with n < 1'
            )

        # Compute
        wienerProcess = self.computeWienerProcess(n, seed=seed)
        return [
            self._calc(data0=data0, t=i, wienerProcess=wienerProcess)
            for i in range(n)
        ]

    def _calc(self, data0=None, t=0, wienerProcess=None):
        # data0 -> t0
        if t == 0:
            return data0
        # ti , i > 0
        return data0 * np.exp(
            (self.mu - np.power(self.sigma, 2.0)/2.0) * t +
            (self.sigma * wienerProcess[t])
        )

    def computeWienerProcess(self, n, seed=5):
        np.random.seed(seed)
        dt = 1./n
        b = np.random.normal(0., 1., int(n))*np.sqrt(dt)
        w = np.cumsum(b)
        return np.insert(w, 0, 0.0).tolist()
