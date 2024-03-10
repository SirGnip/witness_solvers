from typ import Point, PointPair, GridEdges, PointPath, Region, Regions

def lerp(a: float, b: float, u: float) -> float:
    '''Linear interpolation'''
    return a + ((b - a) * u)


def pt_add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def pt_in_bounds(p: Point, x_bound: int, y_bound: int) -> bool:
    '''Is given point in bounds. x_bound and y_bound are EXCLUSIVE'''
    x, y = p
    return 0 <= x < x_bound and 0 <= y < y_bound


def pt_lerp(p1, p2, u):
    x1, y1 = p1
    x2, y2 = p2
    return lerp(x1, x2, u), lerp(y1, y2, u)

