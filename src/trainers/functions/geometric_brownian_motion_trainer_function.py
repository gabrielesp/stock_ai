from trainers.functions.dualvar_time_trainer_function \
    import DualvarTimeTrainerFunction, DualvarTimeTrainerFunctionException
from models.geometric_brownian_motion import GeometricBrownianMotion


class GeometricBrownianMotionTrainerFunctionException(
        DualvarTimeTrainerFunctionException):
    pass


class GeometricBrownianMotionTrainerFunction(DualvarTimeTrainerFunction):
    # ---  I N I T  --- #
    # ----------------- #
    def __init__(self, x0=None, x1=None, y=None):
        super().__init__(x0=x0, x1=x1, y=y)

        # Checks
        if y is None or len(y) < 1:
            raise GeometricBrownianMotionTrainerFunctionException(
                'GeometricBrownianMotionTrainerFunction can not be built '
                'if y\n'
                'is not a collection with at least 1 element'
            )

        # Assigns
        self.model = GeometricBrownianMotion(mu=x0, sigma=x1)
        self.wienerProcess = self.model.computeWienerProcess(
            n=len(y),
            seed=5
        )

    # ---  C A L C  --- #
    # ----------------- #
    def calc(self, t=None):
        # Check
        if not isinstance(t, int):
            raise GeometricBrownianMotionTrainerFunctionException(
                'GeometricBrownianMotionTrainerFunction can not calculate if '
                't is not a int as time index'
            )
        if len(self.wienerProcess) <= t:
            raise GeometricBrownianMotionTrainerFunctionException(
                'GeometricBrownianMotionTrainerFunction can not calculate if '
                't ({t}) is not smaller than length of wienerProcess ({wn})'
                .format(wn=len(self.wienerProcess))
            )

        # Calculate
        return self.model._calc(
            data0=self.y[0],
            t=t,
            wienerProcess=self.wienerProcess
        )
