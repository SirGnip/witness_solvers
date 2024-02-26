Point = tuple[int, int]
PointPair = frozenset[Point]
GridEdges = dict[PointPair, bool]

RIGHT: Point = (1, 0)
UP: Point = (0, 1)
DOT, HORIZ, VERT = '+-|'


def pt_add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


class Grid:
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.edges: GridEdges = {}

        for y in range(height):
            for x in range(width):
                pt: Point = (x, y)

                # right
                right = pt_add(pt, RIGHT)
                if self._contains(right):
                    pair: PointPair = frozenset((pt, right))
                    self.edges[pair] = False

                # up
                up = pt_add(pt, UP)
                if self._contains(up):
                    pair: PointPair = frozenset((pt, up))
                    self.edges[pair] = False

    def _contains(self, pt: Point) -> bool:
        '''Test if grid contains given point'''
        x, y = pt
        return 0 <= x < self.width and 0 <= y < self.height

    def __str__(self) -> str:
        txt = TextGrid((self.width-1) * 2 + 1, (self.height-1) * 2 + 1)

        for y in range(self.height):
            for x in range(self.width):
                # intersection
                txt.write(x * 2, y * 2, DOT)

                # right
                pt = (x, y)
                right = pt_add(pt, RIGHT)
                if self._contains(right):
                    pair: PointPair = frozenset((pt, right))
                    if pair in self.edges:
                        txt.write(x * 2 + 1, y * 2, HORIZ)

                # up
                up = pt_add(pt, UP)
                if self._contains(up):
                    pair: PointPair = frozenset((pt, up))
                    if pair in self.edges:
                        txt.write(x * 2, y * 2 + 1, VERT)

        return str(txt)


class TextGrid:
    '''Helper class that eases writing a character to x, y positions in a 2D grid of characters'''
    def __init__(self, width, height, default=' '):
        self.grid = [[default for x in range(width)] for y in range(height)]

    def __str__(self):
        rows = [''.join(row) for row in self.grid]
        rows.reverse()
        return '\n'.join(rows)

    def write(self, x, y, char):
        self.grid[y][x] = char


def main():
    grid = Grid(3, 3)
    print(grid)


if __name__ == '__main__':
    main()
