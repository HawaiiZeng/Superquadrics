"""
This file generates superquadrics.
Ref1: https://cse.buffalo.edu/~jryde/cse673/files/superquadrics.pdf
Ref2: https://en.wikipedia.org/wiki/Superquadrics
Author: Huayi Zeng
"""

import numpy as np

def save_pts(path_save, x, y, z):
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    pts = np.zeros((x.shape[0], 3))
    pts[:, 0], pts[:, 1], pts[:, 2] = x, y, z
    np.savetxt(path_save, pts, fmt='%1.3f')

def save_obj(path_save, x, y, z, threshold = -1):
    hei, wid = x.shape[0], x.shape[1]
    with open(path_save, "w+") as fout:
        for i in range(hei):
            for j in range(wid):
                if threshold > 0:
                    if np.abs(x[i, j]) > threshold or np.abs(y[i, j]) > threshold or np.abs(z[i, j]) > threshold:
                        continue
                    fout.write("v %.3f %.3f %.3f\n" % (x[i, j], y[i, j], z[i, j]))
                else:
                    fout.write("v %.3f %.3f %.3f\n" % (x[i, j], y[i, j], z[i, j]))
        # Write face: we could not write face when we filter out vertices by threshold
        if threshold < 0:
            for i in range(hei - 1):
                for j in range(wid - 1):
                    fout.write("f %d %d %d\n" % ((i + 1) * wid + j + 1, i * wid + j + 1 + 1, i * wid + j + 1))
                    fout.write("f %d %d %d\n" % ((i + 1) * wid + j + 1 + 1, i * wid + j + 1 + 1, (i + 1) * wid + j + 1))
                
def sgn(x):
    y = np.ones(x.shape)
    y[x == 0] = 0
    y[x < 0] *= -1
    return y

def signed_sin(w, m):
    return sgn(np.sin(w)) * np.power(np.abs(np.sin(w)), m)

def signed_cos(w, m):
    return sgn(np.cos(w)) * np.power(np.abs(np.cos(w)), m)

def signed_tan(w, m):
    return sgn(np.tan(w)) * np.power(np.abs(np.tan(w)), m)

def signed_sec(w, m):
    return sgn(np.cos(w)) * np.power(np.abs(1 / np.cos(w)), m)

def get_eta_and_w(n, etamax = np.pi / 2, wmax = np.pi):
    etamin = -etamax
    wmin = -wmax
    deta = (etamax - etamin) / n
    dw = (wmax - wmin) / n
    # When the range = 2PI, one point will be overlapped
    y = np.linspace(0, n, n + 1)
    x = np.linspace(0, n, n + 1)

    yv, xv = np.meshgrid(y, x)
    eta = etamin + yv * deta
    w = wmin + xv * dw
    return eta, w

def superellipsoid(epsilon, a, n):
    """
    We follow https://en.wikipedia.org/wiki/Superquadrics, (code there should be superellipsoid)
    a is a 3-element vector: A, B, C
    epsilon is a 3-element vector: 2/r, 2/s, 2/t
    NOTE(Huayi): different from superellipsoid_taperingz_blendingx. and superquadrics.pdf EQ 2.10
    """
    eta, w = get_eta_and_w(n)
    x = a[0] * signed_cos(eta, epsilon[0]) * signed_cos(w, epsilon[0])
    y = a[1] * signed_cos(eta, epsilon[1]) * signed_sin(w, epsilon[1])
    z = a[2] * signed_sin(eta, epsilon[2])
    return x, y, z

def superhyperboloid_one_piece(epsilon, a, n):
    """
    https://cse.buffalo.edu/~jryde/cse673/files/superquadrics.pdf EQ 2.20
    """
    eta, w = get_eta_and_w(n)
    x = a[0] * signed_sec(eta, epsilon[0]) * signed_cos(w, epsilon[0])
    y = a[1] * signed_sec(eta, epsilon[1]) * signed_sin(w, epsilon[1])
    z = a[2] * signed_tan(eta, epsilon[2])
    return x, y, z

def supertoroids(epsilon, a, n):
    """
    https://cse.buffalo.edu/~jryde/cse673/files/superquadrics.pdf EQ 2.22
    """
    eta, w = get_eta_and_w(n, etamax = np.pi, wmax = np.pi)
    x = a[0] * (a[3] + signed_cos(eta, epsilon[0])) * signed_cos(w, epsilon[1])
    y = a[1] * (a[3] + signed_cos(eta, epsilon[0])) * signed_sin(w, epsilon[1])
    z = a[2] * signed_sin(eta, epsilon[0])
    return x, y, z

def superellipsoid_taperingz_blendingx(epsilon, a, a0, t, b, n):
    """
    superellipsoid with tapering freedom on z axis, and blending freedom on x axis
    Ref: Shape and nonrigid motion estimation through physics-based synthesis
    epsilon:2d, a:3d, a0:1d, t:2d, b:3d
    tapering: -1 <= t <= 1 (tapering params in x and y)
    bending: -1 <= b[1] <= 1, 0 <= b[2] <= 1 (b[0]: magnitude; b[1]: location on z axis where bending is applied,
                                              b[2]: the region of influence)
    """
    eta, w = get_eta_and_w(n)
    x = a[0] * signed_cos(eta, epsilon[0]) * signed_cos(w, epsilon[1])
    y = a[1] * signed_cos(eta, epsilon[0]) * signed_sin(w, epsilon[1])
    z = a[2] * signed_sin(eta, epsilon[0])
    x, y, z = a0 * x, a0 * y, a0 * z
    x_transformed = (t[0] * z / a0 * a[2] + 1) * x + b[0] * np.cos((z + b[1]) / a0 * a[2] * np.pi * b[2])
    y_transformed = (t[1] * z / a0 * a[2] + 1) * y
    z_transformed = z
    return x_transformed, y_transformed, z_transformed



if __name__ == '__main__':
    path_save = "temp.obj"
    n = 10

    a = [1, 1, 1]
    r = 2
    s = 2
    t = 2
    epsilon = [2/r, 2/s, 2/t]
    # x, y, z = superellipsoid(epsilon, a, n)
    # save_obj(path_save, x, y, z)

    a = [1, 1, 1]
    r = 2
    s = 2
    t = 2
    epsilon = [2/r, 2/s, 2/t]
    # x, y, z = superhyperboloid_one_piece(epsilon, a, n = 80)
    # We add a constrain to avoid bad visualization (for superhyperboloid_one_piece)
    # save_obj(path_save, x, y, z, threshold = 100)

    a = [2, 2, 2, 2]
    r = 2
    s = 2
    epsilon = [2/r, 2/s]
    # x, y, z = supertoroids(epsilon, a, n = 20)
    # save_obj(path_save, x, y, z)

    path_save = "temp_cool.obj"
    a = [1, 1, 1]
    r = 2
    s = 2    
    epsilon = [2/r, 2/s]
    a0 = 1
    t = [0.5, 0.3]
    b = [0.5, 0.2, 0.8]
    x, y, z = superellipsoid_taperingz_blendingx(epsilon, a, a0, t, b, n)
    save_obj(path_save, x, y, z)