import time
import argparse
from PIL import Image, ImageFilter
import keyboard
import cfg
import puzzle
import img_proc
import img_parsing
import plot_utils



def wait_for_keypress(keys: list[str]) -> str:
    print('Waiting for keypress on', keys)
    while True:
        time.sleep(0.1)
        for key in keys:
            if keyboard.is_pressed(key):
                return key

def load_initial_grid_cache(width, height):
    '''Calculate grid paths or load from disk'''
    print(f'Cache initial path info for grid {width}x{height}')
    grid = puzzle.Grid(width, height)
    grids_with_paths, grids_with_complete_paths = grid.calc_paths('grid_5x5.cache.pickle')
    return grid, grids_with_paths, grids_with_complete_paths


def preprocess_image(img: Image) -> Image:
    '''Reduce the image down to a known list of colors to make parsing easier'''
    print('Doing pre-processing on the image')
    palimage = Image.new('P', (16, 16))
    palimage.putpalette(cfg.Puzzle.palette)
    new_img = img.quantize(colors=len(cfg.Puzzle.palette) / 3, palette=palimage, dither=Image.Dither.NONE)
    new_img = new_img.filter(ImageFilter.ModeFilter(5))
    return new_img


def process_image(img, grid, grids_with_complete_paths):
    assert img.size == (640, 480)
    plot_utils.show(img)

    img = preprocess_image(img)
    plot_utils.show(img)

    # parse image
    print('Parse image to get info from it and update the grid with the found cells and edges')
    cells, broken_edges = img_parsing.get_puzzle_details(img)

    # print out grid for confirmation that processing worked
    grid.set_cells(cells)
    grid.delete_edges_from_path(broken_edges)
    print(grid)

    # solve puzzle
    print(f'Given {len(grids_with_complete_paths)} full paths, filter results down to the solutions that match the constraints.')
    answers = []
    for idx, grid_with_path in enumerate(grids_with_complete_paths):
        grid_with_path.set_cells(cells)
        if grid_with_path.is_solved_region_puzzle(broken_edges):
            print(f'========== Puzzle #{idx} of {len(grids_with_complete_paths)} is a solution')
            print(grid_with_path)
            answers.append(grid_with_path)
    print(f'Found {len(answers)} answers')


def main(args):
    grid, grids_with_paths, grids_with_complete_paths = load_initial_grid_cache(5, 5)

    if args.imgpath:
        cfg.config_factory(args.puzzle_type)
        # use specified image file for one iteration
        img = img_proc.get_game_image(args)
        process_image(img, grid, grids_with_complete_paths)
    else:
        # realtime - grab screenshot from running game
        while True:
            key = wait_for_keypress(['z', 'x'])
            print(f'Keypress: {key}')

            key_map = {'z': 'Starter2Region', 'x': 'TripletRegion'}
            cfg.config_factory(key_map[key])

            img = img_proc.get_game_image(args)
            print(img)
            process_image(img, grid, grids_with_complete_paths)


def cli():
    parser = argparse.ArgumentParser(prog='Solvers for The Witness')
    parser.add_argument('--imgpath', help='Use the provided file instead of taking a screenshot')
    parser.add_argument('--puzzle-type', choices=cfg.PUZZLE_TYPES, help='Type of puzzle to solve')
    parser.add_argument('--save-screenshot', action='store_true', help='Save screenshot to a file before processing')
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    cli()
