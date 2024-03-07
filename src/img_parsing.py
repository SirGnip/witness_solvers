# Utilities to read an image and pull details from it (cell colors, broken links, etc)
from PIL import Image, ImageDraw
from typ import PointPair, CellGrid
import plot_utils
import img_proc


DEBUG_COLOR_IDX = 2

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
    top_points = []
    bottom_points = []
    left_points = []
    right_points = []

    drw = ImageDraw.Draw(img)

    for x in (260, 380):
        pixels = [img.getpixel((x, y)) for y in range(0, 480)]
        for y in range(len(pixels)):
            if pixels[y:y+4] == [3, 4, 4, 4]:
                img_proc.cross(drw, x, y, DEBUG_COLOR_IDX)
                top_points.append((x, y))
                break

        for y in range(len(pixels), -1, -1):
            if pixels[y:y+4] == [4, 4, 4, 3]:
                img_proc.cross(drw, x, y+3, DEBUG_COLOR_IDX)
                bottom_points.append((x, y+3))
                break

    for y in (180, 300):
        pixels = [img.getpixel((x, y)) for x in range(0, 640)]
        for x in range(150, len(pixels)):  # 150 is to skip the puzzle to the left
            if pixels[x:x+4] == [3, 4, 4, 4]:
                img_proc.cross(drw, x, y, DEBUG_COLOR_IDX)
                left_points.append((x, y))
                break

        for x in range(len(pixels), -1, -1):
            if pixels[x:x+4] == [4, 4, 4, 3]:
                img_proc.cross(drw, x+3, y, DEBUG_COLOR_IDX)
                right_points.append((x+3, y))
                break

    left = int(sum([x for x, y in left_points]) / len(left_points))
    right = int(sum([x for x, y in right_points]) / len(right_points))
    top = int(sum([y for x, y in top_points]) / len(top_points))
    bottom = int(sum([y for x, y in bottom_points]) / len(bottom_points))
    r = img_proc.Rect(left, top, right, bottom)

    # -7 is half the width of a puzzle line. Don't want to crop the image at the very outer edge of the border line,
    # but in the middle of the outer border line. This makes the math in find_cell_colors more accurate.
    r = r.grow(-7)  # shrinking bounding box

    print(f'Shrunk bounding box: {r}')
    plot_utils.show(img)
    return r


def find_cell_colors(img: Image) -> CellGrid:
    print('Parsing cell colors from puzzle image')
    print(img)
    drw = ImageDraw.Draw(img)
    h_slice = img.width / 8
    v_slice = img.height / 8

    cells = []
    for y_chunk in (1, 3, 5, 7):
        row = []
        for x_chunk in (1, 3, 5, 7):
            x = x_chunk * h_slice
            y = y_chunk * v_slice
            p = img.getpixel((x, y))
            char = ' '
            if p == 1:
                char = 'b'
            elif p == 2:
                char = 'w'
            row.append(char)
            img_proc.cross(drw, x, y, 2)
        cells.append(tuple(row))
    for r in cells:
        print(r)
    plot_utils.show(img)
    return tuple(reversed(cells))


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
