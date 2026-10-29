import numpy as np
import math

class Matrix3x3:
    @staticmethod
    def identity():
        return np.identity(3)

    @staticmethod
    def translation(tx, ty):
        mat = np.identity(3)
        mat[0, 2] = tx
        mat[1, 2] = ty
        return mat

    @staticmethod
    def rotation(radians):
        mat = np.identity(3)
        cos_t = math.cos(radians)
        sin_t = math.sin(radians)
        mat[0, 0] = cos_t
        mat[0, 1] = -sin_t
        mat[1, 0] = sin_t
        mat[1, 1] = cos_t
        return mat

    @staticmethod
    def scaling(sx, sy):
        mat = np.identity(3)
        mat[0, 0] = sx
        mat[1, 1] = sy
        return mat

    @staticmethod
    def shear(shx, shy):
        mat = np.identity(3)
        mat[0, 1] = shx
        mat[1, 0] = shy
        return mat

    @staticmethod
    def reflection(flip_x=False, flip_y=False):
        mat = np.identity(3)
        if flip_x:
            mat[0, 0] = -1
        if flip_y:
            mat[1, 1] = -1
        return mat

    @staticmethod
    def pivot_transform(linear, pivot_x, pivot_y):
        """T(pivot) * linear * T(-pivot)."""
        t1 = Matrix3x3.translation(-pivot_x, -pivot_y)
        t2 = Matrix3x3.translation(pivot_x, pivot_y)
        return np.dot(t2, np.dot(linear, t1))

    @staticmethod
    def transform_point(matrix, x, y):
        """Menerapkan transformasi matriks homogen 3x3 ke koordinat 2D (x, y)."""
        vec = np.array([x, y, 1.0])
        res = np.dot(matrix, vec)
        return res[0], res[1]
