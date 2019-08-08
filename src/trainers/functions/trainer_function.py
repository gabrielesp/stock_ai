from trainers.trainer import TrainerException


class TrainerFunctionException(TrainerException):
    pass


class TrainerFunction:
    # --- ABSTRACT FUNCTIONS --- #
    # -------------------------- #
    def calc(self):
        raise TrainerFunctionException(
            'TrainerFunction is an abstract class which "calc" method can not '
            'be used'
        )
