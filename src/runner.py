import time
import cfg
import argparse
from PIL import Image, ImageGrab, ImageOps
import keyboard


def get_screenshot(idx=0, save=False):
    im = ImageGrab.grab(cfg.BBOX)
    if save:
        im.save(f'shot{idx:04d}.jpg')
    return im


def wait_for_keypress(key='x'):
    print('Waiting for keypress on', key)
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed(key):
            break


def process(im):
    im_poster = ImageOps.posterize(im, 3)
    im_poster.show()


def main(args):
    if args.sleep:
        print('Initial sleep', args.sleep)
        time.sleep(args.sleep)
    if args.path:
        with Image.open(args.path) as im:
            im.load()  # allocate storage for the image
    else:
        wait_for_keypress()
        im = get_screenshot()

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

    # print('saving')
    # img = save_screenshot()
    # print('posterizing')
    # img_poster = PIL.ImageOps.posterize(img, 2)
    # print('done')
    # img.show()
    # # x = input('do next')
    # img_poster.show()
    # print('done showing')

    # time.sleep(5)
    # spin()
