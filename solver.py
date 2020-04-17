from sympy import Symbol, nsolve
import sympy
import mpmath
from sympy import Rational
import numpy as np


# Współrzędne mikrofonu
x = [2,2.35,2.90]
y = [1,1,1]
d = [0.21,-0.1]

mpmath.mp.dps = 5
# Współrzędne głośnika
a = Symbol('a', real=True)
b = Symbol('b', real=True)
# Równanie powiędzy 1 i 2
# f1 = sympy.sqrt((x[1]-a)**2-(y[1]-b)**2) - sympy.sqrt((x[0]-a)**2-(y[0]-b)**2) - d[0]
# Równanie powiędzy 1 i 3
f2 = sympy.sqrt(np.abs((x[2]-a)**2-(y[2]-b)**2)) - sympy.sqrt(np.abs((x[0]-a)**2-(y[0]-b)**2)) - d[0]
# Równanie powiędzy 2 i 3
f3 = sympy.sqrt(np.abs((x[2]-a)**2-(y[2]-b)**2)) - sympy.sqrt(np.abs((x[1]-a)**2-(y[1]-b)**2)) - d[1]

print(nsolve((f3,f2), (a,b), (1.3,1.4),verify=False))
# print(nsolve((f3,f2), (a,b), (1,1)))