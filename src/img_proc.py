# Basic utils for interacting with an image
import datetime
import ctypes
from typing import Self
from ctypes import wintypes
from PIL import Image, ImageGrab, ImageColor
import cfg
import utils


class Clr:
    '''Convenience for specifying color'''
    def __getattr__(self, key):
        return ImageColor.getrgb(key)

CLR = Clr()


def get_screenshot(bounding_box=None, idx=0, save=False):
    im = ImageGrab.grab(bounding_box.as_tuple())
    if save:
        im.save(f'shot{idx:04d}.jpg')
    return im


class Rect:
    '''Wrapper around a wintypes.RECT object'''
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return f"{self.x1},{self.x2}-{self.y1},{self.y2} {width}x{height}"

    @staticmethod
    def from_img(img: Image):
        return Rect(0, 0, img.width, img.height)

    def as_tuple(self):
        '''This is the ordering expected by Pillow'''
        return self.x1, self.y1, self.x2, self.y2

    def grow(self, delta):
        return Rect(
            self.x1-delta,
            self.y1-delta,
            self.x2+delta,
            self.y2+delta)

    def divide(self, divs: int, cell_x: int, cell_y: int) -> Self:
        fraction = 1/divs
        r = Rect(
            utils.lerp(self.x1, self.x2, cell_x * fraction),
            utils.lerp(self.y1, self.y2, cell_y * fraction),
            utils.lerp(self.x1, self.x2, (cell_x + 1) * fraction),
            utils.lerp(self.y1, self.y2, (cell_y + 1) * fraction),
        )
        return r


def get_win_location(desc) -> Rect :
    user32 = ctypes.windll.user32
    handle = user32.FindWindowW(None, desc)
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(handle, ctypes.pointer(rect))
    r = Rect(rect.left, rect.top, rect.right, rect.bottom)
    return r


def get_game_image(args) -> Image:
    if args.imgpath:
        with Image.open(args.imgpath) as img:
            print(f'Loading source image from {args.imgpath}, and not taking a screenshot of the game.')
            img.load()  # allocate storage for the image
    else:
        r = get_win_location(cfg.WINDOW_DESC)
        r.x1 += 8
        r.x2 -= 8
        r.y1 += 31
        r.y2 -= 8

        img = get_screenshot(r)
        if args.save_screenshot:
            now = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
            fname = f'screenshot_{now}.jpg'
            print(f'Saving screenshot to {fname}')
            img.save(fname)
    return img


def clr(name):
    '''Convenience function to get a color by name'''
    return ImageColor.getrgb(name)

def alpha(color, a):
    return tuple(list(color) + [a])

def cross(drw, x, y, color=CLR.red, size=20):
    half = size/2
    drw.line(((x, y-half), (x, y+half)), fill=color)
    drw.line(((x-half, y), (x+half, y)), fill=color)

def cir(drw, x, y, color=CLR.red, size=10):
    half = size/2
    drw.ellipse(( (x-half, y-half), (x+half, y+half)), color)

