class TrainerException(Exception):
    pass


class Trainer:
    # --- ABSTRACT FUNCTIONS --- #
    # -------------------------- #
    def train(self):
        # Must return a TrainingResult
        raise TrainerException(
            'Trainer is an abstract class which "train" method can not be used'
        )
