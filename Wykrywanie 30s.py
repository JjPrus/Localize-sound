from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave


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


def gcc_phat(y1, y2, interp=16):
    n = y1.shape[0] + y2.shape[0]
    xi = np.fft.rfft(y1, n)
    xj = np.fft.rfft(y2, n)

    G = xi * np.conj(xj)
    R = np.fft.irfft(G / np.abs(G), interp * n)

    max_shift = int(interp * n / 2)
    corr = np.concatenate((R[-max_shift:], R[:max_shift+1]))
    shift = np.argmax(corr) - max_shift
    return shift


def get_audio(chunk, channels, rate, record_time):
    """Nagrywa dźwięk z mikrofonu
    chunk - na ile próbek dzielimy sygnał
    channels - liczba kanałów (stereo - 2)
    rate - próbkowanie w Hz
    record_time - czas nagrania"""

    format = pyaudio.paInt16
    wave_output_filename1 = "ZPI.wav"
    p = pyaudio.PyAudio()

    stream1 = p.open(format=format,
                     channels=channels,
                     rate=rate,
                     input=True,
                     frames_per_buffer=chunk,
                     input_device_index=1)

    frames1 = []

    for i in range(0, int(rate / chunk * record_time)):
        data1 = stream1.read(chunk)
        frames1.append(data1)


    stream1.stop_stream()
    stream1.close()
    p.terminate()

    wf = wave.open(wave_output_filename1, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames1))
    wf.close()


def fun(x):
    f1 = np.sqrt(np.abs((wx[1] - x[0]) ** 2 - (wy[1] - x[1]) ** 2)) - np.sqrt(np.abs((wx[0] - x[0]) ** 2
                                                                                     - (wy[0] - x[1]) ** 2)) - d[0]
    f2 = np.sqrt(np.abs((wx[2] - x[0]) ** 2 - (wy[2] - x[1]) ** 2)) - np.sqrt(np.abs((wx[0] - x[0]) ** 2 -
                                                                                     (wy[0] - x[1]) ** 2)) - d[1]
    return [f1, f2]


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

    d = [lag_finder(data1, data2, data1.shape[0]) * 0.3403, lag_finder(data1, data3, data1.shape[0]) * 0.3403,
         lag_finder(data2, data3, data2.shape[0]) * 0.3403]
    # d2 = [gcc_phat(data1, data2) * 0.3403, gcc_phat(data1, data3) * 0.3403]
    print("dupa")
    # print(i, d2)
    print("dupa2")

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
