import time
import cfg
import argparse
import img_proc
from PIL import Image, ImageOps
import keyboard

import plot_utils


def wait_for_keypress(key='x'):
    print('Waiting for keypress on', key)
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed(key):
            break


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
        wait_for_keypress()
        im = img_proc.get_screenshot()

    process(im)


def cli():
    parser = argparse.ArgumentParser(prog='Solvers for The Witness')
    parser.add_argument('--path')
    parser.add_argument('--sleep', type=int)
    args = parser.parse_args()
    args.path = cfg.FNAME
    main(args)


if __name__ == '__main__':
    cli()
