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
