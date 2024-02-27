import copy
import puzzle

def test_make_grid():
    grid = puzzle.Grid(3, 3)
    txt = str(grid)
    assert txt == '''
+-+-^
| | |
+-+-+
| | |
O-+-+
Path: [(0, 0)]
    '''.strip()

def test_make_grid_path():
    grid = puzzle.Grid(3, 3)
    a, b, c = (1, 1), (2, 1), (2, 2)
    grid.edges[frozenset((a, b))] = True
    grid.edges[frozenset((b, c))] = True
    txt = str(grid)
    assert txt == '''
+-+-^
| | X
+-+X+
| | |
O-+-+
Path: [(0, 0)]
    '''.strip()

def test_grid_deepcopy():
    grid = puzzle.Grid(3, 3)
    a, b, c, d = (1, 1), (2, 1), (2, 2), (0, 1)
    grid.edges[frozenset((a, b))] = True
    grid.edges[frozenset((b, c))] = True

    grid2 = copy.deepcopy(grid)
    grid2.edges[frozenset((a, d))] = True

    assert len([v for k, v in grid.edges.items() if v]) == 2
    assert len([v for k, v in grid2.edges.items() if v]) == 3


def test_traversal():
    grid = puzzle.Grid(2, 3)
    grids = puzzle.traverse(grid, grid.start)
    assert len(grids) == 25


