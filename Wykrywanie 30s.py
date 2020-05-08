from scipy.io.wavfile import read
from scipy import signal
from scipy.optimize import root
from numpy.random import uniform
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
    return [np.sqrt(np.abs((wx[1] - x[0]) ** 2 - (wy[1] - x[1]) ** 2)) - np.sqrt(np.abs((wx[0] - x[0]) ** 2
            - (wy[0] - x[1]) ** 2)) - d[0], np.sqrt(np.abs((wx[2] - x[0]) ** 2 - (wy[2] - x[1]) ** 2))
            - np.sqrt(np.abs((wx[0] - x[0]) ** 2 - (wy[0] - x[1]) ** 2)) - d[1]]


# Współrzędne mikrofonu
wx = [-0.40,0,0.50]
wy = [1,1,1]

sample_rate, data = read('dlugie.wav')
'''t = np.arange(len(data))
plt.plot(t,data[:,0:1])
plt.show()
plt.plot(t,data[:,2:3])
plt.show()
plt.plot(t,data[:,4:5])
plt.show()'''

for i in range(0,int(len(data)/sample_rate)):
    data1 = data[i*sample_rate : (i+1)*sample_rate, :1]
    data2 = data[i*sample_rate : (i+1)*sample_rate, 2:3]
    data3 = data[i*sample_rate : (i+1)*sample_rate, 4:5]

    d = [lag_finder(data1, data2, data1.shape[0]), lag_finder(data1, data3, data1.shape[0]),
         lag_finder(data2, data3, data1.shape[0])]

    a = []
    b = []
    while len(a) < 10 and len(b) < 10:
        sol = root(fun, np.array([uniform(-1, 1), uniform(-1, 1)]))
        ai, bi = sol.x
        if -5 < ai < 5 and -1 < bi < 1:
            a.append(ai)
            b.append(bi)

    print(a, b)
    aa = np.mean(a)
    bb = np.mean(b)
    print(aa, bb)

    plt.title(i)
    plt.scatter(wx,wy)
    plt.scatter(aa,bb)
    plt.show()
