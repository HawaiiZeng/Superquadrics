"""
This file performs deformation on superquadrics
Author: Huayi Zeng
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from superquadrics import superellipsoid, save_obj

class Transformation(object):
    """
    The abstract class for Transformation
    See https://www.digitalocean.com/community/tutorials/understanding-class-inheritance-in-python-3 for guidance
    """
    def __init__(self):
        super(Transformation, self).__init__()
        self.jac = None

    @abstractmethod
    def apply_t(self, x, y, z):
        """
        Input: x, y, z with Nx1 each
        """
        pass
        
class TaperingZ(Transformation):
    """
    Tapering along z axis
    Ref: Global and local deformations of solid primitives 
         AH Barr - ‎1984
    """
    def __init__(self, k):
        super(TaperingZ, self).__init__()
        self.k = k
    def apply_t(self, x, y, z):
        r = self.k * z
        x, y = r * x, r * y
        return x, y, z

class BendingZ(Transformation):
    """
    Bending along z axis
    Ref: Recovery of Parametric Models from Range Images: The Case for Superquadrics with Global Deformations.
    alpha: orientation
    k: how much it bends
    """     
    def __init__(self, alpha, k):
        super(BendingZ, self).__init__()
        self.alpha = alpha
        self.k = k
        self.k_inv = 1 / k
    def apply_t(self, x, y, z):
        beta = np.arctan2(y, x)
        r = np.cos(self.alpha - beta) * np.sqrt(x**2 + y**2)
        gamma = z * self.k_inv
        R = self.k_inv - np.cos(gamma) * (self.k_inv - r)
        x = x + np.cos(self.alpha) * (R - r)
        y = y + np.sin(self.alpha) * (R - r)
        z = np.sin(gamma) * (self.k_inv - r)
        return x, y, z

if __name__ == '__main__':
    n = 10
    a = [1, 1, 1]
    r = 2
    s = 2
    t = 2
    epsilon = [2/r, 2/s, 2/t]
    x, y, z = superellipsoid(epsilon, a, n)
    save_obj("temp.obj", x, y, z)

    # taperingZ = TaperingZ(0.5)
    # x, y, z = taperingZ.apply_t(x, y, z)

    bendingZ = BendingZ(alpha = -1.5, k = 0.5)
    x, y, z = bendingX.apply_t(x, y, z)
    
    save_obj("temp_d.obj", x, y, z)