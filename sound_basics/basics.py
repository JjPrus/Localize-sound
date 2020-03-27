from scipy import fftpack, signal, io
import matplotlib.pyplot as plt
import numpy as np


def próbkowany_sygnał(t):
    return (2 * np.sin(2 * np.pi * t) + 3 * np.sin(22 * 2 * np.pi * t) + 2 * np.random.randn(*np.shape(t)))


B = 30.0
f_s = 2 * B
delta_f = 0.01
N = int(f_s / delta_f)
T = N / f_s

t = np.linspace(0, T, N)
f_t = próbkowany_sygnał(t)

fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
axes[0].plot(t, f_t)
axes[0].set_xlabel("czas (s)")
axes[0].set_ylabel("sygnał")
axes[1].plot(t, f_t)
axes[1].set_xlim(0, 5)
axes[1].set_xlabel("czas (s)")

plt.show()

F = fftpack.fft(f_t)
f = fftpack.fftfreq(N, 1.0/f_s)
maska = np.where(f >= 0)

fig, axes = plt.subplots(3, 1, figsize=(8, 6))
axes[0].plot(f[maska], np.log(abs(F[maska])), label="real")
axes[0].plot(B, 0, 'r*', markersize=10)
axes[0].set_ylabel("$\log(|F|)$", fontsize=14)
axes[1].plot(f[maska], abs(F[maska])/N, label="real")
axes[1].set_xlim(0, 2)
axes[1].set_ylabel("$|F|/N$", fontsize=14)
axes[2].plot(f[maska], abs(F[maska])/N, label="real")
axes[2].set_xlim(0, 30)
axes[2].set_xlabel("freq. (Hz)", fontsize=14)
axes[2].set_ylabel("$|F|/N$", fontsize=14)
plt.show()
