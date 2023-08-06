"""Experiments with astropy"""

import os.path
import timeit
from astropy.table import Table
import astropy.io.fits as fits

DIR = 'C:/Users/sg55/spice/python'
OUT = 'C:/Users/sg55/temp/'
OBSID = 33554559
STUDY_ID = 30

file = os.path.join(DIR, f'cube_{OBSID}_{STUDY_ID}_0.fits')
out = os.path.join(OUT, f'temp.fits')
t = Table.read(file, hdu=2)
hdu = fits.table_to_hdu(t)
hdu.header
hdu.data
hdu.writeto(out)
hdul = fits.HDUList([fits.PrimaryHDU(), hdu])
hdul.writeto(out)

fits.append(out, hdu.data, hdu.header, verify=False)

tables = [t, t]
for table in tables:
    table.write(out, append=True)


def append():
    t.write(out, append=True)


def write():
    t.write(out, overwrite=True)


timeit.timeit(append, number=100)
timeit.timeit(write, number=100)
