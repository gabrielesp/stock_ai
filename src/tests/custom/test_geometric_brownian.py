import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from models.geometric_brownian import GeometricBrownianMotion


def generateTestData(n=10):
    return list(enumerate([
        x*100+1000 for x in np.random.rand(n).tolist()
    ]))


def obtainData(path=None, n=10):
    if path is None:
        return generateTestData(n=n)

    vals = pd.read_csv(path, delimiter='\t')['Low']\
        .dropna(axis=0)\
        .to_list()
    print(vals)
    n = len(vals)
    return [[t, vals[t]] for t in range(n)]


# ---  M A I N  --- #
# ----------------- #
if __name__ == '__main__':
    # Prepare
    deep = 100
    n = 100
    if len(sys.argv) > 1:
        data = obtainData(path=sys.argv[1])
        n = len(data)
    else:
        data = generateTestData(n=n)
    # estimator = GeometricBrownianMotion(
    #    mu=np.log(np.mean(data)),
    #    sigma=np.log(np.std(data))
    # )
    estimator = GeometricBrownianMotion(
        mu=0.00198790113187,
        sigma=0.009181598109527
    )

    # Calculate
    estimations = [estimator.calc(
        data0=data[0][1],
        n=n,
        seed=np.random.randint(0, 1337)
    ) for i in range(deep)]

    # Plot
    print(data)
    # plt.plot(range(n), estimations)
    plt.scatter(range(n), [v for [t,v] in data])
    for estimation in estimations:
        # plt.scatter(range(n), estimation)
        plt.plot(range(n), estimation)

    plt.show()
