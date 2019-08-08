from trainers.functions.dualvar_trainer_function \
    import DualvarTrainerFunction, DualvarTrainerFunctionException


class DualvarTimeTrainerFunctionException(DualvarTrainerFunctionException):
    pass


class DualvarTimeTrainerFunction(DualvarTrainerFunction):
    # ---  INIT  --- #
    # -------------- #
    def __init__(self, x0=None, x1=None, y=None):
        super().__init__(x0=x0, x1=x1)
        self.y = y

    # ---  C A L C  --- #
    # ----------------- #
    def calc(self):
        raise DualvarTimeTrainerFunctionException(
            'DualvarTimeTrainerFunction is an abstract class which "calc" '
            'method can not be used'
        )
