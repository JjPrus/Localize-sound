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
            plt.ylabel('Y Label')
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

def dalej():
    
    for i in range(len(nazwy)):
        if save_this.get() == nazwy[i]:
            global toto
            toto = i
            print(toto)
        # if save_this1.get() == nazwy[i]:
        #     global toto1
        #     toto1 = i
        #     print(toto1)
        # if save_this2.get() == nazwy[i]:
        #     global toto2
        #     toto2 = i
        #     print(toto2)

    wx = [float(x_jeden.get()), float(x_dwa.get()), float(x_trzy.get())]
    wy = [float(y_jeden.get()), float(y_dwa.get()), float(y_trzy.get())]

    print(wx)
    print(wy)   
    global d
    line1 = []
    x_val = [wx[0],wx[1],wx[2],0.0]
    y_val = [wy[0],wy[1],wy[2],0.0]

    while True:
        get_audio(1024, 6, 44100, 1, toto)
        sample_rate, data = read("ZPI.wav")

        data1 = data[:, :1]
        data2 = data[:, 2:3]
        data3 = data[:, 4:5]
        # plt.figure(0)
        # plt.plot(data1[34000:])
        # plt.figure(1)
        # plt.plot(data2[34000:])
        # plt.figure(2)
        # plt.plot(data3[34000:])        
        # plt.show()
        # print(data1[34000:].shape)
        d = [lag_finder(data1[34000:], data2[34000:], data1[34000:].shape[0]) * 0.3403, lag_finder(data1[34000:], data3[34000:], data1[34000:].shape[0]) * 0.3403,
            lag_finder(data2[34000:], data3[34000:], data1[34000:].shape[0]) * 0.3403]

        print(d)

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
        x_val[-1] = x[0]
        y_val[-1] = x[1]
        print(x_val)
        print(y_val)
        line1 = live_plotter(x_val,y_val,line1)

def graph():

    def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
        if line1==[]:
            # this is the call to matplotlib that allows dynamic plotting
            plt.ion()
            fig = plt.figure(figsize=(13,6))
            ax = fig.add_subplot(111)
            # create a variable for the line so we can later update it
            line1, = ax.plot(x_vec,y1_data,'bo',alpha=0.8)       
            #update plot label/title
            plt.ylabel('Y Label')
            plt.title('Title: {}'.format(identifier))
            plt.show()
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line1.set_ydata(y1_data)
        # adjust limits if new data goes beyond bounds
        if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
            plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
        plt.pause(pause_time)
        
        # return line so we can update it again in the next iteration
        return line1

    size = 100
    x_vec = np.linspace(0,1,size+1)[0:-1]
    y_vec = np.random.randn(len(x_vec))
    line1 = []

    while True:
        rand_val = np.random.randn(1)
        y_vec[-1] = rand_val
        line1 = live_plotter(x_vec[-4:-1],y_vec[-4:-1],line1)
        y_vec = np.append(y_vec[1:],0.0)

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

nazwa = Label(rootXD, text = "Mikrfonix 3000", font = ("Comic Sans MS", 44), padx = 15, pady = 15)
nazwa.pack(anchor = "center")

global save_this, save_this1, save_this2

save_this = StringVar()
save_this.set("wybierz mikrofon jeden")

# save_this1 = StringVar()
# save_this1.set("wybierz mikrofon dwa")

# save_this2 = StringVar()
# save_this2.set("wybierz mikrofon trzy")

drop = OptionMenu(rootXD, save_this, *nazwy)
drop.pack(anchor = "center")

# drop1 = OptionMenu(root, save_this1, *nazwy)
# drop1.pack(anchor = "center")

# drop2 = OptionMenu(root, save_this2, *nazwy)
# drop2.pack(anchor = "center")

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

#     # root2 = Tk()
    
#     # def time():
#     #     string = strftime('%S')
#     #     czas.config(text = string)
#     #     czas.after(1000, time)

#     # czas = Label(root2)
#     # czas.pack(anchor = "center")
#     # time()
    
#     # root2.mainloop()
#     return

przycisk = Button(rootXD, text = "dalej", command = dalej)
przycisk.pack(anchor = "center")

przycisk2 = Button(rootXD, text = "graf test", command = graph)
przycisk2.pack(anchor = S)

rootXD.mainloop()