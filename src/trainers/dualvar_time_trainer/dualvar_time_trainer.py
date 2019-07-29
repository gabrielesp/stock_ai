from trainers.trainer import TrainerException
from trainers.trainer import Trainer


class DualvarTimeTrainerException(TrainerException):
    pass


class DualvarTimeTrainer(Trainer):
    # ---  INIT  --- #
    # -------------- #
    def __init__(self, f=None,  y=None):
        # Checks
        if f is None:
            raise DualvarTimeTrainerException(
                'Can not initialize DualvarTimeTrainer with None '
                'dualvar function'
            )
        if y is None:
            raise DualvarTimeTrainerException(
                'Can not initialize DualvarTimeTrainer with None y'
            )
        if len(y) < 1:
            raise DualvarTimeTrainerException(
                'Can not initialize DualvarTimeTrainer with y having '
                'less than 1 element'
            )
        if len(y[0]) < 2:
            raise DualvarTimeTrainerException(
                'Can not initialize DualvarTimeTrainer with y elements '
                'not having at least:\n'
                '\t[t, v] as first and second elements'
            )

        # Super init
        super(DualvarTimeTrainer, self).__init__()

        # Assigns
        self.f = f
        self.y = y

    # ---  TRAIN  --- #
    # --------------- #
    def train(self, searchFactor=2, searchSteps=4, searchDeep=64):
        # Genetic finding process : Start candidates
        x0Candidates = [
            -1000000, -100000, -10000, -1000, -100, -10, -8, -6, -5, -3,
            -2, -2.5, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2,
            -0.1
        ]
        x0Candidates = x0Candidates + [0] + \
            list(map(lambda x: abs(x), x0Candidates))
        x1Candidates = set(x0Candidates)
        x0Candidates = set(x0Candidates)

        # Genetic finding process : Already visited
        considered = set()  # Pairs [x0, x1]

        # Genetic finding process : Deep search
        minError = None
        maxError = None
        avgError = 0
        nError = 0
        x0 = None
        x1 = None
        for deep in range(searchDeep):
            # Debug print
            self.debugDeepPrint(deep, x0Candidates, x1Candidates)

            for x0c in x0Candidates:
                for x1c in x1Candidates:
                    if((x0c, x1c) in considered):
                        # Ignore already considered pairs
                        continue

                    # Get the error measure
                    error = self.errorMeasure(x0c, x1c)

                    # Minimum error as genetic criteria
                    if minError is None or error < minError:
                        minError = error
                        x0 = x0c
                        x1 = x1c

                    # Some error statistics (redesign to use
                    # DualvarTrainerResult if further statistics are desired)
                    if maxError is None or error > maxError:
                        maxError = error
                    avgError += error
                    nError += 1.0

                    # Remember this pair has already been considered
                    considered.add((x0c, x1c))

            # Expand candidates considering searchFactor and searchSteps
            x0Candidates = self.expandCandidates(
                candidatesSet=x0Candidates,
                searchFactor=searchFactor,
                searchSteps=searchSteps
            )
            if len(x0Candidates) < 1:
                break
            x1Candidates = self.expandCandidates(
                candidatesSet=x1Candidates,
                searchFactor=searchFactor,
                searchSteps=searchSteps
            )
            if len(x1Candidates) < 1:
                break

        # Return min error pair and error measures
        return x0, x1, minError, maxError, avgError/nError, maxError-minError

    # ---  INNER FUNCTIONS  --- #
    # ------------------------- #
    def errorMeasure(self, x0=None, x1=None):
        # Checks
        if x0 is None:
            raise DualvarTimeTrainerException(
                'DualvarTrainer can not measure error with None x0'
            )
        if x1 is None:
            raise DualvarTimeTrainerException(
                'DualvarTrainer can not measure error with None x1'
            )
        if self.f is None:
            raise DualvarTimeTrainerException(
                'DualvarTrainer can not measure error with None '
                'dualvar function'
            )
        if self.y is None:
            raise DualvarTimeTrainerException(
                'DualvarTrainer can not measure error with None y'
            )

        # Error measure
        error = 0.0
        for [t, v] in self.y:
            prediction = self.f(t, x0, x1)
            error += (prediction - v)**2
        return error

    def expandCandidates(
        self,
        candidatesSet=None,
        searchFactor=2,
        searchSteps=1
    ):
        # Checks
        if candidatesSet is None:
            raise DualvarTimeTrainerException(
                'DualvarTrainer can not expand candidates with None '
                'candidatesSet'
            )

        # Candidates expansion
        newCandidatesSet = set()
        for x in candidatesSet:
            forward = x
            backward = x
            for s in range(searchSteps):
                forward *= searchFactor
                backward /= searchFactor
                newCandidatesSet.add(forward)
                newCandidatesSet.add(backward)

        # Return new candidates set (candidates expansion)
        return newCandidatesSet

    # ---  D E B U G  --- #
    # ------------------- #
    def debugDeepPrint(self, deep, x0Candidates, x1Candidates):
        print(
            'Dualvar trainer genetic finding deep: {d}\n'
            '\tx0 candidates:\n\t\t{x0}\n'
            '\tx1 candidates:\n\t\t{x1}'
            .format(
                d=deep, x0=x0Candidates, x1=x1Candidates
            )
        )
