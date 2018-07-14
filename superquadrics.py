"""
This file generates superquadrics.
Ref1: https://cse.buffalo.edu/~jryde/cse673/files/superquadrics.pdf
Ref2: https://en.wikipedia.org/wiki/Superquadrics
Author: Huayi Zeng
"""

import numpy as np

def save_obj(path_save, x, y, z):
    with open(path_save, "w+") as fout:
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                fout.write("v %.3f %.3f %.3f\n" % (x[i, j], y[i, j], z[i, j]))

def sgn(x):
    y = np.ones(x.shape)
    y[x == 0] = 0
    y[x < 0] *= -1
    return y

def f(w, m):
    return sgn(np.sin(w)) * np.power(np.abs(np.sin(w)), m)

def g(w, m):
    return sgn(np.cos(w)) * np.power(np.abs(np.cos(w)), m)

def superquadric(epsilon, a, n):
    """
    We follow https://en.wikipedia.org/wiki/Superquadrics,
    a is a 3-element vector: A, B, C
    epsilon is a 3-element vector: 2/r, 2/s, 2/t
    """
    etamax = np.pi / 2
    etamin = -np.pi / 2
    wmax = np.pi
    wmin = -np.pi
    deta = (etamax - etamin) / n
    dw = (wmax - wmin) / n
    x = np.linspace(0, n, n)
    y = np.linspace(0, n, n)
    xv, yv = np.meshgrid(x, y)
    eta = etamin + xv * deta
    w = wmin + yv * dw
    x = a[0] * g(eta, epsilon[0]) * g(w, epsilon[0])
    y = a[1] * g(eta, epsilon[1]) * f(w, epsilon[1])
    z = a[2] * f(eta, epsilon[2])
    return x, y, z

if __name__ == '__main__':
    a = [1, 1, 1]
    r = 2
    s = 2
    t = 2
    epsilon = [2/r, 2/s, 2/t]
    x, y, z = superquadric(epsilon, a, n = 20)
    path_save = "temp.obj"
    save_obj(path_save, x, y, z)
