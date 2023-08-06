import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

import movie


class Formatter(object):
    def __init__(self, im):
        self.im = im

    def __call__(self, x, y):
        ix = round(x)
        iy = round(y)
        return f"x {ix} y {iy} val {self.im[iy, ix]}"


def get_cube(name: str) -> np.array:
    with fits.open(movie.OUT + name + ".fits") as hdus:
        cube = hdus[1].data
    return cube


def plot_img(axes, im):
    axes.format_coord = Formatter(im)
    axes.imshow(im)


cube1 = get_cube("unshifted")
cube2 = get_cube("shifted")
print(f"unshifted {cube1.shape} shifted {cube2.shape}")

im1 = cube1[-1, :, :]
im2 = cube2[-1, :, :]
#im3 = movie.shift_image(im1, -2, 6)

fig, ax = plt.subplots(ncols=2)
plot_img(ax[0], im1)
plot_img(ax[1], im2)
#plot_img(ax[1], im3)

plt.show()
