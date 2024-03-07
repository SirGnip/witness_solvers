import time
import datetime
import collections.abc
import argparse
import ctypes
from ctypes import wintypes
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


class Rect:
    '''Wrapper around a wintypes.RECT object'''
    def __init__(self, r):
        self.r: wintypes.RECT = r

    def __str__(self):
        x1, y1, x2, y2 = self.as_tuple()
        width = x2 - x1
        height = y2 - y1
        return f"{x1},{x2}-{y1},{y2} {width}x{height}"

    def as_tuple(self):
        '''This is the format supported by Pillow'''
        return self.r.left, self.r.top, self.r.right, self.r.bottom


def get_win_location(desc) -> Rect :
    user32 = ctypes.windll.user32
    handle = user32.FindWindowW(None, desc)
    rect = wintypes.RECT()
    ff = ctypes.windll.user32.GetWindowRect(handle, ctypes.pointer(rect))
    print(ff)
    print(rect)
    return Rect(rect)


def get_game_image(args) -> Image:
    if args.imgpath:
        with Image.open(args.imgpath) as img:
            print(f'Loading source image from {args.imgpath} instead of taking a screenshot')
            img.load()  # allocate storage for the image
    else:
        r = get_win_location(cfg.WINDOW_DESC)
        r.r.left += 8
        r.r.right -= 8
        r.r.top += 31
        r.r.bottom -= 8

        img = img_proc.get_screenshot(r)
        if args.save_screenshot:
            now = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
            fname = f'screenshot_{now}.jpg'
            print(f'Saving screenshot to {fname}')
            img.save(fname)
    return img


def load_grid_cache():
    '''Calculate grid paths or load from disk'''
    return {}


def preprocess_image(img: Image) -> Image:
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
        img = get_game_image(args)
        process_image(img)
    else:
        # realtime - grab screenshot from game
        while True:
            key = wait_for_keypress(['x'])
            print(f'Keypress: {key}')
            img = get_game_image(args)
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
