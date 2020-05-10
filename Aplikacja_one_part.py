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
from Wykrywanie_30s import lag_finder, fun ,get_audio

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


root = Tk()
root.title("coś")
root.geometry("400x600")

global save_this, save_this1, save_this2

save_this = StringVar()
save_this.set("wybierz mikrofon jeden")

# save_this1 = StringVar()
# save_this1.set("wybierz mikrofon dwa")

# save_this2 = StringVar()
# save_this2.set("wybierz mikrofon trzy")

drop = OptionMenu(root, save_this, *nazwy)
drop.pack(anchor = "center")

# drop1 = OptionMenu(root, save_this1, *nazwy)
# drop1.pack(anchor = "center")

# drop2 = OptionMenu(root, save_this2, *nazwy)
# drop2.pack(anchor = "center")

x_jeden = Entry(root)
x_jeden.pack(anchor = "center")

y_jeden = Entry(root)
y_jeden.pack(anchor = "center")

x_dwa = Entry(root)
x_dwa.pack(anchor = "center")

y_dwa = Entry(root)
y_dwa.pack(anchor = "center")

x_trzy = Entry(root)
x_trzy.pack(anchor = "center")

y_trzy = Entry(root)
y_trzy.pack(anchor = "center")

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
    
    get_audio(1024, 6, 44100, 1, toto)
    sample_rate, data = read("ZPI.wav")

    data1 = data[:, :1]
    data2 = data[:, 2:3]
    data3 = data[:, 4:5]
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

    dalej()

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

przycisk = Button(root, text = "dalej", command = dalej)
przycisk.pack(anchor = "center")

# przycisk2 = Button(root, text = "graf test", command = graph)
# przycisk2.pack(anchor = S)

root.mainloop()








                    #exit button
# root = Tk()

# img = ImageTk.PhotoImage(Image.open('ZPI1.png'))
# lol = Label(image = img)
# lol.pack()

# def enter():
#     root1 = Tk()
#     button_quit = Button(root1, text = "exit", command = root1.quit)
#     button_quit.pack()
#     root1.mainloop()


# button_enter = Button(root, text = "enter", command = enter)
# button_enter.pack()


# root.mainloop()







# root = Tk()
# root.title("Kalkulator")

# box = Entry(root, width = 35, borderwidth = 5)
# box.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

# def button_click(number):
#     current = box.get()
#     box.delete(0, END)
#     box.insert(0, str(current) + str(number))

# def button_clear():
#     box.delete(0, END)

# def button_add():
#     add_number = box.get()
#     global add
#     global math
#     math = "addition"
#     add = float(add_number)
#     box.delete(0, END) 

# def button_subtrack():
#     sub_number = box.get()
#     global sub
#     global math
#     math = "subtraction"
#     sub = float(sub_number)
#     box.delete(0, END)

# def button_divide():
#     div_number = box.get()
#     global div
#     global math
#     math = "division"
#     div = float(div_number)
#     box.delete(0, END)

# def button_multiply():
#     mul_number = box.get()
#     global mul
#     global math
#     math = "multiplication"
#     mul = float(mul_number)
#     box.delete(0, END)

# def button_equal():
#     if math == "addition":
#         second_number = box.get()
#         equal = add + float(second_number)
#         box.delete(0, END)
#         box.insert(0, equal)
#     elif math == "subtraction":
#         second_number = box.get()
#         equal = sub - float(second_number)
#         box.delete(0, END)
#         box.insert(0, equal)
#     elif math == "division":
#         second_number = box.get()
#         equal = div / float(second_number)
#         box.delete(0, END)
#         box.insert(0, equal)
#     elif math == "multiplication":
#         second_number = box.get()
#         equal = mul * float(second_number)
#         box.delete(0, END)
#         box.insert(0, equal)

# b1 = Button(root, text = "1", padx = 40, pady = 20, command = lambda: button_click(1))
# b1.grid(row = 3, column = 0)
# b2 = Button(root, text = "2", padx = 40, pady = 20, command = lambda: button_click(2))
# b2.grid(row = 3, column = 1)
# b3 = Button(root, text = "3", padx = 41, pady = 20, command = lambda: button_click(3))
# b3.grid(row = 3, column = 2)

# b4 = Button(root, text = "4", padx = 40, pady = 20, command = lambda: button_click(4))
# b4.grid(row = 2, column = 0)
# b5 = Button(root, text = "5", padx = 40, pady = 20, command = lambda: button_click(5))
# b5.grid(row = 2, column = 1)
# b6 = Button(root, text = "6", padx = 41, pady = 20, command = lambda: button_click(6))
# b6.grid(row = 2, column = 2)

# b7 = Button(root, text = "7", padx = 40, pady = 20, command = lambda: button_click(7))
# b7.grid(row = 1, column = 0)
# b8 = Button(root, text = "8", padx = 40, pady = 20, command = lambda: button_click(8))
# b8.grid(row = 1, column = 1)
# b9 = Button(root, text = "9", padx = 41, pady = 20, command = lambda: button_click(9))
# b9.grid(row = 1, column = 2)

# b0 = Button(root, text = "0", padx = 40, pady = 20, command = lambda: button_click(0))
# b0.grid(row = 4, column = 0)
# bclear = Button(root, text = "Clear", padx = 88, pady = 20, command = button_clear)
# bclear.grid(row = 4, column = 1, columnspan = 2)

# badd = Button(root, text = "+", padx = 40, pady = 20, command = button_add)
# badd.grid(row = 5, column = 0)
# bsum = Button(root, text = "=", padx = 99, pady = 20, command = lambda: button_equal())
# bsum.grid(row = 5, column = 1, columnspan = 2)

# bsub = Button(root, text = "-", padx = 41, pady = 20, command = button_subtrack)
# bsub.grid(row = 6, column = 0)
# bdiv = Button(root, text = "/", padx = 42, pady = 20, command = button_divide)
# bdiv.grid(row = 6, column = 1)
# bmul = Button(root, text = "*", padx = 42, pady = 20, command = button_multiply)
# bmul.grid(row = 6, column = 2)

# root.mainloop()
