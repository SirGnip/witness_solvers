# File that contains a bunch of temp experimental scripts.
import sys
from PIL.Image import Dither
from PIL import Image, ImageDraw, ImageFilter
from matplotlib.backend_bases import MouseButton
import cfg
import img_proc
import plot_utils


FILE = sys.argv[1]
print(f'Reading from {FILE}')


def getf():
    with Image.open(FILE) as img:
        img.load()  # allocate storage for the image
    return img

def interactive():
    '''very minimal way to do quasi-interactive interactions with an image'''
    img = getf()
    img.show()
    drw = ImageDraw.Draw(img, 'RGBA')  # RGBA

    while True:
        resp = input('Enter x y: ')
        if resp.strip() == '':
            break
        x, y = [int(v) for v in resp.split()]
        img_proc.cross(drw, x, y, img_proc.CLR.white)
        img.show()

def color_reduce():
    img = getf()
    print(img, img.format, img.size, img.mode)

    for c in (32, 40, 50, 64):
        print(c)
        # 64 colors is pretty good.
        img2 = img.convert('P', palette=Image.ADAPTIVE, colors=c)  # https://stackoverflow.com/a/1074680
        img2 = img2.convert('RGB')
        plot_utils.show(img2)

def palletize():
    im = getf()
    p2 = (
        0,0,0,
        128,128,128,
        255,255,255,
        128,0,0,
        0,128,0,
        0,255,0,
        0,0,128,
    )
    # original image
    plot_utils.show(im)

    # quantize to palette
    palimage = Image.new('P', (16, 16))
    palimage.putpalette(palette_colors)
    im = im.quantize(colors=len(palette_colors)/3, palette=palimage, dither=Dither.NONE)
    plot_utils.show(im)

    # force another palette on it
    im.putpalette(p2)
    plot_utils.show(im)

def demo_anim():
    '''Demo the 'do_anim()' function'''
    def make_img():
        img = getf()
        x = 0
        drw = ImageDraw.Draw(img, 'RGBA')  # RGBA
        while x < 400:
            img_proc.cross(drw, x, 100)
            x += 25
            yield img
    plot_utils.run_anim(make_img(), 0.5)

def demo_live():
    '''Demonstrate how to use the live image `run_live_img()` function.'''
    class LiveImgApp:
        def __init__(self):
            self.img = getf()
            self.drw = ImageDraw.Draw(self.img, 'RGBA')  # RGBA
        def get_img(self) -> Image:
            return self.img
        def on_click(self, event):  # optional
            img_proc.cross(self.drw, event.xdata, event.ydata, img_proc.CLR.white)
        def on_key(self, event):  # optional
            print('key', event.key)
        def tick(self):  # optional
            pass
    plot_utils.run_live_img(LiveImgApp())

def color_avg():
    '''Click a pixel and get average pixel values around it'''
    class LiveImgApp:
        def __init__(self):
            self.img = getf()
        def get_img(self) -> Image:
            return self.img
        def on_click(self, event):
            x, y = int(event.xdata), int(event.ydata)
            pixels = []
            for y in range(y - 2, y + 3):
                for x in range(x - 2, x + 3):
                    pixels.append(self.img.getpixel((x, y)))

            r_avg = sum([p[0] for p in pixels]) / len(pixels)
            g_avg = sum([p[1] for p in pixels]) / len(pixels)
            b_avg = sum([p[2] for p in pixels]) / len(pixels)
            print(r_avg, g_avg, b_avg)

    print('Click on a pixel and an average of the 25 pixels around the click point will be printed out...')
    plot_utils.run_live_img(LiveImgApp())

def detect_edges_app():
    '''Click a pixel and search down the image until you find edge of panel'''
    class LiveImgApp:
        def __init__(self):
            self.img = getf()
            palimage = Image.new('P', (16, 16))
            palimage.putpalette(cfg.PALETTE_COLORS)
            self.img = self.img.quantize(colors=len(cfg.PALETTE_COLORS) / 3, palette=palimage, dither=Dither.NONE)
            self.img = self.img.filter(ImageFilter.ModeFilter(5))
            self.drw = ImageDraw.Draw(self.img)
        def get_img(self) -> Image:
            return self.img
        def on_click(self, event):
            if event.button == MouseButton.RIGHT:
                return
            x, y = int(event.xdata), int(event.ydata)
            while y < 1000:
                p = self.img.getpixel((x, y))
                print(x, y, p)
                if p == 4:
                    print('found', x, y)
                    img_proc.cross(self.drw, x, y, cfg.DEBUG_COLOR_IDX)
                    break
                else:
                    y += 1

    plot_utils.run_live_img(LiveImgApp())

if __name__ == '__main__':
    # interactive()
    # color_reduce()
    # demo_anim()
    # demo_live()

    # palletize()
    # color_avg()
    detect_edges_app()
