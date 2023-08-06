import sympy as sy

from .dhmatrix import DHMatrix


class ForwardKinematics:
    """Класс для работы с прямой кинематикой"""

    @staticmethod
    def links(d: list, r: list, thetas: list, alpha: list) -> list:
        """Формирование всех матриц преобразования T(i-1, i)"""
        return [DHMatrix.matrix(r[i], alpha[i], d[i], thetas[i]) for i in range(len(d))]

    @staticmethod
    def frames(links: list) -> list:
        """Формирование всех матриц преобразования T(0, i) где i от 0 до N"""
        frames = list([sy.eye(4)])
        frames.append(links[0])
        for i in range(1, len(links)):
            frames.append(frames[-1] * links[i])
        return frames

    @staticmethod
    def resultMatrix(links: list) -> sy.Matrix:
        """Формирование результирующей матрицы преобразования"""
        fk = links[0]
        for i in range(1, len(links)):
            fk = fk * links[i]
        return fk
