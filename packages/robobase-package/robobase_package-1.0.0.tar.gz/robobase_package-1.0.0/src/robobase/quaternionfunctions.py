import math

from .quaternion import Quaternion


def nextQ(q0: Quaternion, q1: Quaternion, theta: float, t: int):
    firstPart = math.sin((1 - t) * theta) / math.sin(theta)
    secondPart = math.sin(t * theta) / math.sin(theta)
    return q0.multiToScalar(firstPart) + q1.multiToScalar(secondPart)


def quatSlerp(q0: Quaternion, q1: Quaternion, step: int = 3):
    cosTheta = q0.scalarMulti(q1)
    theta = math.acos(cosTheta)
    if theta > math.pi:
        theta -= 2 * math.pi
    quaternions = list()
    tList = [i / step for i in range(step + 1)]
    for t in tList:
        quaternions.append(nextQ(q0, q1, theta, t))
    return quaternions
