# Basic utils for interacting with an image
import ctypes
from ctypes import wintypes
from PIL import Image, ImageGrab, ImageColor
import cfg


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

    def as_tuple(self):
        '''This is the ordering expected by Pillow'''
        return self.x1, self.y1, self.x2, self.y2


def get_win_location(desc) -> Rect :
    user32 = ctypes.windll.user32
    handle = user32.FindWindowW(None, desc)
    rect = wintypes.RECT()
    ff = ctypes.windll.user32.GetWindowRect(handle, ctypes.pointer(rect))
    print(ff)
    r = Rect(rect.left, rect.top, rect.right, rect.bottom)
    print(r)
    return r


def get_game_image(args) -> Image:
    if args.imgpath:
        with Image.open(args.imgpath) as img:
            print(f'Loading source image from {args.imgpath} instead of taking a screenshot')
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

