from trainers.functions.trainer_function import TrainerFunction, \
    TrainerFunctionException


class DualvarTrainerFunctionException(TrainerFunctionException):
    pass


class DualvarTrainerFunction(TrainerFunction):
    # ---  INIT  --- #
    # -------------- #
    def __init__(self, x0=None, x1=None):
        self.validateX0X1(x0, x1)
        self.x0 = x0
        self.x1 = x1

    # ---  VALIDATION  --- #
    # -------------------- #
    @classmethod
    def validateX0X1(cls, x0, x1):
        cls._validateX0X1(x0, 'x0')
        cls._validateX0X1(x1, 'x1')

    @classmethod
    def _validateX0X1(cls, var=None, name=None):
        if name is None:
            raise DualvarTrainerFunctionException(
                'Can not _validateX0X1 with None name'
            )
        if not isinstance(var, float):
            raise DualvarTrainerFunctionException(
                'Can not _validateX0X1 if var {name} is not float '
                .format(name=name)
            )
