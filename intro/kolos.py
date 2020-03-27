import numpy as np


def mal(tab):
    count = 0
    for i in range(len(tab)-1):
        if tab[i] < tab[i+1]:
            count += 1

    if count == 0:
        print('Inna')
    else:
        print('Niemalejąca')


x = [1,1,1,2,2,3]
mal(x)
