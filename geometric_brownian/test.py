import numpy as np
import matplotlib.pyplot as plt

from geometric_brownian import GeometricBrownianMotion


def generateTestData(n=10):
    return [
        x*100+1000 for x in np.random.rand(n).tolist()
    ]


# ---  M A I N  --- #
# ----------------- #
if __name__ == '__main__':
    # Prepare
    deep = 10
    n = 100
    data = generateTestData(n=n)
    # estimator = GeometricBrownianMotion(
    #    mu=np.log(np.mean(data)),
    #    sigma=np.log(np.std(data))
    # )
    estimator = GeometricBrownianMotion(
        mu=1.0,
        sigma=1.4
    )

    # Calculate
    estimations = [estimator.calc(
        data0=data[0],
        n=n,
        seed=np.random.randint(0, 1337)
    ) for i in range(deep)]

    # Plot
    print(data)
    # plt.plot(range(n), estimations)
    plt.scatter(range(n), data)
    for estimation in estimations:
        # plt.scatter(range(n), estimation)
        plt.plot(range(n), estimation)

    plt.show()
