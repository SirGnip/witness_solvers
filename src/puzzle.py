import datetime
import copy

Point = tuple[int, int]
PointPair = frozenset[Point]
GridEdges = dict[PointPair, bool]
Path = list[Point]

RIGHT: Point = (1, 0)
UP: Point = (0, 1)
LEFT: Point = (-1, 0)
DOWN: Point = (0, -1)

START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = 'O^+X-X|'


def pt_add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


class Grid:
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.start: Point = (0, 0)
        self.end: Point = (width - 1, height - 1)
        self.edges: GridEdges = {}
        self.path: Path = [self.start]

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

    def valid_moves(self, pt: Point) -> list[Point]:
        '''Return all valid points around the given point that are valid moves
        Path is blocked by points that fall outside of the board and links that are already visited.'''
        results = []

        # Avoid intersections that lines have already traveled through (algorithm was traveling through "corners"
        # that were already drawn in.
        points = set()
        pairs = [pair for pair, state in self.edges.items() if state == True]
        for a, b in pairs:
            points.add(a)
            points.add(b)

        for d in (RIGHT, UP, LEFT, DOWN):
            hop = pt_add(pt, d)
            if self._contains(hop):
                pair = frozenset((pt, hop))
                if pair in self.edges and self.edges[pair] == False and hop not in points:
                    results.append(hop)
        return results

    def add_link(self, start: Point, hop: Point) -> None:
        pair: PointPair = frozenset((start, hop))
        if pair not in self.edges:
            raise Exception(f'Edge was expected to exist but did not: {pair}')
        self.edges[pair] = True
        self.path.append(hop)

    def __str__(self) -> str:
        txt = TextGrid((self.width-1) * 2 + 1, (self.height-1) * 2 + 1)

        for y in range(self.height):
            for x in range(self.width):
                pt = (x, y)

                # intersection
                char = INTERSECT
                if pt == self.start:
                    char = START
                if pt == self.end:
                    char = END
                txt.write(x * 2, y * 2, char)

                # right
                right = pt_add(pt, RIGHT)
                if self._contains(right):
                    pair: PointPair = frozenset((pt, right))
                    txt.write(x * 2 + 1, y * 2, HORIZ_ON if self.edges.get(pair, False) else HORIZ_OFF)

                # up
                up = pt_add(pt, UP)
                if self._contains(up):
                    pair: PointPair = frozenset((pt, up))
                    txt.write(x * 2, y * 2 + 1, VERT_ON if self.edges.get(pair, False) else VERT_OFF)
        return str(txt) + f'\nPath: {self.path}'


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


def traverse(given_grid: Grid, cur_point: Point) -> list[Grid]:
    '''Given a grid, return a list of grids that contain paths that start/end at the start/end'''
    results: list[Grid] = []
    for pt in given_grid.valid_moves(cur_point):
        g = copy.deepcopy(given_grid)
        g.add_link(cur_point, pt)  # creates new link and adds to grid.path
        results.append(g)
        results.extend(traverse(g, pt))
    return results


def temp_test_1():
    grid = Grid(3, 3)
    a, b, c = (1, 1), (2, 1), (2, 2)
    grid.edges[frozenset((a, b))] = True
    grid.edges[frozenset((b, c))] = True
    print(grid)


def temp_traversal_demo():
    grid = Grid(4, 4)
    print()
    # print(grid)
    results = traverse(grid, grid.start)
    # for r in results:
    #     print()
    #     print(r)
    print('end to end ----------------')
    end_to_end = [r for r in results if r.path[-1] == r.end]
    # for r in end_to_end[:30]:
    #     print()
    #     print(r)
    print(f'counts {len(results)} {len(end_to_end)}')


def main():
    # temp_test_1()

    s = datetime.datetime.now()
    temp_traversal_demo()
    e = datetime.datetime.now()
    print(f'{e - s} ({s} -> {e})')


if __name__ == '__main__':
    main()
