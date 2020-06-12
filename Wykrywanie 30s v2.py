from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def lag_finder(y1, y2, sr):
    """Zwraca różnicę w przybyciu sygnału do mikrofonów w sekundach
    y1 - sygnał z pierwszego mikrofonu
    y2 - sygnał z drugiego mikrofonu
    sr - ilość próbek"""

    n = len(y1)
    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)]
                                                           * signal.correlate(y2, y2, mode='same')[int(n/2)])

    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    return delay


# Współrzędne mikrofonu
wx = [-0.40, 0, 0.50]
wy = [1, 1, 1]

sample_rate, data = read('dlugie.wav')
'''t = np.arange(len(data))
plt.plot(t,data[:,0:2])
plt.show()
plt.plot(t,data[:,2:4])
plt.show()
plt.plot(t,data[:,4:6])
plt.show()'''

step = np.arange(3.0, int(len(data) / sample_rate), 0.25)
for i in step:
    data1 = data[int(i*sample_rate) : int((i+0.25)*sample_rate), :1]
    data2 = data[int(i*sample_rate) : int((i+0.25)*sample_rate), 2:3]
    data3 = data[int(i*sample_rate) : int((i+0.25)*sample_rate), 4:5]

    ts1 = np.concatenate(data1)
    ts2 = np.concatenate(data2)
    ts3 = np.concatenate(data3)

    smooth1 = pd.Series(ts1).rolling(window=20).mean()
    smooth2 = pd.Series(ts2).rolling(window=20).mean()
    smooth3 = pd.Series(ts3).rolling(window=20).mean()

    data1 = np.array(smooth1).reshape((data1.shape[0], 1))
    data2 = np.array(smooth2).reshape((data2.shape[0], 1))
    data3 = np.array(smooth3).reshape((data3.shape[0], 1))

    data1 = data1[np.logical_not(np.isnan(data1))]
    data2 = data2[np.logical_not(np.isnan(data2))]
    data3 = data3[np.logical_not(np.isnan(data3))]
    plt.plot(data1)
    plt.show()
    plt.plot(data2)
    plt.show()
    plt.plot(data3)
    plt.show()

    d = [lag_finder(data1, data2, data1.shape[0]) * 0.3, lag_finder(data1, data3, data1.shape[0]) * 0.3,
         lag_finder(data2, data3, data2.shape[0]) * 0.3]

    A = np.array([[wx[0] - wx[1], wy[0] - wy[1], d[0]],
                  [wx[0] - wx[2], wy[0] - wy[2], d[1]]])
    b1 = 0.5 * (wx[0] ** 2 - wx[1] ** 2 + wy[0] ** 2 - wy[1] ** 2 + d[0] ** 2)
    b2 = 0.5 * (wx[0] ** 2 - wx[2] ** 2 + wy[0] ** 2 - wy[2] ** 2 + d[1] ** 2)
    b = np.array([b1, b2]).T
    x = A.T @ np.linalg.inv(A @ A.T) @ b
    # print(i, x[0], d)

    plt.title(i)
    plt.scatter(wx, wy)
    plt.scatter(x[0], x[1])
    plt.show()
