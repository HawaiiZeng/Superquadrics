"""
This file generates arrays. (see res jpeg)
Author: Huayi Zeng
"""

import numpy as np
import os
from superquadrics import *

def save_objs(path_save, x_all, y_all, z_all):
    with open(path_save, "w+") as fout:
        v_inds = 0
        for x, y, z in zip(x_all, y_all, z_all):
            hei, wid = x.shape[0], x.shape[1]
            for i in range(hei):
                for j in range(wid):
                    fout.write("v %.3f %.3f %.3f\n" % (x[i, j], y[i, j], z[i, j]))
            for i in range(hei - 1):
                for j in range(wid - 1):
                    fout.write("f %d %d %d\n" % ((i + 1) * wid + j + 1 + v_inds, i * wid + j + 1 + 1 + v_inds, i * wid + j + 1 + v_inds))
                    fout.write("f %d %d %d\n" % ((i + 1) * wid + j + 1 + 1 + v_inds, i * wid + j + 1 + 1 + v_inds, (i + 1) * wid + j + 1 + v_inds))
            v_inds += hei * wid
            # exit(0)      
def shift_transform(dx, dy, x, y):
    return x - dx, y - dy

def produce_superellipsoid_array(dir_save, n_sampled):
    a = [1, 1, 1]
    n_choice = 30 # Then the total number will be n_choice * n_choice
    rmax = 10
    rmin = 1
    smax = 10
    smin = 1
    t = 2
    dr = (rmax - rmin) / n_choice
    ds = (smax - smin) / n_choice
    y = np.linspace(0, n_choice, n_choice + 1)
    x = np.linspace(0, n_choice, n_choice + 1)
    yv, xv = np.meshgrid(y, x)
    r = rmin + yv * dr
    s = smin + xv * ds
    x_cell = 3.5
    y_cell = 3.5
    x_all, y_all, z_all = [], [], []
    for i in range(n_choice + 1):
        for j in range(n_choice + 1):
            epsilon = [2/r[i, j], 2/s[i, j], 2/t]
            x, y, z = superellipsoid(epsilon, a, n_sampled)
            # print("largest range: ", np.max([np.max(x), np.max(y), np.max(z)])) # always 1
            # path_save = os.path.join(dir_save, "superellipsoid", "%d_%d.obj" % (i, j))
            # save_obj(path_save, x, y, z)
            path_save = os.path.join(dir_save, "superellipsoid", "%d_%d.pts" % (i, j))
            save_pts(path_save, x, y, z)
            dy = -y_cell * i
            dx = -x_cell * j
            x, y = shift_transform(dx, dy, x, y)
            x_all.append(x)
            y_all.append(y)
            z_all.append(z)
    save_objs(os.path.join(dir_save, "all_superellipsoid.obj"), x_all, y_all, z_all)


def produce_supertoroids_array(dir_save, n_sampled):
    a = [2, 2, 2, 2]
    n_choice = 8
    rmax = 10
    rmin = 1
    smax = 10
    smin = 1
    dr = (rmax - rmin) / n_choice
    ds = (smax - smin) / n_choice
    y = np.linspace(0, n_choice, n_choice + 1)
    x = np.linspace(0, n_choice, n_choice + 1)
    yv, xv = np.meshgrid(y, x)
    r = rmin + yv * dr
    s = smin + xv * ds
    x_cell = 14
    y_cell = 14
    x_all, y_all, z_all = [], [], []
    for i in range(n_choice + 1):
        for j in range(n_choice + 1):
            epsilon = [2/r[i, j], 2/s[i, j]]
            x, y, z = supertoroids(epsilon, a, n_sampled)
            # print("largest range: ", np.max([np.max(x), np.max(y), np.max(z)])) # always 6
            # path_save = os.path.join(dir_save, "supertoroids", "%d_%d.obj" % (i, j))
            # save_obj(path_save, x, y, z)
            path_save = os.path.join(dir_save, "supertoroids", "%d_%d.pts" % (i, j))
            save_pts(path_save, x, y, z)
            dy = -y_cell * i
            dx = -x_cell * j
            x, y = shift_transform(dx, dy, x, y)
            x_all.append(x)
            y_all.append(y)
            z_all.append(z)
    save_objs(os.path.join(dir_save, "all_supertoroids.obj"), x_all, y_all, z_all)

if __name__ == '__main__':
    dir_save = "res"
    n_sampled = 20
    produce_superellipsoid_array(dir_save, n_sampled)
    # produce_supertoroids_array(dir_save, n_sampled)