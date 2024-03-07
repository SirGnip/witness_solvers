import datetime
import copy
import itertools
from pathlib import Path
import pickle
import cfg
from typ import Point, PointPair, GridEdges, PointPath, Region, Regions


if cfg.DEBUG:
    EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^+X-X|'  # good for debugging grid/path
else:
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^ ━ ┃ '  # good for showing solutions
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF =   ' O^ ═-║|'  # good for showing solutions
    EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^ ━-┃|'  # good for showing solutions


def pt_add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def pt_in_bounds(p: Point, x_bound: int, y_bound: int) -> bool:
    '''Is given point in bounds. x_bound and y_bound are EXCLUSIVE'''
    x, y = p
    return 0 <= x < x_bound and 0 <= y < y_bound


class RegionsWrapper:
    def __init__(self):
        self.regions: Regions = []

    def get_points(self):
        points = []
        for region in self.regions:
            for point in region:
                points.append(point)
        return points


class Grid:
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.start: Point = (0, 0)
        self.end: Point = (width - 1, height - 1)
        self.edges: GridEdges = {}
        self.path: PointPath = [self.start]
        self.cells: tuple[tuple[str]] | None = None

        for y in range(height):
            for x in range(width):
                pt: Point = (x, y)

                # right
                right = pt_add(pt, cfg.RIGHT)
                if self._contains(right):
                    pair: PointPair = frozenset((pt, right))
                    self.edges[pair] = False

                # up
                up = pt_add(pt, cfg.UP)
                if self._contains(up):
                    pair: PointPair = frozenset((pt, up))
                    self.edges[pair] = False

    def set_cells(self, cells: tuple[tuple[str, ...]]) -> None:
        '''2D tuple of ints representing the values in the  is expected to have 0,0 at bottom left. A "reversed" on a tuple literal will work.'''
        self.cells = cells

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

        for d in (cfg.RIGHT, cfg.UP, cfg.LEFT, cfg.DOWN):
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

    def append_to_path(self, hop: Point) -> None:
        pair: PointPair = frozenset((self.path[-1], hop))
        if pair not in self.edges:
            raise Exception(f'Edge was expected to exist but did not: {pair}')
        self.edges[pair] = True
        self.path.append(hop)

    def delete_edges_from_path(self, edges_to_del: set[PointPair]) -> None:
        [self.edges.pop(e) for e in edges_to_del]

    def touching_edges(self, x: int, y: int) -> int:
        '''given x,y of an overlay cell, return the number of active edges that are adjacent'''
        assert 0 <= x < self.width - 1
        assert 0 <= y < self.height - 1
        bl = (x, y)
        br = (x+1, y)
        tr = (x+1, y+1)
        tl = (x, y+1)
        edges = (
            frozenset((bl, br)),
            frozenset((br, tr)),
            frozenset((tr, tl)),
            frozenset((tl, bl)),
        )
        activated_edges = [e for e in edges if self.edges.get(e, False) == True]
        return len(activated_edges)

    def get_cell_points(self) -> list[Point]:
        return [(x, y) for y in range(self.width - 1) for x in range(self.height - 1)]

    def get_regions_wrapper(self) -> RegionsWrapper:
        final_regions = RegionsWrapper()

        # while points exist that are not classified into regions...
        while True:
            all_cell_points = set(self.get_cell_points())
            points_in_regions = set(final_regions.get_points())
            if len(all_cell_points - points_in_regions) == 0:
                return final_regions

            # Create and grow new region
            start = list(all_cell_points - points_in_regions)[0]
            region = self.make_region(start)

            final_regions.regions.append(region)

    def make_region(self, start: Point) -> Region:
        region = set([start])
        while True:
            new_region = self.grow_step(region)
            if len(new_region) == len(region):
                return region
            else:
                region = new_region

    def grow_step(self, region: Region) -> Region:
        new_region = region.copy()
        for p in region:
            growth = self.grow_around_point(p)
            new_region.update(growth)
        return new_region

    def grow_around_point(self, point: Point) -> set[Point]:
        # BUG: This method doesn't properly handle a grid with some edges missing. It expects to work on a full grid
        # and the higher level code will eliminate paths that use edges that have been eliminated. The way the code
        # below is written, a new edge from calc_edge() is a 'no edge', the "growth" is halted in that direction.
        # But when an internal edge is removed, the growth of a Region should continue. But in this current
        # implementation, a region is blocked by a missing edge.
        points = set()
        # If and edge exists and the edge's state is False, the "grow" is valid
        if self.edges.get(self.calc_edge(point, cfg.RIGHT), 'no edge') == False:
            p = pt_add(point, cfg.RIGHT)
            if pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        if self.edges.get(self.calc_edge(point, cfg.UP), 'no edge') == False:
            p = pt_add(point, cfg.UP)
            if pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        if self.edges.get(self.calc_edge(point, cfg.LEFT), 'no edge') == False:
            p = pt_add(point, cfg.LEFT)
            if pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        if self.edges.get(self.calc_edge(point, cfg.DOWN), 'no edge') == False:
            p = pt_add(point, cfg.DOWN)
            if pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        return points

    def calc_edge(self, point: Point, direction: Point) -> PointPair:
        x, y = point
        direction_map = {
            cfg.RIGHT: frozenset(((x+1, y), (x+1, y+1))),
            cfg.UP: frozenset(((x+1, y+1), (x, y+1))),
            cfg.LEFT: frozenset(((x, y+1), (x, y))),
            cfg.DOWN: frozenset(((x, y), (x+1, y))),
        }
        return direction_map[direction]

    def find_all_paths(self, cur_point: Point) -> list['Grid']:
        '''Given a grid, return a list of grids that contain paths that start/end at the start/end'''
        results: list[Grid] = []
        for pt in self.valid_moves(cur_point):
            g = copy.deepcopy(self)
            g.add_link(cur_point, pt)  # creates new link and adds to grid.path
            results.append(g)
            results.extend(g.find_all_paths(pt))
        return results

    def calc_paths(self, cache_file: str = ''):
        '''Convenience function to generate the initial enumeration of all paths.

        Also caches data to disk if a `cache_file` name is provided'''

        cache = Path(cache_file)
        if cache_file == '' or not cache.exists():
            print('Calculating full set of paths... This may take a couple minutes.')
            grids_with_paths = self.find_all_paths(self.start)
            grids_with_complete_paths = [g for g in grids_with_paths if g.path[-1] == g.end]
            if cache_file != '':  # only write if file was provided
                print(f'Writing results cache to {cache_file}')
                with cache.open('wb') as fout:
                    pickle.dump((grids_with_paths, grids_with_complete_paths), fout)
        else:
            print(f'Reading cached results from {cache_file}.')
            with cache.open('rb') as fin:
                grids_with_paths, grids_with_complete_paths = pickle.load(fin)

        return grids_with_paths, grids_with_complete_paths

    def is_solved_tri_puzzle(self) -> bool:
        '''Return True if the given Grid, cells and path are a solved Triangle puzzle'''
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                cell = self.cells[y][x]
                if cell != ' ':
                    count = int(cell)
                    touching = self.touching_edges(x, y)
                    if count != touching:
                        # print('touch', x, y, val, touching)
                        return False
        return True

    def is_solved_region_puzzle(self) -> bool:
        '''Return True if the given Grid, cells and path are a solved Region puzzle'''
        for region in self.get_regions_wrapper().regions:
            # get cell values for each point in region
            colors = [self.cells[point[1]][point[0]] for point in region]
            # strip out whitespace and count number of unique colors
            colors = {c for c in colors if c.strip() != ''}  # use set for uniqueness
            # if any region has > 1 unique cell color, fail solution
            if len(colors) > 1:
                return False
        return True

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

                def get_char(pair, none_char, on_char, off_char):
                    if pair not in self.edges:
                        return none_char
                    elif self.edges[pair] == True:
                        return on_char
                    elif self.edges[pair] == False:
                        return off_char
                    else:
                        raise RuntimeError('Unable to determine character for point pair: {pair}')

                # right
                right = pt_add(pt, cfg.RIGHT)
                if self._contains(right):
                    pair: PointPair = frozenset((pt, right))
                    txt.write(x * 2 + 1, y * 2, get_char(pair, EMPTY, HORIZ_ON, HORIZ_OFF))

                # up
                up = pt_add(pt, cfg.UP)
                if self._contains(up):
                    pair: PointPair = frozenset((pt, up))
                    txt.write(x * 2, y * 2 + 1, get_char(pair, EMPTY, VERT_ON, VERT_OFF))

                if self.cells is not None:
                    if x < self.width - 1 and y < self.height - 1:
                        char = self.cells[y][x]
                        if char != '':
                            txt.write(x * 2 + 1, y * 2 + 1, char)

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


