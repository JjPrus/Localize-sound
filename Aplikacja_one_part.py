from tkinter import *
from PIL import ImageTk, Image
from time import strftime
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy import signal
from scipy.optimize import root
from numpy.random import uniform
import pyaudio
import wave
import pandas as pd
from scipy.signal import butter, lfilter


def fun(x):
    return [np.sqrt(np.abs((wx[1] - x[0]) ** 2 - (wy[1] - x[1]) ** 2)) - np.sqrt(np.abs((wx[0] - x[0]) ** 2
            - (wy[0] - x[1]) ** 2)) - d[0], np.sqrt(np.abs((wx[2] - x[0]) ** 2 - (wy[2] - x[1]) ** 2))
            - np.sqrt(np.abs((wx[0] - x[0]) ** 2 - (wy[0] - x[1]) ** 2)) - d[1]]


def get_audio(chunk, channels, rate, record_time, indeks):
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
                     input_device_index=indeks)

    frames1 = []

    print("Recording")

    for i in range(0, int(rate / chunk * record_time)):
        data1 = stream1.read(chunk)
        frames1.append(data1)

    print("Recording ended")

    stream1.stop_stream()
    stream1.close()
    p.terminate()

    wf = wave.open(wave_output_filename1, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames1))
    wf.close()


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


def live_plotter(x_vec,y1_data,line1,identifier='Mikrofonix',pause_time=0.01):
        if line1==[]:
            # this is the call to matplotlib that allows dynamic plotting
            plt.ion()
            fig = plt.figure(figsize=(13,6))
            ax = fig.add_subplot(111)
            # create a variable for the line so we can later update it
            line1, = ax.plot(x_vec,y1_data,'bo',alpha=0.8)       
            #update plot label/title
            plt.ylabel('Y')
            plt.xlabel('X')
            plt.title('Title: {}'.format(identifier))
            plt.show()
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line1.set_ydata(y1_data)
        line1.set_xdata(x_vec)
        # adjust limits if new data goes beyond bounds
        if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
            plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
        plt.pause(pause_time)
        
        # return line so we can update it again in the next iteration
        return line1


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def dalej():
    
    for i in range(len(nazwy)):
        if save_this.get() == nazwy[i]:
            global toto
            toto = i
            print(toto)

    wx = [float(x_jeden.get()), float(x_dwa.get()), float(x_trzy.get())]
    wy = [float(y_jeden.get()), float(y_dwa.get()), float(y_trzy.get())]

    print(wx)
    print(wy)   
    global d
    line1 = []
    x_val = [wx[0],wx[1],wx[2],0.0]
    y_val = [wy[0],wy[1],wy[2],0.0]

    while True:
        get_audio(1024, 6, 44100, 1.5, toto)
        sample_rate, data = read("ZPI.wav")

        data1 = data[:, :1]
        data2 = data[:, 2:3]
        data3 = data[:, 4:5]
        
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

        # fs = 5000.0
        # lowcut = 100.0
        # highcut = 2000.0

        # t = np.linspace(0, data1.shape[0], 88045, endpoint=False)
        # # ta duza liczba to ilosc jednostek w calym nagraniu. czyli jest 44100 * dlugosc nagrania
        # f0 = 600.0
        # plt.figure(2)
        # plt.clf()
        # plt.plot(t, data1, label='Noisy signal')

        # data1 = butter_bandpass_filter(data1, lowcut, highcut, fs, order=6) 
        # plt.plot(t, data1, label='Filtered signal (%g Hz)' % f0)
        # plt.xlabel('time (seconds)')
        # plt.axis('tight')
        # plt.legend(loc='upper left')

        # plt.show()

        # lowcut = 75.0
        # highcut = 2000.0

        # data2 = butter_bandpass_filter(data2, lowcut, highcut, fs, order=6)

        # lowcut = 50.0
        # highcut = 2000.0

        # data3 = butter_bandpass_filter(data3, lowcut, highcut, fs, order=6)
        
        d = [lag_finder(data1[34000:], data2[34000:], data1[34000:].shape[0]) * 0.3403, lag_finder(data1[34000:], data3[34000:], data1[34000:].shape[0]) * 0.3403,
            lag_finder(data2[34000:], data3[34000:], data1[34000:].shape[0]) * 0.3403]

        print(d)


        # A = np.array([[wx[1] - wx[0], wy[1] - wy[0], d[0]],
        #       [wx[2] - wx[0], wy[2] - wy[0], d[1]]])
        # b1 = 0.5 * ((wx[1] - wx[0]) ** 2 + (wy[1] - wy[0]) ** 2 - d[0] ** 2)
        # b2 = 0.5 * ((wx[2] - wx[0]) ** 2 + (wy[2] - wy[0]) ** 2 - d[1] ** 2)
        # b = np.array([b1, b2]).T

        A = np.array([[wx[0] - wx[1], wy[0] - wy[1], d[0]],
                        [wx[0] - wx[2], wy[0] - wy[2], d[1]]])
        b1 = 0.5 * (wx[0] ** 2 - wx[1] ** 2 + wy[0] ** 2 - wy[1] ** 2 + d[0] ** 2)
        b2 = 0.5 * (wx[0] ** 2 - wx[2] ** 2 + wy[0] ** 2 - wy[2] ** 2 + d[1] ** 2)
        b = np.array([b1, b2]).T
        # x = A.T @ np.linalg.inv(A @ A.T) @ b
        try:
            x = np.linalg.inv(A.T @ A) @ A.T @ b
        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                x = A.T @ np.linalg.inv(A @ A.T) @ b
                print('dupa')
        x_val[-1] = x[0]
        y_val[-1] = x[1]
        print(x_val)
        print(y_val)
        line1 = live_plotter(x_val,y_val,line1)


