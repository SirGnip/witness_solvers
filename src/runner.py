import time
import argparse
import copy
import traceback
from PIL import Image, ImageFilter
import keyboard
import cfg
import puzzle
import img_proc
import img_parsing
import plot_utils
from utils import timer


def wait_for_keypress(keys: list[str]) -> str:
    print('Waiting for keypress on', keys)
    while True:
        time.sleep(0.05)
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
    with timer('3 preproc'):
        assert img.size == (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
        plot_utils.show(img)

        img = preprocess_image(img)
        plot_utils.show(img)

    # parse image
    with timer('3 details'):
        print('Parse image to get info from it and update the grid with the found cells and edges')
        cells, broken_edges = img_parsing.get_puzzle_details(img)

    # print out grid for confirmation that processing worked
    with timer('3 set cells'):
        grid.set_cells(cells)
    with timer('3 del edges'):
        print('Grids edges:', len(grid.edges))
        for e in grid.edges:
            print(e)
        print('broken edges that will be deleted:')
        for e in broken_edges:
            print(e)
        grid.delete_edges_from_path(broken_edges)
        print(grid)

    # solve puzzle
    with timer('3 solve'):
        find_solutions(grids_with_complete_paths, broken_edges, cells)


def find_solutions(grids_with_complete_paths, broken_edges, cells):
    print(f'Given {len(grids_with_complete_paths)} full paths, filter results down to the solutions that match the constraints.')
    answers = []
    is_tri_puzzle = isinstance(cfg.Puzzle, cfg.Triangle)
    for idx, grid_with_path in enumerate(grids_with_complete_paths):
        grid_with_path.set_cells(cells)
        if is_tri_puzzle:
            is_solved = grid_with_path.is_solved_tri_puzzle()
        else:
            is_solved = grid_with_path.is_solved_region_puzzle(broken_edges)
        if is_solved:
            print(f'========== Puzzle #{idx} of {len(grids_with_complete_paths)} is a solution')
            print(grid_with_path)
            answers.append(grid_with_path)
            if not cfg.SHOW_DEBUG_IMG:
                break  # only show first answer for speed
    print(f'Found {len(answers)} answers')
    return answers


def main(args):
    if args.imgpath is not None:
        if args.puzzle_type is None:
            raise Exception('Must provide --puzzle-type if you provide --imgpath')

    with timer('Initial load') as t:
        grid, grids_with_paths, grids_with_complete_paths = load_initial_grid_cache(5, 5)

    if args.imgpath:
        cfg.config_factory(args.puzzle_type)
        # use specified image file for one iteration
        with timer('game img'):
            img = img_proc.get_game_image(args)
        with timer('proc img'):
            process_image(img, grid, grids_with_complete_paths)
    else:
        # realtime - grab screenshot from running game
        while True:
            key = wait_for_keypress(['1', '2', '3', '0'])
            print(f'Keypress: {key}')

            try:
                with timer('1 Total'):
                    key_map = {'1': 'Starter2Region', '2': 'TripletRegion', '3': 'Triangle', '0': 'NoOp'}
                    cfg.config_factory(key_map[key])

                    with timer('2 get img'):
                        img = img_proc.get_game_image(args)
                    print(img)
                    if cfg.Puzzle is None:
                        print('Puzzle type was NoOp, Skipping puzzle solving.')
                        num_shots = 14
                        for i in range(1, num_shots + 1):
                            print(f'#{i}/{num_shots} screenshots...')
                            img_proc.get_game_image(args)
                            time.sleep(1.0)  # screenshots are named with per-second timestamps
                        continue
                    with timer('2 proc img'):
                        cur_grid = copy.deepcopy(grid)  # grid is muted inside process_image
                        process_image(img, cur_grid, grids_with_complete_paths)
            except Exception as exc:
                print(''.join(traceback.format_exception(exc)))
                print()
                time.sleep(0.3)  # delay a bit otherwise the keypress will be detected multiple times

def cli():
    parser = argparse.ArgumentParser(prog='Solvers for The Witness')
    parser.add_argument('--imgpath', help='Use the provided file instead of taking a screenshot')
    parser.add_argument('--puzzle-type', choices=cfg.PUZZLE_TYPES, help='Type of puzzle to solve')
    parser.add_argument('--save-screenshot', action='store_true', help='Save screenshot to a file before processing')
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    with timer('Total'):
        cli()

