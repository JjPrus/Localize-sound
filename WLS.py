import numpy as np

a = [-0.40, 0, 0.50]
b = [0.75, 1, 1.25]
r = [0.00252, 0.01318, 0.00715]  # |r21|, |r31|

A = np.array([[a[1] - a[0], b[1] - b[0], r[0]],
              [a[2] - a[0], b[2] - b[0], r[1]]])
th1 = 0.5 * ((a[1] - a[0]) ** 2 + (b[1] - b[0]) ** 2 - r[0] ** 2)
th2 = 0.5 * ((a[2] - a[0]) ** 2 + (b[2] - b[0]) ** 2 - r[1] ** 2)
Theta = np.array([th1, th2]).T