global slownik, nazwy, indexy, wx, wy, data

slownik = {}
nazwy = []
indexy = []
wx = []
wy = []

# pobieranie danych o urządzeniach audio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    slownik['name{}'.format(i)] = p.get_device_info_by_index(i)['name']
    slownik['index{}'.format(i)] = p.get_device_info_by_index(i)['index']
    nazwy.append(slownik['name{}'.format(i)])
    indexy.append(slownik['index{}'.format(i)])
print("nazwy: {}".format(nazwy))
print("indexy: {}".format(indexy))

rootXD = Tk()
rootXD.title("coś")
rootXD.geometry("400x600")

nazwa = Label(rootXD, text = "Mikrofonix 3000", font = ("Comic Sans MS", 44), padx = 15, pady = 15)
nazwa.pack(anchor = "center")

global save_this, save_this1, save_this2

save_this = StringVar()
save_this.set("wybierz urządzenie")

drop = OptionMenu(rootXD, save_this, *nazwy)
drop.pack(anchor = "center")

mikrofon_jeden_x = Label(rootXD, text = "mikrofon jeden - x", font = ("Comic Sans MS", 14), padx = 15, pady = 5)
mikrofon_jeden_x.pack(anchor = 'center')

x_jeden = Entry(rootXD)
x_jeden.pack(anchor = "center")

mikrofon_jeden_y = Label(rootXD, text = "mikrofon jeden - y", font = ("Comic Sans MS", 14), padx = 15, pady = 5)
mikrofon_jeden_y.pack(anchor = 'center')

y_jeden = Entry(rootXD)
y_jeden.pack(anchor = "center")

mikrofon_dwa_x = Label(rootXD, text = "mikrofon dwa - x", font = ("Comic Sans MS", 14), padx = 15, pady = 5)
mikrofon_dwa_x.pack(anchor = 'center')

x_dwa = Entry(rootXD)
x_dwa.pack(anchor = "center")

mikrofon_dwa_y = Label(rootXD, text = "mikrofon dwa - y", font = ("Comic Sans MS", 14), padx = 15, pady = 5)
mikrofon_dwa_y.pack(anchor = 'center')

y_dwa = Entry(rootXD)
y_dwa.pack(anchor = "center")

mikrofon_trzy_x = Label(rootXD, text = "mikrofon trzy - x", font = ("Comic Sans MS", 14), padx = 15, pady = 5)
mikrofon_trzy_x.pack(anchor = 'center')

x_trzy = Entry(rootXD)
x_trzy.pack(anchor = "center")

mikrofon_trzy_y = Label(rootXD, text = "mikrofon trzy - y", font = ("Comic Sans MS", 14), padx = 15, pady = 5)
mikrofon_trzy_y.pack(anchor = 'center')

y_trzy = Entry(rootXD)
y_trzy.pack(anchor = "center")

przycisk = Button(rootXD, text = "dalej", command = dalej)
przycisk.pack(anchor = "center")

rootXD.mainloop()