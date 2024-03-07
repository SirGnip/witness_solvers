# Basic utils for interacting with an image
from PIL import ImageGrab, ImageColor
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

def clr(name):
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

