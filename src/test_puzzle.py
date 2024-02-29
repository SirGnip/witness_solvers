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
    grids = puzzle.find_all_paths(grid, grid.start)
    assert len(grids) == 17


def test_overlay():
    grid = puzzle.Grid(3, 3)
    over = tuple(reversed((
        (' ', '1'),
        ('2', '3')
    )))
    grid.set_cells(over)
    txt = str(grid)
    assert txt == '''
+-+-^
| |1|
+-+-+
|2|3|
O-+-+
Path: [(0, 0)]
        '''.strip()


def test_tri_puzzle():
    grid = puzzle.Grid(4, 4)
    grids_with_paths = puzzle.find_all_paths(grid, grid.start)
    grids_with_complete_paths = [g for g in grids_with_paths if g.path[-1] == g.end]
    cells = tuple(reversed((
        ('3', ' ', ' '),
        (' ', ' ', '2'),
        (' ', ' ', '1'),
    )))

    ans = []
    for g in grids_with_complete_paths:
        g.set_cells(cells)
        if puzzle.is_solved_tri_puzzle(g):
            ans.append(g)

    assert len(grids_with_paths) == 2110
    assert len(grids_with_complete_paths) == 184
    assert len(ans) == 2
