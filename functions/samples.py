from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


def lag_finder(y1, y2, sr):
    n = len(y1)

    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)]
                                                           * signal.correlate(y2, y2, mode='same')[int(n/2)])

    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    return abs(delay) / 100


sample_rate1, data1 = read("Inglot_4_35_1_20.wav")
sample_rate2, data2 = read("Inglot_4_35_2_20.wav")
data1 = data1.reshape((data1.shape[0], 1))[40000:100000]
data2 = data2.reshape((data2.shape[0], 1))[43500:103500]
lag = lag_finder(data1, data2, data1.shape[0])

delta_d1 = 343 * lag

print('Próbkowanie: {} Hz'.format(sample_rate1))
print('Czas nagrania: {} s'.format(data1.shape[0] / sample_rate1))
print('Lag: {}'.format(lag))
print('Delta_d: {}'.format(delta_d1))

t = np.arange(0, data1.shape[0], 1)
fig, axes = plt.subplots(2, 1, figsize=(20, 6))
axes[0].plot(t, data1)
axes[1].plot(t, data2)
axes[0].set_ylabel("Sygnal 1", fontsize=14)
axes[1].set_ylabel("Sygnal 2", fontsize=14)
plt.show()
