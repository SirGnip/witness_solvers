import datetime
import copy
import itertools
from pathlib import Path
import pickle
import cfg
import utils
from typ import Point, PointPair, GridEdges, PointPath, Region, Regions


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
    '''Origin is at top-left'''
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.start: Point = (0, height - 1)
        self.end: Point = (width - 1, 0)
        self.edges: GridEdges = {}
        self.path: PointPath = [self.start]
        self.cells: tuple[tuple[str]] | None = None

        for edge in self.enumerate_all_edges(self.width, self.height):
            self.edges[edge] = False

    def set_cells(self, cells: tuple[tuple[str, ...]]) -> None:
        '''2D tuple of ints representing the values in the grid cells (boxes, triangle count, etc). Origin is top-left.'''
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

        for d in (cfg.RIGHT, cfg.DOWN, cfg.LEFT, cfg.UP):
            hop = utils.pt_add(pt, d)
            if self._contains(hop):
                pair = frozenset((pt, hop))
                if pair in self.edges and self.edges[pair] == False and hop not in points:
                    results.append(hop)
        return results

    @staticmethod
    def enumerate_all_edges(width, height):
        for y in range(height):
            points = [(x, y) for x in range(width)]
            yield from [frozenset(pair) for pair in itertools.pairwise(points)]
        for x in range(width):
            points = [(x, y) for y in range(height)]
            yield from [frozenset(pair) for pair in itertools.pairwise(points)]

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
        '''Return a set of Points around the given points after "growing" the point.
        Note: A `Point` in this function represents the location of a cell, NOT an intersection of grid lines.'''

        # BUG: This method doesn't properly handle a grid with some edges missing. It does function properly on a full
        # grid. I currently don't use this function to handle grids with missing edges.  But, to get around this, I have
        # higher level functions in the puzzle solving logic that do logic with missing edges and eliminates those paths.
        # That was easier than making this function more general.
        #
        # Description of bug: With the code below as written, a new edge from calc_edge() is a 'no edge', the "growth"
        # is halted in that direction. But when an internal edge is removed, the growth of a Region should continue.
        # But in this current implementation, a region is blocked by a missing edge.
        points = set()
        # If and edge exists and the edge's state is False, the "grow" is valid

        if not self.edges.get(self.calc_edge(point, cfg.RIGHT), 'no edge'):
            # p = utils.pt_add(point, cfg.RIGHT)  # removed for potential optimization
            p = point[0] + cfg.RIGHT[0], point[1] + cfg.RIGHT[1]
            if utils.pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        if not self.edges.get(self.calc_edge(point, cfg.UP), 'no edge'):
            # p = utils.pt_add(point, cfg.UP)
            p = point[0] + cfg.UP[0], point[1] + cfg.UP[1]
            if utils.pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        if not self.edges.get(self.calc_edge(point, cfg.LEFT), 'no edge'):
            # p = utils.pt_add(point, cfg.LEFT)
            p = point[0] + cfg.LEFT[0], point[1] + cfg.LEFT[1]
            if utils.pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        if not self.edges.get(self.calc_edge(point, cfg.DOWN), 'no edge'):
            # p = utils.pt_add(point, cfg.DOWN)
            p = point[0] + cfg.DOWN[0], point[1] + cfg.DOWN[1]
            if utils.pt_in_bounds(p, self.width - 1, self.height - 1):
                points.add(p)
        return points

    def calc_edge(self, point: Point, direction: Point) -> PointPair:
        '''Given a Point (that identifies a cell), return the Edge that lies in the direction given
        Note: It is overloading terminology a bit, but Point here is the x,y of a cell while the PointPair contains x,y
        values that represent points on the grid lines. The x,y values represent two slightly different concepts here.'''
        # This function is called 1.5 million times when solving a puzzle. Keep it tight.
        x, y = point
        if direction == cfg.RIGHT:
            return frozenset(((x+1, y+1), (x+1, y)))
        elif direction == cfg.DOWN:
            return frozenset(((x, y+1), (x+1, y+1)))
        elif direction == cfg.LEFT:
            return frozenset(((x, y), (x, y + 1)))
        elif direction == cfg.UP:
            return frozenset(((x+1, y), (x, y)))
        else:
            raise RuntimeError('Unexpected direction: {direction}')

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
        '''Wrapper function around find_all_paths() that either calls find_all_paths() or reads the results from a cache.
        Caches generated data to disk if a `cache_file` name is provided'''

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

    def is_solved_region_puzzle(self, edges_to_del: set[PointPair]) -> bool:
        '''Return True if the given Grid, cells and path are a solved Region puzzle'''
        for region in self.get_regions_wrapper().regions:
            # get cell values for each point in region
            colors = [self.cells[point[1]][point[0]] for point in region]
            # strip out whitespace and count number of unique colors
            colors = {c for c in colors if c.strip() != ''}  # use set for uniqueness
            # if any region has > 1 unique cell color, fail solution
            if len(colors) > 1:
                return False

        # Test if any of the path segments have been removed via `edges_to_del`.
        # This is possible because in general we are creating a grids with fully traversed paths (often loaded from
        # disk) that do NOT take removed edges into the enumeration. This is a performance optimization (cache the
        # exhaustive enumeration of all paths to disk and then load it. Then, I get the list of paths that meet the
        # region requirements (code above) and then reject any potential solution paths that include an edge that
        # is rejected via `edges_to_del`.
        for points_on_path in itertools.pairwise(self.path):
            if frozenset(points_on_path) in edges_to_del:
                return False

        return True

    def __str__(self) -> str:
        txt = TextGrid((self.width-1) * 2 + 1, (self.height-1) * 2 + 1)

        for y in range(self.height):
            for x in range(self.width):
                pt = (x, y)  # point on a grid line, not a cell

                # intersection
                char = cfg.INTERSECT
                if pt == self.start:
                    char = cfg.START
                if pt == self.end:
                    char = cfg.END
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
                right = utils.pt_add(pt, cfg.RIGHT)
                if self._contains(right):
                    pair: PointPair = frozenset((pt, right))
                    txt.write(x * 2 + 1, y * 2, get_char(pair, cfg.EMPTY, cfg.HORIZ_ON, cfg.HORIZ_OFF))

                # down
                down = utils.pt_add(pt, cfg.DOWN)
                if self._contains(down):
                    pair: PointPair = frozenset((pt, down))
                    txt.write(x * 2, y * 2 + 1, get_char(pair, cfg.EMPTY, cfg.VERT_ON, cfg.VERT_OFF))

                if self.cells is not None:
                    if x < self.width - 1 and y < self.height - 1:
                        char = self.cells[y][x]
                        if char != '':
                            txt.write(x * 2 + 1, y * 2 + 1, char)

        return str(txt) + f'\nPath: {self.path}'


