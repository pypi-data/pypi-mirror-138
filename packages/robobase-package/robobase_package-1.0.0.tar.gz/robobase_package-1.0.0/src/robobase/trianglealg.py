class Point:

    def __init__(self, coords=None):
        if coords is None:
            coords = [0, 0]
        self.x = coords[0]
        self.y = coords[1]

    def coord(self):
        return [self.x, self.y]


class Triangle:

    def __init__(self, points=None):
        if points is None:
            points = [Point(), Point(), Point()]
        self.point_1 = points[0]
        self.point_2 = points[1]
        self.point_3 = points[2]

    def isIntersection(self, other):
        if self.checkSeparate(self.linePointPairs(), other.points()):
            return False
        if self.checkSeparate(other.linePointPairs(), self.points()):
            return False
        return True

    @classmethod
    def checkSeparate(cls, pairs, points):
        for s_p in pairs:
            duration = cls.isClockWise(s_p[0], s_p[1], s_p[2])
            separate = True
            for p in points:
                if duration == cls.isClockWise(s_p[0], s_p[1], p) or cls.isLine(s_p[0], s_p[1], p):
                    separate = False
                    break
            if separate:
                return True
        return False

    def points(self):
        return [self.point_1, self.point_2, self.point_3]

    def edges(self):
        return [[self.point_1, self.point_2], [self.point_2, self.point_3], [self.point_3, self.point_1]]

    def linePointPairs(self):
        return [[self.point_1, self.point_2, self.point_3],
                [self.point_2, self.point_3, self.point_1],
                [self.point_3, self.point_1, self.point_2]]

    @staticmethod
    def durationRotate(first: Point, second: Point, third: Point):
        return (second.x - first.x) * (third.y - first.y) - (second.y - first.y) * (third.x - first.x)

    @classmethod
    def isClockWise(cls, first: Point, second: Point, third: Point):
        return cls.durationRotate(first, second, third) < 0

    @classmethod
    def isLine(cls, first: Point, second: Point, third: Point):
        return cls.durationRotate(first, second, third) == 0
