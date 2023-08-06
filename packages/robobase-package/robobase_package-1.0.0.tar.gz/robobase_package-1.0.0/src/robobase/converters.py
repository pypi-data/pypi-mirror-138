import math
import numpy as np


def rotateMatrixToAxisAndAngle(r):
    theta = math.acos((np.trace(r) - 1) / 2)
    if round(theta, 5) == 0:
        return theta, np.array([None, None, None]), None
    if math.pi - 0.001 <= round(theta, 5) <= math.pi + 0.001:
        wx = math.sqrt((r[0][0] + 1) / 2)
        wy = math.sqrt((r[1][1] + 1) / 2) if wx == 0 else r[0][1] / (2 * wx)
        if wx != 0:
            wz = r[0][2] / (2 * wx)
        elif wy != 0:
            wz = r[1][2] / (2 * wy)
        else:
            wz = math.sqrt((r[2][2] + 1) / 2)
        w = np.array([wx, wy, wz])
        return theta, w, -1 * w
    w = np.array([r[2][1] - r[1][2],
                  r[0][2] - r[2][0],
                  r[1][0] - r[0][1]])
    w = w/(2 * math.sin(theta))
    return theta, w, None