def demo_simple():
    grid = Grid(3, 3)
    a, b, c = (1, 1), (2, 1), (2, 2)
    grid.edges[frozenset((a, b))] = True
    grid.edges[frozenset((b, c))] = True
    print(grid)


def demo_traversal():
    grid = Grid(4, 4)
    print()
    # print(grid)
    results = grid.find_all_paths(grid.start)
    # for r in results:
    #     print()
    #     print(r)
    print('end to end ----------------')
    end_to_end = [r for r in results if r.path[-1] == r.end]
    # for r in end_to_end[:30]:
    #     print()
    #     print(r)
    print(f'counts {len(results)} {len(end_to_end)}')


def demo_tri():
    grid = Grid(3, 3)
    cells = tuple(reversed((
        (' ', ' '),
        ('3', ' '),
    )))
    grid.set_cells(cells)
    print(grid)
    results = grid.find_all_paths(grid.start)
    print(len(results))
    ans = []

    end_to_end = [r for r in results if r.path[-1] == r.end]

    for idx, g in enumerate(end_to_end):
        if g.is_solved_tri_puzzle():
            ans.append(g)

    print('answers', '-' * 20)
    for g in ans:
        print()
        print(g)
    print('counts', len(results), len(end_to_end), len(ans))


def demo_solve_tri_puzzles():
    '''precalculate grids and solve multiple puzzles, starting with the same grid (testing the optimization)'''
    test_cells = []
    test_cells.append(tuple(reversed((
        ('3', ' ', ' ', ' '),
        (' ', ' ', '2', '1'),
        (' ', ' ', '1', ' '),
        ('2', ' ', '1', ' '),
    ))))
    test_cells.append(tuple(reversed((
        (' ', ' ', ' ', ' '),
        (' ', ' ', ' ', '1'),
        ('2', ' ', '1', '1'),
        (' ', '1', '2', ' '),
    ))))
    test_cells.append(tuple(reversed((
        ('1', ' ', ' ', ' '),
        (' ', '2', '2', '1'),
        (' ', '1', '2', ' '),
        ('2', ' ', '1', ' '),
    ))))

    grid = Grid(5, 5)
    grids_with_paths = grid.find_all_paths(grid.start)
    grids_with_complete_paths = [g for g in grids_with_paths if g.path[-1] == g.end]

    for cells in test_cells:
        print('=' * 80, datetime.datetime.now())
        grid.set_cells(cells)
        print(grid)

        ans = []
        for g in grids_with_complete_paths:
            g.set_cells(cells)
            if g.is_solved_region_puzzle():
                ans.append(g)
                print(g)
        print('counts', len(grids_with_paths), len(grids_with_complete_paths), len(ans))


