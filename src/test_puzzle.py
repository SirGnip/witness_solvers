import puzzle

def test_make_grid():
    grid = puzzle.Grid(3, 3)
    txt = str(grid)
    assert txt == '''
+-+-+
| | |
+-+-+
| | |
+-+-+
    '''.strip()

def test_make_grid_path():
    grid = puzzle.Grid(3, 3)
    a, b, c = (1, 1), (2, 1), (2, 2)
    grid.edges[frozenset((a, b))] = True
    grid.edges[frozenset((b, c))] = True
    txt = str(grid)
    assert txt == '''
+-+-+
| | X
+-+X+
| | |
+-+-+
    '''.strip()
