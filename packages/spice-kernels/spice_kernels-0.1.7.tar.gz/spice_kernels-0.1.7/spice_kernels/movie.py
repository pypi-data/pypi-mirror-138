import os
from typing import List, Tuple

import cv2
import numpy as np
import cmapy
from astropy.io import fits
from numpy.lib.index_tricks import IndexExpression
from scipy.ndimage import median_filter

import spice_kernels as sk

DIR = 'C:/Users/sg55/spice/python'
OUT = 'C:/Users/sg55/temp/'
OBSID = 33554559
STUDY_ID = 30
LW_Y = 1.0587
LW_L = 0.864
LAMBDA_START = 1146
LAMBDA_END = 1178
HEAT = cmapy.cmap('gist_heat')


def to_lambda_pix(arcsec: float) -> float:
    return arcsec / LW_L


def to_y_pix(arcsec: float) -> float:
    return arcsec / LW_Y


def get_slice(i: int, j: int) -> IndexExpression:
    if i < 0 and j < 0:
        s = np.s_[:j, :i]
    elif i < 0:
        s = np.s_[j:, :i]
    elif j < 0:
        s = np.s_[:j, i:]
    else:
        s = np.s_[j:, i:]
    return s


def cut_image(a: np.array, i: int, j: int) -> np.array:
    """Cut the given offsets from the image."""
    #if i < 0 and j < 0:
    #    b = a[:j, :i]
    #elif i < 0:
    #    b = a[j:, :i]
    #elif j < 0:
    #    b = a[:j, i:]
    #else:
    #    b = a[j:, i:]
    #return b
    return a[get_slice(i, j)]


def shift_image(a: np.array, i: int, j: int, cut: bool = True) -> np.array:
    a0 = np.roll(a, j, axis=0)
    a1 = np.roll(a0, i, axis=1)
    return cut_image(a1, i, j) if cut else a1


def find_offset_image(a: np.array, b: np.array, pixels: int = 5) -> Tuple[int, int]:
    """Find where the difference between frames is minimum."""
    indices = np.array(range(-pixels, pixels+1))
    size = len(indices)
    diff = np.empty((size, size))

    for i in indices:
        for j in indices:
            aa = cut_image(a, i, j)
            bb = shift_image(b, i, j)
            cc = aa - bb
            d = np.sum(np.abs(cc)) / cc.size
            diff[j+pixels, i+pixels] = d
            #print(f"i {i} j {j} n {bb.size} diff {d} bb {bb} cc {cc}")
    #print(f"diff {diff}")
    loc_min = np.unravel_index(np.argmin(diff), diff.shape)
    return loc_min[0] - pixels, loc_min[1] - pixels


def find_offsets(cube: np.array) -> Tuple[np.array, np.array]:
    """Find horizontal and vertical offsets from first frame of cube."""

    frames = cube.shape[0]
    h_off = np.zeros(frames, dtype=np.int)
    v_off = np.zeros(frames, dtype=np.int)
    h_cum = np.zeros(frames, dtype=np.int)
    v_cum = np.zeros(frames, dtype=np.int)

    for i, frame in enumerate(cube):
        if i == 0:
            h_off[i] = v_off[i] = 0
            #first_frame = frame
        else:
            v_off[i], h_off[i] = find_offset_image(frame, last_frame)
            h_cum[i] += h_cum[i-1] + h_off[i]
            v_cum[i] += v_cum[i-1] + v_off[i]
        last_frame = frame
        print(f"frame {i} hoff {h_off[i]} voff {v_off[i]} hcum {h_cum[i]} vcum {v_cum[i]}")

    return h_cum, v_cum


def shift_with_offsets(cube: np.array, l_off: np.array, y_off: np.array) -> np.array:
    """Shift cube with given offsets (in pixels)."""

    # FIXME: diagnostics only
    minl, maxl = np.min(l_off), np.max(l_off)
    miny, maxy = np.min(y_off), np.max(y_off)
    print(f'lambda {minl} to {maxl} y {miny} to {maxy}')

    new_cube = np.full_like(cube, np.median(cube))
    for i, frame in enumerate(cube):
        x = l_off[i]
        y = y_off[i]
        shifted = shift_image(frame, -x, -y)
        shape = shifted.shape
        print(f"cube {cube.shape} image {shape} x {x} y {y}")
        slice = get_slice(x, y)
        print(f"slice {slice}")
        slice2 = np.s_[i:i+1, slice[0], slice[1]]
        print(f"slice {slice}")
        new_cube[slice2] = shifted
        print(f"slice2 {slice2}")
        #new_cube[i, y:shape[0] + y, x:shape[1] + x] = shifted
    return new_cube


def shift_from_jitter(cube: np.array) -> np.array:
    """Shift cube from observed jitter."""
    l_off, y_off = find_offsets(cube)
    return shift_with_offsets(cube, l_off, y_off)


def shift_with_times(cube: np.array, times: List[str]) -> np.array:
    """Shift cube by offsets in calculated pointing."""

    frames = len(times)
    lon = np.zeros(frames)
    lat = np.zeros(frames)

    for i, time in enumerate(times):
        #lon, lat = sk.get_sc_lon_lat(time)
        lon[i], lat[i] = sk.get_lon_lat(time, correct_aberration=False)

    lon -= np.median(lon)
    lat -= np.median(lat)

    l_off = np.array([round(to_lambda_pix(x)) for x in lon])
    y_off = np.array([round(to_y_pix(x)) for x in lat])

    return shift_with_offsets(cube, l_off, y_off)


def make_video(cube: np.array, name: str):
    frames = cube.shape[0]
    height = cube.shape[1]
    width = cube.shape[2]
    print(f'frames {frames} height {height} width {width}')

    fps = 10.0
    fourcc = cv2.VideoWriter_fourcc(*'MP42')
    file = os.path.join(OUT, name)
    print(f'Writing movie to {file}')
    video = cv2.VideoWriter(file, fourcc, fps, (width, height))

    for frame in cube:
        img = frame.astype('uint8')
        img = cv2.applyColorMap(img, HEAT)
        video.write(img)

    video.release()


def write_fits(name: str, hdus):
    fname = OUT+name
    print(f"Writing {fname}")
    hdus.writeto(fname, overwrite=True)


def process_file(hdus):
    hdus.info()
    hdr = hdus[0].header
    exp_time = float(hdr['exposure'])
    offset = exp_time/2
    cube = hdus[1].data

    window = cube[:, :, LAMBDA_START:LAMBDA_END]
    smoothed = median_filter(window, size=2)

    print()
    print(f'exp_time {exp_time} cube {cube.shape} window {window.shape}')
    acq_time = hdus[3].data['acquisitionTime']
    print(f'{len(acq_time)} acquisition times from {acq_time[0]}')
    times_uncorr = [sk.to_date(t, offset=offset) for t in acq_time]
    times_corr = [sk.correlate(t) for t in times_uncorr]
    print(f'correlated start with offset {sk.to_utc_string(times_corr[0])}')
    print(f'difference {(times_corr[0] - times_uncorr[0])} offset {offset}')

    #find_offsets(window)
    #win2 = shift_with_times(window, times_corr)
    shifted = shift_from_jitter(smoothed)

    #make_video(window, 'unshifted.avi')
    make_video(shifted, 'shifted.avi')

    hdus[1].data = smoothed
    write_fits('unshifted.fits', hdus)
    hdus[1].data = shifted
    write_fits('shifted.fits', hdus)


if __name__ == "__main__":
    with fits.open(os.path.join(DIR, f'cube_{OBSID}_{STUDY_ID}_0.fits')) as hdus:
        process_file(hdus)