def demo_initial_region_solve():
    cells = tuple(reversed((
        ('b', ' ', 'b', 'w'),
        ('w', ' ', 'w', ' '),
        (' ', 'b', ' ', ' '),
        ('w', ' ', ' ', 'w'),
    )))
    edges_to_del: set[PointPair] = {
        frozenset(((4, 0), (3, 0))),
        frozenset(((3, 0), (3, 1))),
        frozenset(((3, 1), (2, 1))),
        frozenset(((3, 2), (3, 3))),
        frozenset(((1, 2), (1, 3))),
    }

    grid = Grid(5, 5)
    grid.set_cells(cells)

    # print starting grid
    grid.delete_edges_from_path(edges_to_del)  # because paths are caching in calc_paths(), this deletion only is cosmetic for the print()
    print(grid)

    grids_with_paths, grids_with_complete_paths = grid.calc_paths('grid_5x5.cache.pickle')

    ans = []
    for g in grids_with_complete_paths:
        if g.is_solved_region_puzzle():

            # Test if any of the path segments do not exist in the grid
            # This is possible because in general we are loading the fully enumerated list of Paths from disk
            # and are not re-traversing the grid each time. It is a performance optimization to load the generic
            # but exhaustive path traversal and simply skip any valid paths that use edges that don't exist in the grid.
            keep = True
            for points_on_path in itertools.pairwise(g.path):
                if frozenset(points_on_path) in edges_to_del:
                    keep = False
                    break
            if keep:
                ans.append(g)

    print('answers', '-' * 20)
    for g in ans:
        g.delete_edges_from_path(edges_to_del)  # this removal is only for printing purposes
        print()
        print(g)
    print('counts', len(grids_with_paths), len(grids_with_complete_paths), len(ans))
    print('end ', datetime.datetime.now())


def main():
    s = datetime.datetime.now()

    demo_simple()
    demo_traversal()
    demo_tri()
    demo_solve_tri_puzzles()
    demo_initial_region_solve()

    e = datetime.datetime.now()
    print(f'{e - s} ({s} -> {e})')


if __name__ == '__main__':
    main()
