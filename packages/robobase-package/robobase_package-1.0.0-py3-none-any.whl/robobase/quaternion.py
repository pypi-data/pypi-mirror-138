import numpy
import math


class Quaternion:
    def __init__(self, scalar: float = 1.0, vector=None):
        if vector is None:
            vector = [1, 1, 1]
        self._scalar = round(scalar, 3)
        self._vector = numpy.array(vector)

    @classmethod
    def fromAngleAndVector(cls, angle: float = 0.0, v=None):
        if v is None:
            v = [1, 1, 1]
        _scalar = math.cos(angle/2)
        _vector = numpy.array(v) * math.sin(angle/2)
        return cls(_scalar, _vector)

    def __mul__(self, other):
        scalar = self._scalar * other.scalar - numpy.dot(self.vector.transpose(), other.vector)
        vector = self._scalar * other.vector + other.scalar * self.vector + numpy.cross(self.vector, other.vector)
        return Quaternion(scalar, vector)

    def __add__(self, other):
        scalar = self._scalar + other.scalar
        vector = self._vector + other.vector
        return Quaternion(scalar, vector)

    def __sub__(self, other):
        scalar = self._scalar - other.scalar
        vector = self._vector - other.vector
        return Quaternion(scalar, vector)

    def scalarMulti(self, other) -> float:
        return (other.scalar * self.scalar + other.x * self.x + other.y * self.y + other.z * self.z) \
               / (self.norma() * other.norma())

    def multiToScalar(self, s):
        scalar = self._scalar *  s
        vector = self._vector * s
        return Quaternion(scalar, vector)

    def toRotateMatrix(self):
        a11 = 1 - 2 * self.y ** 2 - 2 * self.z ** 2
        a12 = 2 * self.x * self.y - 2 * self.z * self.scalar
        a13 = 2 * self.x * self.z + 2 * self.y * self.scalar

        a21 = 2 * self.x * self.y + 2 * self.z * self.scalar
        a22 = 1 - 2 * self.x ** 2 - 2 * self.z ** 2
        a23 = 2 * self.y * self.z - 2 * self.x * self.scalar

        a31 = 2 * self.x * self.z - 2 * self.y * self.scalar
        a32 = 2 * self.y * self.z + 2 * self.x * self.scalar
        a33 = 1 - 2 * self.x ** 2 - 2 * self.y ** 2

        R = numpy.array([[a11, a12, a13],
                         [a21, a22, a23],
                         [a31, a32, a33]])
        return R

    def norma(self):
        return math.sqrt(self._scalar ** 2 + numpy.dot(self._vector.transpose(), self._vector))

    def isUnit(self):
        return round(self.norma()) == 1

    @property
    def scalar(self):
        return self._scalar

    @scalar.setter
    def scalar(self, value):
        self._scalar = value

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        self._vector = value

    @property
    def x(self):
        return self._vector[0]

    @x.setter
    def x(self, value):
        self._vector[0] = value

    @property
    def y(self):
        return self._vector[1]

    @y.setter
    def y(self, value):
        self._vector[1] = value

    @property
    def z(self):
        return self._vector[2]

    @z.setter
    def z(self, value):
        self._vector[2] = value
