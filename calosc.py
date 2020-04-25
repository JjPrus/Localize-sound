from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
from sympy import Symbol, nsolve, Rational
import sympy
import mpmath
from random import randrange



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
    return delay/100


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



# get_audio(1024, 6, 44100, 1)
sample_rate1, data = read('Lol_to_dziala2.wav')
data1 = data[:, :1]
data2 = data[:, 3:4]
data3 = data[:, 5:6]
# t = np.arange(0, data1.shape[0], 1)
# plt.figure(0)
# plt.plot(t,data1)
# plt.figure(1)
# plt.plot(t,data2)
# plt.figure(2)
# plt.plot(t,data3)
# plt.show()



# Współrzędne mikrofonu
x = [-0.225,0,0.49]
y = [0,0,0]
d = [lag_finder(data2, data1, data1.shape[0]), lag_finder(data3, data1, data1.shape[0]), lag_finder(data3, data2, data1.shape[0])]
print(d)

mpmath.mp.dps = 5
# Współrzędne głośnika
a = Symbol('a', real=True)
b = Symbol('b', real=True)

def solve_equation(x,y,d):
    # Równanie powiędzy 1 i 2
    f1 = sympy.sqrt(np.abs((x[1]-a)**2-(y[1]-b)**2)) - sympy.sqrt(np.abs((x[0]-a)**2-(y[0]-b)**2)) - d[0]
    # Równanie powiędzy 1 i 3
    f2 = sympy.sqrt(np.abs((x[2]-a)**2-(y[2]-b)**2)) - sympy.sqrt(np.abs((x[0]-a)**2-(y[0]-b)**2)) - d[1]
    # Równanie powiędzy 2 i 3
    f3 = sympy.sqrt(np.abs((x[2]-a)**2-(y[2]-b)**2)) - sympy.sqrt(np.abs((x[1]-a)**2-(y[1]-b)**2)) - d[2]
    x_dz = []
    y_dz = []
    while len(x_dz) < 10:
        pp1 = np.random.uniform(x[0]-5, x[2] + 5)
        pp2 = np.random.uniform(y[0]-5, y[2] + 5)

        try:
            p,q = nsolve((f1,f2,f3), (a,b), (pp1,pp2),verify=False)
            if abs(p) < 10 and (0 < -q < 10):
                x_dz.append(p)
                y_dz.append(q)
        except:
            pass
    print(x_dz)
    print(y_dz)

    return np.median(x_dz), np.median(y_dz)

x_dz, y_dz = solve_equation(x,y,d)
print(x_dz , y_dz)

plt.scatter(x,y)
plt.scatter(x_dz,y_dz)
plt.show()