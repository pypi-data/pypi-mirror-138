import random
from math import pi

import numpy as np


def xRotation(vector, theta):
    """Поворот 3D вектора вокруг оси x"""
    R = np.array([[1, 0, 0],
                  [0, np.cos(theta), -np.sin(theta)],
                  [0, np.sin(theta), np.cos(theta)]])
    return np.dot(R, vector)


def yRotate(vector, theta):
    """Поворот 3D вектора вокруг оси y"""
    R = np.array([[np.cos(theta), 0, np.sin(theta)],
                  [0, 1, 0],
                  [-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(R, vector)


def zRotate(vector, theta):
    """Поворот 3D вектора вокруг оси z"""
    R = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])
    return np.dot(R, vector)


def randomRotate(vector):
    """Поворот 3D вектора на рандомные углы вокруг оси x, y и z"""
    x = random.randint(int(-pi * 100), int(pi * 100)) / 100
    y = random.randint(int(-pi * 100), int(pi * 100)) / 100
    z = random.randint(int(-pi * 100), int(pi * 100)) / 100
    return zRotate(yRotate(xRotation(vector, x), y), z)
