import time
import cfg
import argparse
import ctypes
from ctypes import wintypes
from PIL import Image, ImageOps
import keyboard
import img_proc
import plot_utils


def wait_for_keypress(key='x'):
    print('Waiting for keypress on', key)
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed(key):
            break

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


def process(im):
    im_poster = ImageOps.posterize(im, 3)
    plot_utils.show(im_poster)


def main(args):
    if args.sleep:
        print('Initial sleep', args.sleep)
        time.sleep(args.sleep)
    if args.path:
        with Image.open(args.path) as im:
            im.load()  # allocate storage for the image
    else:
        while True:
            wait_for_keypress()
            r = get_win_location(cfg.WINDOW_DESC)
            r.r.left += 8
            r.r.right -= 8
            r.r.top += 31
            r.r.bottom -= 8

            im = img_proc.get_screenshot(r)
            print(im)
            # process(im)


def cli():
    parser = argparse.ArgumentParser(prog='Solvers for The Witness')
    parser.add_argument('--path')
    parser.add_argument('--sleep', type=int)
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    cli()
