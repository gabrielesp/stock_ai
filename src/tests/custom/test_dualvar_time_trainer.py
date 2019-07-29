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
    return model._calc(
        data0=y0,
        t=t,
        wienerProcess=wienerProcess
    )


def obtainDualvarTimeY():
    return [[v, v*2] for v in range(n)]


# ---  M A I N  --- #
# ----------------- #
if __name__ == '__main__':
    # Obtain data

    # Obtain dualvar time y
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
    dvtTrainer.train(
        searchFactor=2,
        searchSteps=4,
        searchDeep=64
    )
    end = time.perf_counter()
    print('Trained in {s} seconds'.format(s=end-start))
