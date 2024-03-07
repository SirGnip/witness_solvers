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

