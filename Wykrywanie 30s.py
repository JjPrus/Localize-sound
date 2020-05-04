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


def solve_equation(x,y,d):
    # Równanie powiędzy 1 i 2
    f1 = sympy.sqrt(np.abs((x[1]-a)**2-(y[1]-b)**2)) - sympy.sqrt(np.abs((x[0]-a)**2-(y[0]-b)**2)) - d[0]
    # Równanie powiędzy 1 i 3
    f2 = sympy.sqrt(np.abs((x[2]-a)**2-(y[2]-b)**2)) - sympy.sqrt(np.abs((x[0]-a)**2-(y[0]-b)**2)) - d[1]
    # Równanie powiędzy 2 i 3
    f3 = sympy.sqrt(np.abs((x[2]-a)**2-(y[2]-b)**2)) - sympy.sqrt(np.abs((x[1]-a)**2-(y[1]-b)**2)) - d[2]
    x_dz = []
    y_dz = []
    while len(x_dz) < 3:
        pp1 = np.random.uniform(x[0]-5, x[2] + 5)
        pp2 = np.random.uniform(y[0]-5, y[2] + 5)

        try:
            p,q = nsolve((f1,f2,f3), (a,b), (pp1,pp2),verify=False)
            if abs(p) < 10 and (0 < q < 10):
                x_dz.append(p)
                y_dz.append(q)
        except:
            pass
    # print(x_dz)
    # print(y_dz)

    return np.median(x_dz), np.median(y_dz)




mpmath.mp.dps = 8
# Współrzędne mikrofonu
x = [-0.30,0,0.55]
y = [0,0,0]

# Współrzędne głośnika
a = Symbol('a', real=True)
b = Symbol('b', real=True)



sample_rate, data = read('dlugie.wav')
t = np.arange(len(data))
plt.plot(t,data[:,0:1])
plt.show()
plt.plot(t,data[:,2:3])
plt.show()
plt.plot(t,data[:,4:5])
plt.show()

for i in range(0,int(len(data)/sample_rate)):
    data1 = data[i*sample_rate : (i+1)*sample_rate, :1]
    data2 = data[i*sample_rate : (i+1)*sample_rate, 2:3]
    data3 = data[i*sample_rate : (i+1)*sample_rate, 4:5]

    d = [lag_finder(data1, data2, data1.shape[0]), lag_finder(data1, data3, data1.shape[0]), lag_finder(data2, data3, data1.shape[0])]
    # print(d)

    x_dz, y_dz = solve_equation(x,y,d)
    # print(i, x_dz , y_dz)
    # plt.xlim(-0.5,0.7)
    # plt.ylim(-0.1,0.7)
    plt.title(i)
    plt.scatter(x,y)
    plt.scatter(x_dz,y_dz)
    plt.show()