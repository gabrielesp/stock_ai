from trainers.dualvar_time_trainer import DualvarTimeTrainer
from models.geometric_brownian import GeometricBrownianMotion
import time

# ---  GLOBAL VARS  --- #
# --------------------- #
y0 = None  # First y value (must be known for the geometric brownian
n = 10  # Number of samples


# ---  FUNCTIONS  --- #
# ------------------- #
def dualvarTimeFunction(t, x0, x1):
    model = GeometricBrownianMotion(mu=x0, sigma=x1)
    wienerProcess = model.computeWienerProcess(n)
    result = model._calc(
        data0=y0[1],
        t=t,
        wienerProcess=wienerProcess
    )
    return result


def obtainDualvarTimeY():
    return [[v, v*2] for v in range(n)]


# ---  M A I N  --- #
# ----------------- #
if __name__ == '__main__':
    # Obtain data
    dualvarTimeY = obtainDualvarTimeY()
    y0 = dualvarTimeY[0]

    # Instantiate trainer
    dvtTrainer = DualvarTimeTrainer(
        f=dualvarTimeFunction,
        y=dualvarTimeY
    )

    # Train
    print('Training ... ')
    start = time.perf_counter()
    x0, x1, minError, maxError, avgError, deltaError = \
        dvtTrainer.train(
            searchFactor=2,
            searchSteps=1,
            searchDeep=8
        )
    end = time.perf_counter()
    print('Trained in {s} seconds'.format(s=end-start))

    # Summary
    print(
        '\n\n\t\t SUMMARY\n'
        '\t---------------\n'
        'Min error of {minerr} was found for [mu={x0}  ,  sigma={x1}]\n'
        '\tMax found error was {maxerr}\n'
        '\tAverage error was {avgerr}\n'
        '\tDelta error was {derr}\n'
        .format(
            minerr=minError,
            x0=x0,
            x1=x1,
            maxerr=maxError,
            avgerr=avgError,
            derr=deltaError
        )
    )
