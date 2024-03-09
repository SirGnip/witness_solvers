# Shared utilities that leverage matplotlib's plt lib
from matplotlib import pyplot as plt
import cfg


def show(img):
    '''Nice interactive image viewer with matplotlib plt module'''
    if cfg.SHOW_DEBUG_IMG:
        print(img)
        plt.imshow(img)
        plt.show()


def run_anim(img_generator, delay=1.0):
    '''Pass in generator that produces PIL.Images and draw them in sequence as an animation in the plt viewer'''
    figure, axis = plt.gcf(), plt.gca()
    axis_image = axis.imshow(next(img_generator))

    for img in img_generator:
        axis_image.set_data(img)
        figure.canvas.draw_idle()
        plt.pause(delay)
    print('Animation complete. Waiting for user to close window.')
    while True:
        plt.pause(0.2)
        if len(plt.get_fignums()) == 0:
            print('User closed window.')
            break
    print('Done')


def run_live_img(app, delay=0.1):
    '''Simple utility function that allows for simplistic app'''
    if hasattr(app, 'on_click'):
        plt.connect('button_press_event', app.on_click)
    if hasattr(app, 'on_key'):
        plt.connect('key_press_event', app.on_key)

    figure, axis = plt.gcf(), plt.gca()
    axis_image = axis.imshow(app.get_img())
    while len(plt.get_fignums()) > 0:
        axis_image.set_data(app.get_img())
        figure.canvas.draw_idle()
        if hasattr(app, 'tick'):
            app.tick()
        plt.pause(delay)
    print('Live Image done')
