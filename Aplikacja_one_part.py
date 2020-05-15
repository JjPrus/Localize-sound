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

    wx = [x_jeden.get(), x_dwa.get(), x_trzy.get()]
    wy = [y_jeden.get(), y_dwa.get(), y_trzy.get()]

    print(wx)
    print(wy)
    
    get_audio(1024, 6, 44100, 3, toto)
    sample_rate, data = read("ZPI.wav")

    data1 = data[:, :1]
    data2 = data[:, 2:3]
    data3 = data[:, 4:5]
    
    global d
    d = [lag_finder(data1, data2, data1.shape[0]), lag_finder(data1, data3, data1.shape[0]),
        lag_finder(data2, data3, data1.shape[0])]
    
    print(d)

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

    dalej()

global slownik, nazwy, indexy, wx, wy, data

slownik = {}
nazwy = []
indexy = []
wx = []
wy = []

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

# def graph():

#     plt.ioff()
#     for i in range(0, 30):
#         prices = np.random.normal(200000, 25000, 5000)
#         name = 'fig' +str(i)+'.png'
#         plt.savefig(name)
#         time.sleep(1)
#         plt.close(fig)
        
        # plt.figure(1)
        # plt.hist(prices, 50)
        # plt.show()
        # time.sleep(1)
        # plt.close('all')
    # graph()

przycisk = Button(rootXD, text = "dalej", command = dalej)
przycisk.pack(anchor = "center")

# przycisk2 = Button(root, text = "graf test", command = graph)
# przycisk2.pack(anchor = S)

rootXD.mainloop()