class TextGrid:
    '''Helper class that eases writing a character to x, y positions in a 2D grid of characters

    The origin is at the top-left of the grid'''
    def __init__(self, width, height, default=' '):
        self.grid = [[default for x in range(width)] for y in range(height)]

    def __str__(self):
        rows = [''.join(row) for row in self.grid]
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
    cells = tuple((
        (' ', ' '),
        ('3', ' '),
    ))
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
    test_cells.append(tuple((
        ('3', ' ', ' ', ' '),
        (' ', ' ', '2', '1'),
        (' ', ' ', '1', ' '),
        ('2', ' ', '1', ' '),
    )))
    test_cells.append(tuple((
        (' ', ' ', ' ', ' '),
        (' ', ' ', ' ', '1'),
        ('2', ' ', '1', '1'),
        (' ', '1', '2', ' '),
    )))
    test_cells.append(tuple((
        ('1', ' ', ' ', ' '),
        (' ', '2', '2', '1'),
        (' ', '1', '2', ' '),
        ('2', ' ', '1', ' '),
    )))

    grid = Grid(5, 5)
    # Note: If you create a cached paths pickle file with codepaths in puzzle.py, you can NOT load it in runner.py
    # because the module paths stored in the .pickle file are not visible to runner.py. But, if the pickle file is
    # generated in a runner.py codepath, code in puzzle.py will be able to load it.
    grids_with_paths, grids_with_complete_paths = grid.calc_paths('grid_5x5.cache.pickle')

    for cells in test_cells:
        print('=' * 80, datetime.datetime.now())
        grid.set_cells(cells)
        print(grid)

        ans = []
        for g in grids_with_complete_paths:
            g.set_cells(cells)
            if g.is_solved_tri_puzzle():
                ans.append(g)
                print(g)
        print('counts', len(grids_with_paths), len(grids_with_complete_paths), len(ans))


def demo_initial_region_solve():
    cells = tuple((
        ('b', ' ', 'b', 'w'),
        ('w', ' ', 'w', ' '),
        (' ', 'b', ' ', ' '),
        ('w', ' ', ' ', 'w'),
    ))
    edges_to_del: set[PointPair] = {
        frozenset(((4, 4), (3, 4))),
        frozenset(((3, 4), (3, 3))),
        frozenset(((3, 3), (2, 3))),
        frozenset(((3, 2), (3, 1))),
        frozenset(((1, 2), (1, 1))),
    }

    grid = Grid(5, 5)
    grid.set_cells(cells)

    # print starting grid
    grid.delete_edges_from_path(edges_to_del)  # because paths are caching in calc_paths(), this deletion only is cosmetic for the print()
    print(grid)

    grids_with_paths, grids_with_complete_paths = grid.calc_paths('grid_5x5.cache.pickle')

    ans = []
    for g in grids_with_complete_paths:
        g.set_cells(cells)
        if g.is_solved_region_puzzle(edges_to_del):
            ans.append(g)

    print('answers', '-' * 20)
    for g in ans:
        g.delete_edges_from_path(edges_to_del)  # this removal is only for printing purposes
        print()
        print(g)
    print('counts',len( grids_with_paths), len(grids_with_complete_paths), len(ans))
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



