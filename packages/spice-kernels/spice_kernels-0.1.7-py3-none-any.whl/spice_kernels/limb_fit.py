from datetime import datetime
from enum import IntEnum
from typing import Optional

import astropy.io.fits as fits
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import skimage
from scipy import optimize, ndimage

from spice_kernels import get_pointing_array, get_radius
from util import mid_time

DIR = 'C:/Users/sg55/spice/data/images/'
SCALE = 1.0


class Limb(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def slice(self, img: np.array) -> np.array:
        """ Return central slice in right direction. """
        if self == self.NORTH or self == self.SOUTH:
            return img[:, img.shape[1] // 2]
        else:
            return img[img.shape[0] // 2, :]

    def find_edge(self, y_slice: np.array) -> np.array:
        """Find position of edge"""
        y = y_slice.copy()
        inverted = self == self.NORTH or self == self.WEST
        if inverted:
            y = y[::-1]

        y = ndimage.median_filter(y, 20)
        dy = y[1:] - y[:-1]
        dyf = ndimage.median_filter(dy, 40)
        zero = 0

        if np.any(np.where(dyf != 0.0)):
            non_zero = 0
            needed = 1
            found_slope = False

            for idx, val in enumerate(dyf):
                # print(f'idx {idx} val {val} non-zero {non_zero} zero {zero}')
                if val > 0:
                    non_zero += 1
                if non_zero > needed:
                    found_slope = True
                if found_slope and val == 0.0:
                    zero += 1
                if zero > needed:
                    break
        else:
            m = np.min(dy)
            idx = np.where(dy == m)[0][0]

        edge = idx - zero + 1
        if inverted:
            edge = len(y) - edge
        return edge

    def __str__(self):
        return self.name.capitalize()


class Formatter(object):
    def __init__(self, im):
        self.im = im

    def __call__(self, x, y):
        z = self.im.get_array()[int(y), int(x)]
        return 'x={:.01f}, y={:.01f}, z={:.01f}'.format(x, y, z)


def in_circle(x: float, y: float, x0: float, y0: float, r2: float) -> bool:
    return ((x - x0) * (x - x0) + (y - y0) * (y - y0)) < r2


def cost(guess: np.ndarray, *args) -> float:
    img, xmin, xmax, ymin, ymax, r0, threshold = args
    x0 = guess[0] * SCALE
    y0 = guess[1] * SCALE
    if r0 is None:
        r0 = guess[2]

    score = 0.0
    r2 = r0 * r0
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            val = img[y, x]
            if in_circle(x, y, x0, y0, r2):
                if val < threshold:
                    score += val
                else:
                    score -= val

    #print(f'x {x0:.2f} y {y0:.2f} r {r0:.2f} s {score}')
    return score


class Data:
    def __init__(self, file: str, limb: Limb,
                 xguess: float, yguess: float, rguess: float = -1,  image: int = 5,
                 result: np.array = None,
                 xmin: int = 0, xmax: Optional[int] = None,
                 ymin: int = 0, ymax: Optional[int] = None, cut: float = -1.0):
        self.file = file
        self.limb = limb
        self.guess = np.array([xguess, yguess, rguess])
        self.image = image,
        self.result = result
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.cut = cut

    def analyse_disk(self, img: np.array, x0: float, y0: float, r: float) -> float:
        r2 = r * r
        disk = np.array([img[y, x]
                        for y in range(self.ymin, self.ymax)
                        for x in range(self.xmin, self.xmax) if in_circle(x, y, x0, y0, r2)])
        median = np.median(disk)
        return median


class FitData:
    def __init__(self, data: Data, axes, fit: bool = False,
                 percent: int = 100, display_fit_img=False):

        self.data = data
        self.fit = fit
        self.percent = percent
        self.radius = None
        self.median = None
        self.threshold = None
        self.centre = None
        self.start = None
        self.end = None
        self.fit_img = display_fit_img
        self.xf = 0.0
        self.yf = 0.0
        self.rf = 0.0
        self.scx = 0.0
        self.scy = 0.0
        self.offx = 0.0
        self.offy = 0.0
        self.axes = axes
        if self.axes is not None:
            self.axes.set_title(str(self.data.limb))

    def process(self) -> None:
        print('Process file {}'.format(self.data.file))
        if self.data.file.endswith('fits'):
            self.process_fits(image=self.data.image)
        else:
            self.process_img()

    def process_fits(self, image: int = 5) -> None:
        # img = np.log(img, where=(img > 0))
        img = self.get_fits_image(image)
        self.do_fit(img)

        if self.data.result is not None and self.axes is not None:
            self.plot_result()

    def process_img(self) -> None:
        rgb = mpimg.imread(self.file)
        red = rgb[:, :, 0]
        img = np.asarray(red, float)
        self.do_fit(img)

    def get_fits_image(self, image: int = 5) -> np.ndarray:
        with fits.open(self.data.file) as hdu:
            header = hdu[0].header
            self.start = datetime.fromisoformat(header['DATE-OBS'])
            self.end = datetime.fromisoformat(header['DATE-END'])
            cube = hdu[1].data

        ref_time = mid_time(self.start, self.end)
        self.radius = get_radius(ref_time)
        print(f'start {self.start:%Y-%m-%d %H:%M} end {self.end:%Y-%m-%d %H:%M} '
              f'solar radius {self.radius:.2f}')

        # This can end up with a degenerate dimension, why?
        img = cube[image, :, :] if len(cube.shape) == 3 else cube
        if len(img.shape) == 3:
            img = img[0, :, :]
        self.analyse_image(img)
        #img = ndimage.median_filter(img, 5)
        #im2 = img / (img.max() - img.min())
        #im3 = skimage.img_as_ubyte(im2)
        #edges = cv2.Canny(ndimage.sobel(im3, 1), ndimage.sobel(im3, 0))
        return img

    def analyse_image(self, img: np.ndarray) -> None:
        if self.data.xmax is None:
            self.data.xmax = img.shape[1]
        if self.data.ymax is None:
            self.data.ymax = img.shape[0]

        self.centre = (img.shape[1]/2.0, img.shape[0]/2.0)
        self.median = self.data.analyse_disk(img, self.data.guess[0], self.data.guess[1],
                                             self.radius)
        self.threshold = self.data.cut if self.data.cut > 0 else self.median * (self.percent / 100.)
        print(f'image median {self.median:.2f} cut threshold {self.threshold:.2f}')

    def do_fit(self, img: np.ndarray) -> None:

        if self.fit:
            fit_img = self.apply_fit(img)
            show_img = fit_img if self.fit_img else img
        else:
            show_img = img

        if self.axes is not None:
            im = self.axes.imshow(show_img)
            self.axes.invert_yaxis()
            self.axes.format_coord = Formatter(im)

    def apply_fit(self, img: np.ndarray) -> np.ndarray:
        if self.data.guess[2] < 0:
            print("Using calculated radius")
            guess = np.array([self.data.guess[0], self.data.guess[1]])
            radius = self.radius
        else:
            print("Varying radius")
            guess = self.data.guess
            radius = None

        # The minimize default method on this data is BFGS.
        args = (img, self.data.xmin, self.data.xmax, self.data.ymin, self.data.ymax,
                radius, self.threshold)
        #res = optimize.minimize(cost, guess, args, jac=deriv, tol=1.0)
        res = optimize.minimize(cost, guess, args, method='Nelder-Mead')
        print(str(res))
        self.data.result = res.x

        median = self.data.analyse_disk(img, self.data.result[0], self.data.result[1], radius)
        print(f'median of fitted disk {median}')
        self.calculate_result()
        return img

    def calculate_result(self):
        self.xf = self.data.result[0] * SCALE
        self.yf = self.data.result[1] * SCALE
        self.rf = self.data.result[2] if len(self.data.result) > 2 else self.radius
        print(f'{str(self.data.limb)}: x {self.xf:.2f} y {self.yf:.2f} r {self.rf:.2f}')

        # Add spacecraft pointing.
        _, lon, lat = get_pointing_array(self.start, self.end)
        av_lon = np.median(lon)
        av_lat = np.median(lat)
        self.scx = av_lon + self.data.result[0]
        self.scy = av_lat + self.data.result[1]
        print(f's/c lon avg {av_lon: .2f} min {np.min(lon): .2f} max {np.max(lon): .2f}')
        print(f's/c lat avg {av_lat: .2f} min {np.min(lat): .2f} max {np.max(lat): .2f}')
        self.offx = self.centre[0] - self.scx
        self.offy = self.centre[1] - self.scy
        print(f'offset x {self.offx:.2f} y {self.offy:.2f}\n')

    def plot_result(self):

        # Plot the fitted circle.
        circle = plt.Circle((self.xf, self.yf), self.rf, fill=False, color='m')
        self.axes.add_artist(circle)

        # Add spacecraft pointing.
        self.axes.plot(self.scx, self.scy, marker='*', color='r', label='Spacecraft')

        # Add the SPICE optical centre.
        self.axes.plot(self.centre[0], self.centre[1],
                       marker='*', color='y', label='SPICE')

    def plot_slice(self):
        img = self.get_fits_image(self.data.image)
        y = self.data.limb.slice(img)
        self.axes.plot(y, label='Intensity')
        self.axes.axhline(self.median, color='r', label='Disk median')
        self.axes.axhline(self.threshold, color='m', label='Threshold')
        #self.axes.axhline(self.threshold, color='m', label=f'Cut at {self.percent}%')
        #edge = self.data.limb.find_edge(y)
        #print(f'edge at {edge}')
        #self.axes.axhline(y[edge], color='g', label=f'Edge algorithm')


fig, ax = plt.subplots(2, 2)
fig.subplots_adjust(wspace=-0.4, hspace=0.4)
#fig.subplots_adjust(wspace=0.4, hspace=0.4)

#fit_png(DIR + 'North_Pole_OVI.jpg', ax[0, 0], 220., 500., 400., yrange=[40, 375], fit=True)
#fit_png(DIR + 'West_Limb_OVI.jpg', ax[0, 1], -300., 350., 600., yrange=[95, 565], fit=True)
#fit_png(DIR + 'South_Pole_CIII.jpg', ax[1, 0], 250., -150., 600., yrange=[150,420], fit=True)
#fit_png(DIR + 'East_Limb_OVI.jpg', ax[1, 1], 750., 400., 600., yrange=[150, 620], fit=True)

disp_fit = False
do_fit = True
cut = -1.0
percent = 100

# NECP files.
"""
image = 5
north = Data(DIR+'cube_12583688_28_0_7FlightRSCSOU70_0_pixrespv1_images_rescale.fits',
             Limb.NORTH, xguess=357., yguess=-1312., image=image,
             #result=np.array([360.97, -1301.20, 1700.35]),
             ymax=400, cut=cut) #cut=5000.0)

south = Data(DIR+'cube_12583689_28_0_7FlightRSCSOU70_0_pixrespv1_images_rescale.fits',
             Limb.SOUTH, xguess=319., yguess=2056., image=image,
             #result=np.array([325.88, 2046.21, 1701.45]),
             ymin=300, cut=cut) #cut=5700.0)

west = Data(DIR+'cube_12583690_28_0_7FlightRSCSOU70_0_pixrespv1_images_rescale.fits',
            Limb.WEST, xguess=-1354., yguess=363., image=image,
            #result=np.array([-1348.91, 366.23, 1702.56]),
            xmax=500, cut=cut) #cut=8610.0)

east = Data(DIR+'cube_12583691_32_0_7FlightRSCSOU70_0_pixrespv1_images_rescale.fits',
            Limb.EAST, xguess=2010., yguess=361., image=image,
            #result=np.array([2005.08, 357.56, 1703.71]),
            xmin=250, cut=cut) #cut=8140.0)

"""
# Cruise phase files.
image = 0
north = Data(DIR+'cube_16777425_18_0_11RSCW1b_0_pixrespv1_images_rescale.fits',
             Limb.NORTH, xguess=351., yguess=-1416., image=image,
             result=np.array([355.67, -1415.03, 1846.98]),
             ymax=475, cut=cut) #cut=3550.0)

south = Data(DIR+'cube_16777426_19_0_11RSCW1b_0_pixrespv1_images_rescale.fits',
             Limb.SOUTH, xguess=316., yguess=2246., image=2,
             result=np.array([327.38, 2234.20, 1846.55]),
             ymin=300, cut=cut) #cut=3950.0)

west = Data(DIR+'cube_16777429_19_0_11RSCW1b_0_pixrespv1_images_rescale.fits',
            Limb.WEST, xguess=-1492., yguess=415., image=2,
            result=np.array([-1488.16, 405.04, 1846.11]),
            xmax=375, cut=cut) #cut=5140.0)

east = Data(DIR+'cube_16777430_20_0_11RSCW1b_0_pixrespv1_images_rescale.fits',
            Limb.EAST, xguess=2169., yguess=409., image=image,
            result=np.array([2168.67, 409.87, 1845.67]),
            xmin=280, cut=cut) #cut=17330.0)

nf = FitData(north, ax[0, 0], fit=do_fit, percent=percent, display_fit_img=disp_fit)
sf = FitData(south, ax[1, 0], fit=do_fit, percent=percent, display_fit_img=disp_fit)
wf = FitData(west, ax[0, 1], fit=do_fit, percent=percent, display_fit_img=disp_fit)
ef = FitData(east, ax[1, 1], fit=do_fit, percent=percent, display_fit_img=disp_fit)

with open(DIR+'fit_results.txt', 'w') as file:
    for f in (nf, sf, wf, ef):
    #for f in (nf,):
        #for percent in range(100, 50, -10):
        for pct in (percent,):
            f.percent = pct
            f.process()
            file.write(f'{str(f.data.limb):<5} {f.percent:>3} {f.offx:.2f} {f.offy:.2f}\n')

"""
FitData(north, ax[0, 0], percent=percent).plot_slice()
FitData(south, ax[1, 0], percent=percent).plot_slice()
FitData(west, ax[0, 1], percent=percent).plot_slice()
FitData(east, ax[1, 1], percent=percent).plot_slice()
"""

handles, labels = ax[1, 1].get_legend_handles_labels()
fig.legend(handles, labels, loc='center right')
plt.show(block=True)
