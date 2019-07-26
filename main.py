import pandas as pd
import numpy as np
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from models.geometric_brownian.geometric_brownian \
    import GeometricBrownianMotion


def get_stats(s, n=252):
    s = s.dropna()
    wins = len(s[s > 0])
    losses = len(s[s < 0])
    evens = len(s[s == 0])
    mean_w = round(s[s > 0].mean(), 3)
    mean_l = round(s[s < 0].mean(), 3)
    win_r = round(wins/losses, 3)
    mean_trd = round(s.mean(), 3)
    sd = round(np.std(s), 3)
    max_l = round(s.min(), 3)
    max_w = round(s.max(), 3)
    sharpe_r = round((s.mean()/np.std(s))*np.sqrt(n), 4)
    cnt = len(s)
    print('Trades:', cnt,
          '\nWins:', wins,
          '\nLosses:', losses,
          '\nBreakeven:', evens,
          '\nWin/Loss Ratio', win_r,
          '\nMean Win:', mean_w,
          '\nMean Loss:', mean_l,
          '\nMean', mean_trd,
          '\nStd Dev:', sd,
          '\nMax Loss:', max_l,
          '\nMax Win:', max_w,
          '\nSharpe Ratio:', sharpe_r)


# ---  M A I N  --- #
# ----------------- #
if __name__ == "__main__":

    # Import data from yahoo api
    start_date = pd.to_datetime('2019-07-01')
    stop_date = pd.to_datetime('2019-07-26')
    msft = pdr.data.get_data_yahoo('MSFT', start_date, stop_date)

    # Calculate daily change of the stock price
    msft['Daily Change'] = pd.Series(msft['Close'] - msft['Open'])

    # Prepare
    deep = 10
    n = 100
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
        data0=msft['Close'][0],
        n=n,
        seed=np.random.randint(0, 1337)
    ) for i in range(deep)]

    # Plot
    fig, axs = plt.subplots(2, figsize=(15, 10))
    axs[0].plot(msft.index, msft['Close'], color='k', label='Closing')
    axs[0].plot(msft.index, msft['Open'], color='r', label='Opening')
    for estimation in estimations:
        axs[0].plot(range(n), estimation)

    axs[0].set_title("MSFT SP", fontsize=20)

    axs[1].plot(msft.index, msft['Daily Change'], color='r')
    axs[1].set_title("MSFT SP Daily Change", fontsize=20)
    axs[1].set_xlabel('Date', fontsize=20)

    axs[0].legend()
    axs[1].legend()
    plt.show()
