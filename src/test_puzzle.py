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
Path: [(0, 2)]
    '''.strip()

def test_make_grid_path():
    grid = puzzle.Grid(3, 3)
    a, b, c = (1, 1), (2, 1), (2, 0)
    grid.edges[frozenset((a, b))] = True
    grid.edges[frozenset((b, c))] = True
    txt = str(grid)
    assert txt == '''
+-+-^
| | X
+-+X+
| | |
O-+-+
Path: [(0, 2)]
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
    grids = grid.find_all_paths(grid.start)
    assert len(grids) == 17


def test_overlay():
    grid = puzzle.Grid(3, 3)
    over = tuple((
        (' ', '1'),
        ('2', '3')
    ))
    grid.set_cells(over)
    txt = str(grid)
    assert txt == '''
+-+-^
| |1|
+-+-+
|2|3|
O-+-+
Path: [(0, 2)]
        '''.strip()


def test_tri_puzzle():
    grid = puzzle.Grid(4, 4)
    grids_with_paths, grids_with_complete_paths = grid.calc_paths()

    cells = tuple((
        ('3', ' ', ' '),
        (' ', ' ', '2'),
        (' ', ' ', '1'),
    ))

    ans = []
    for g in grids_with_complete_paths:
        g.set_cells(cells)
        if g.is_solved_tri_puzzle():
            ans.append(g)

    assert len(grids_with_paths) == 2110
    assert len(grids_with_complete_paths) == 184
    assert len(ans) == 2


def test_region_separator():
    g = puzzle.Grid(3, 3)
    # print()
    # print(g)
    g.append_to_path((1, 2))
    g.append_to_path((1, 1))
    g.append_to_path((2, 1))
    g.append_to_path((2, 0))
    # print(g)

    regions = g.get_regions_wrapper()  # list[list[cell]]
    assert len(regions.regions) == 2
    region_sizes = {len(r) for r in regions.regions}
    assert region_sizes == {1, 3}
    # for r in regions.regions:
    #     print(r)


def test_region_separator_large():
    g = puzzle.Grid(5, 5)
    # print()
    # print(g)
    g.append_to_path((1, 4))
    g.append_to_path((1, 3))
    g.append_to_path((0, 3))
    g.append_to_path((0, 2))
    g.append_to_path((0, 1))
    g.append_to_path((0, 0))
    g.append_to_path((1, 0))
    g.append_to_path((2, 0))
    g.append_to_path((3, 0))
    g.append_to_path((3, 1))
    g.append_to_path((2, 1))
    g.append_to_path((1, 1))
    g.append_to_path((1, 2))
    g.append_to_path((2, 2))
    g.append_to_path((2, 3))
    g.append_to_path((2, 4))
    g.append_to_path((3, 4))
    g.append_to_path((3, 3))
    g.append_to_path((3, 2))
    g.append_to_path((4, 2))
    g.append_to_path((4, 1))
    g.append_to_path((4, 0))
    # print(g)

    regions = g.get_regions_wrapper()  # list[list[cell]]
    assert len(regions.regions) == 4
    region_sizes = {len(r) for r in regions.regions}
    assert region_sizes == {1, 7, 2, 6}
    # for r in regions.regions:
    #     print(r)

def test_region_puzzle_4x4_2_color():
    grid = puzzle.Grid(4, 4)
    grids_with_paths, grids_with_complete_paths = grid.calc_paths()
    cells = tuple((
        ('w', 'w', 'b'),
        ('w', 'b', ' '),
        (' ', 'b', 'w'),
    ))

    ans = []
    for g in grids_with_complete_paths:
        g.set_cells(cells)
        if g.is_solved_region_puzzle():
            ans.append(g)

    # for a in ans:
    #     print('-' * 40)
    #     print(a)

    assert len(grids_with_paths) == 2110
    assert len(grids_with_complete_paths) == 184
    assert len(ans) == 1

def test_region_puzzle_5x5_3_color():
    '''This test can take 2 to 3 minutes to run.'''
    grid = puzzle.Grid(5, 5)
    grids_with_paths, grids_with_complete_paths = grid.calc_paths()
    cells = tuple((
        ('b', ' ', 'w', 'w'),
        ('r', 'r', ' ', 'w'),
        (' ', 'w', ' ', ' '),
        (' ', ' ', 'w', 'b'),
    ))

    ans = []
    for g in grids_with_complete_paths:
        g.set_cells(cells)
        if g.is_solved_region_puzzle():
            ans.append(g)

    # for a in ans:
    #     print('-' * 40)
    #     print(a)

    assert len(grids_with_paths) == 153744
    assert len(grids_with_complete_paths) == 8512
    assert len(ans) == 14
