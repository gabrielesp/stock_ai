class GeometricBrownianMotionException(Exception):
    pass


class GeometricBrownianMotion:
    # ---  I N I T  --- #
    # ----------------- #
    def __init__(self, **kwargs):
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
