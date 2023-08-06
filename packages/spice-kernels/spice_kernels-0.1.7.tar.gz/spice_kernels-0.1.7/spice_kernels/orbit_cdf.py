import cdflib

DIR = 'C:/Users/sg55/spice/SPICE_Kernels/'
FILE = DIR + 'solo_ANC_soc-orbit_20200210-20301120_L004_V1_00062_V01.cdf'


def lon_lat(start,end):
    lon = file.varget('SHURST_LON', starttime=t1, endtime=t2)
    lat = file.varget('HGRAPH_LAT', starttime=t1, endtime=t2)
    dst = file.varget('HCENTRIC_DIST', starttime=t1, endtime=t2)
    print(f'stonyhurst longitude {lon} (degrees)')
    print(f'heliographic latitude {lat} (degrees)')
    print(f'heliocentric distance {dst} (km)')


file = cdflib.CDF(FILE)
file.cdf_info()

# OBSID 12583472, 14-May-20, ~0940-1120
t1 = [2020, 5, 14, 9, 40, 0, 0, 0, 0]
t2 = [2020, 5, 14, 11, 20, 0, 0, 0, 0]
lon_lat(t1, t2)

# OBSID 12583474, 14-May-20, ~1140-1250
t1 = [2020, 5, 14, 11, 40, 0, 0, 0, 0]
t2 = [2020, 5, 14, 12, 50, 0, 0, 0, 0]
lon_lat(t1, t2)

t = file.varget('EPOCH')
t0 = t[0]
cdflib.cdfepoch.encode(t0)
# '2020-02-10T04:55:50.000000000' = UTC
at0 = cdflib.cdfastropy.convert_to_astropy(t0)
at0.iso
# '2020-02-10 04:56:59.184000000' = TT
s = (t0 / 1e9) - (12 * 3600)
# 634582619.184