from trainers.trainer import TrainerException, Trainer
from trainers.functions.dualvar_trainer_function import DualvarTrainerFunction


class DualvarTrainerException(TrainerException):
    pass


class DualvarTrainer(Trainer):
    # ---  INIT  --- #
    # -------------- #
    def __init__(self,  f=None, y=None):
        # Checks
        if f is not DualvarTrainerFunction:
            raise DualvarTrainerException(
                'You need a DualvarTrainerFunction f to build a DualvarTrainer'
            )

        if y is None or len(y) < 1 or len(y[0]) < 2:
            raise DualvarTrainerException(
                'You need at least one collection with 1 element '
                'as y argument to build a DualvarTrainer.\n'
            )

        # Assigns
        self.f = f
        self.y = y

    # ---  TRAIN  --- #
    # --------------- #
    def train(self):
        pass  # TODO

