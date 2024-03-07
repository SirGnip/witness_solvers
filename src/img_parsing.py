# Utilities to read an image and pull details from it (cell colors, broken links, etc)
from PIL import Image
import img_proc
from typ import PointPair, CellGrid


def get_puzzle_details(img: Image) -> tuple[CellGrid, set[PointPair]]:
    print('Parsing details from puzzle')
    bounding_box = find_bounding_box(img)
    puzzle_img = img.crop(bounding_box.as_tuple())
    import plot_utils
    plot_utils.show(puzzle_img)
    cells = find_cell_colors(puzzle_img)
    broken_links = find_broken_links(puzzle_img)
    return cells, broken_links


def find_bounding_box(img: Image) -> img_proc.Rect:
    print('Identifying bounding box of puzzle image')
    r = img_proc.Rect(0, 0, 200, 200)
    print(f'Bounding box: {r}')
    return r


def find_cell_colors(img: Image) -> CellGrid:
    print('Parsing cell colors from puzzle image')
    cells = tuple(reversed((
        ('b', ' ', 'b', 'w'),
        ('w', ' ', 'w', ' '),
        (' ', 'b', ' ', ' '),
        ('w', ' ', ' ', 'w'),
    )))
    print(cells)
    return cells


def find_broken_links(img: Image) -> set[PointPair]:
    print('Parsing broken links from puzzle image')
    edges_to_del: set[PointPair] = {
        frozenset(((4, 0), (3, 0))),
        frozenset(((3, 0), (3, 1))),
        frozenset(((3, 1), (2, 1))),
        frozenset(((3, 2), (3, 3))),
        frozenset(((1, 2), (1, 3))),
    }
    return edges_to_del
