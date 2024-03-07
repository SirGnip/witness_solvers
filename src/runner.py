import time
import datetime
import collections.abc
import argparse
from PIL import Image, ImageFilter
import keyboard
import cfg
import img_proc
import plot_utils


def wait_for_keypress(keys: list[str]) -> str:
    print('Waiting for keypress on', keys)
    while True:
        time.sleep(0.1)
        for key in keys:
            if keyboard.is_pressed(key):
                return key

def load_grid_cache():
    '''Calculate grid paths or load from disk'''
    return {}


def preprocess_image(img: Image) -> Image:
    '''Reduce the image down to a known list of colors to make parsing easier'''
    print('Doing pre-processing on the image')
    palimage = Image.new('P', (16, 16))
    palimage.putpalette(cfg.PALETTE_COLORS)
    new_img = img.quantize(colors=len(cfg.PALETTE_COLORS) / 3, palette=palimage, dither=Image.Dither.NONE)
    new_img = new_img.filter(ImageFilter.ModeFilter(5))
    return new_img


def process_image(img):
    img = preprocess_image(img)
    plot_utils.show(img)

    # parse image
    print('Parse image and populate the cells/edges')

    # solve puzzle
    print('Filter results down to the solution')

    # display answer
    print('Puzzle answer')


def main(args):
    grid_cache = load_grid_cache()

    if args.imgpath:
        # use provided image file for one iteration
        img = img_proc.get_game_image(args)
        process_image(img)
    else:
        # realtime - grab screenshot from game
        while True:
            key = wait_for_keypress(['x'])
            print(f'Keypress: {key}')
            img = img_proc.get_game_image(args)
            print(img)
            process_image(img)


def cli():
    parser = argparse.ArgumentParser(prog='Solvers for The Witness')
    parser.add_argument('--imgpath', help='Use the provided file instead of taking a screenshot')
    parser.add_argument('--save-screenshot', action='store_true', help='Save screenshot to a file before processing')
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    cli()
