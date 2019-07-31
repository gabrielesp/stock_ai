from trainers.dualvar_time_trainer import DualvarTimeTrainer
from models.geometric_brownian import GeometricBrownianMotion
import time
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


def obtainDualvarTimeY(path=None):
    global n

    # None path, so use fixed values
    if path is None:
        return [[v, 100+v*5] for v in range(n)]

    # Get values from path
    vals = pd.read_csv(path, delimiter='\t')['High'].to_list()
    n = len(vals)
    return [[t, vals[t]] for t in range(n)]


# ---  M A I N  --- #
# ----------------- #
# No args required
# However, if an arg is specified, it will be used as the path for
# data retrieving at obtainDualvarTimeY function
if __name__ == '__main__':
    # Obtain data
    dualvarTimeY = obtainDualvarTimeY(
        path=None if len(sys.argv) < 2 else sys.argv[1]
    )
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

    # Estimate
    estimator = GeometricBrownianMotion(
        mu=x0,
        sigma=x1
    )
    deep = 10
    estimations = [estimator.calc(
        data0=float(y0[1]),
        n=n,
        seed=np.random.randint(0, 1337)
    ) for i in range(deep)]

    # Plot
    plt.scatter(range(n), [y for [t, y] in dualvarTimeY])
    for estimation in estimations:
        plt.plot(range(n), estimation)
    plt.show()
