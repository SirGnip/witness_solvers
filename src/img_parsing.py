# Utilities to read an image and pull details from it (cell colors, broken links, etc)
import itertools

from PIL import Image, ImageDraw
import cfg
from typ import PointPair, CellGrid
import utils
import plot_utils
import img_proc
import puzzle


def get_puzzle_details(img: Image) -> tuple[CellGrid, set[PointPair]]:
    print('Parsing details from puzzle')
    bounding_box = find_bounding_box(img)
    puzzle_img = img.crop(bounding_box.as_tuple())
    plot_utils.show(puzzle_img)
    if isinstance(cfg.Puzzle, cfg.Triangle):
        cells = find_triangle_counts(puzzle_img)
        broken_links = set()
    else:
        cells = find_cell_colors(puzzle_img)
        if isinstance(cfg.Puzzle, cfg.Region2ColorStarter):
            broken_links = find_broken_edges(puzzle_img)
        else:
            broken_links = set()
    return cells, broken_links


def find_bounding_box(img: Image) -> img_proc.Rect:
    print('Identifying bounding box of puzzle image')
    top_points = []
    bottom_points = []
    left_points = []
    right_points = []

    drw = ImageDraw.Draw(img)

    for x in cfg.Puzzle.PANEL_BOUNDING_BOX_WHISKER_START_X:
        pixels = [img.getpixel((x, y)) for y in range(0, cfg.SCREEN_HEIGHT)]
        # Search from the top pointing down
        for y in range(len(pixels)):
            if pixels[y:y+4] == cfg.Puzzle.line_pattern():
                img_proc.cross(drw, x, y, cfg.Puzzle.DEBUG_COLOR)
                top_points.append((x, y))
                break

        # Search from the bottom pointing up
        for y in range(len(pixels), -1, -1):
            if pixels[y:y+4] == list(reversed(cfg.Puzzle.line_pattern())):
                img_proc.cross(drw, x, y+3, cfg.Puzzle.DEBUG_COLOR)
                bottom_points.append((x, y+3))
                break

    for y in cfg.Puzzle.PANEL_BOUNDING_BOX_WHISKER_START_Y:
        pixels = [img.getpixel((x, y)) for x in range(0, cfg.SCREEN_WIDTH)]
        # Search from the left pointing right
        for x in range(int(cfg.SCREEN_WIDTH*0.23), len(pixels)):  # 23% is to skip the puzzle to the left for the 1st puzzle
            if pixels[x:x+4] == cfg.Puzzle.line_pattern():
                img_proc.cross(drw, x, y, cfg.Puzzle.DEBUG_COLOR)
                left_points.append((x, y))
                break

        # Search from the right pointing left
        for x in range(len(pixels), -1, -1):
            if pixels[x:x+4] == list(reversed(cfg.Puzzle.line_pattern())):
                img_proc.cross(drw, x+3, y, cfg.Puzzle.DEBUG_COLOR)
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
            char = cfg.Puzzle.pixel_to_color_char(p)
            row.append(char)
            img_proc.cross(drw, x, y, cfg.Puzzle.DEBUG_COLOR)
        cells.append(tuple(row))
    for r in cells:
        print(r)
    plot_utils.show(img)
    return tuple(cells)


def find_triangle_counts(img: Image) -> CellGrid:
    print('Counting number of triangles')
    drw = ImageDraw.Draw(img)

    cells = []
    full_rect = img_proc.Rect.from_img(img)
    for cell_y in range(4):
        row = []
        for cell_x in range(4):
            # subdivide grid into per-cell region
            sub_rect = full_rect.divide(4, cell_x, cell_y)

            # determine the y of the triangles (50%)
            triangle_y = utils.lerp(sub_rect.y1, sub_rect.y2, 0.5)
            img_proc.cross(drw, sub_rect.x1, triangle_y, cfg.Puzzle.DEBUG_COLOR)

            # get the pixels in this sub_rect
            pixels = [img.getpixel((x, triangle_y)) for x in range(int(sub_rect.x1), int(sub_rect.x2))]

            # count the number of "starts" of the TRIANGLE_ICON color when scanning left-to-right
            tri_clr_idx = cfg.Puzzle.TRIANGLE_ICON
            tri_count = sum([1 for a, b in itertools.pairwise(pixels) if a != tri_clr_idx and b == tri_clr_idx])

            # encode triangle count as a character
            char = str(tri_count) if tri_count > 0 else ' '
            row.append(char)

        cells.append(tuple(row))
    plot_utils.show(img)
    return tuple(cells)


def find_broken_edges(img: Image) -> set[PointPair]:
    print('Parsing broken edges from puzzle image')

    edges_to_del = set()
    drw = ImageDraw.Draw(img)
    h_step = img.width / 4
    v_step = img.height / 4
    print(img)

    for edge in puzzle.Grid.enumerate_all_edges(5, 5):
        p1, p2 = edge
        mid_point_idx = utils.pt_lerp(p1, p2, 0.5)
        x, y = mid_point_idx[0] * h_step, mid_point_idx[1] * v_step
        x = min(x, img.width - 1)  # clamp to image dimension
        y = min(y, img.height - 1)  # clamp to image dimension
        p = img.getpixel((x, y))
        img_proc.cross(drw, x, y, cfg.Puzzle.DEBUG_COLOR)
        if p != cfg.Puzzle.LINE_GREEN:
            edges_to_del.add(edge)

    print('Found broken edges that will be deleted')
    for e in edges_to_del:
        print(e)

    plot_utils.show(img)

    return edges_to_del
