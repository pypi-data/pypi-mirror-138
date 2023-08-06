"""
This is becoming a higher level API using the SPICE kernels.
"""
import os
import sys
from datetime import datetime, timezone, timedelta
from math import atan, atan2, asin, pi, sin, cos
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import spiceypy

from spice_kernels.util import mid_time, from_utc

#KERNELS = "C:/Users/sg55/spice/solo_kernels/solar-orbiter/kernels"
KERNELS = os.getenv("SPICE_KERNELS", ".")
#OUT = "C:/Users/sg55/temp/"
OUT = "."
KERNEL = "solo_ANC_soc-flown-mk.tm"
MK = os.path.join(KERNELS, "mk", KERNEL)
R2M = 180 / pi * 60
R2S = R2M * 60
VX = np.array((1.0, 0.0, 0.0))
NAIF_ID = -144
T2000 = datetime(2000, 1, 1).timestamp()


def load_kernels():
    print(f"Loading meta-kernel {MK}")
    spiceypy.tkvrsn("TOOLKIT")
    spiceypy.furnsh(MK)


def to_utc_string(t: datetime) -> str:
    """
    Convert a Python datetime to UTC.
    :param t: reference time
    :return: UTC string
    """
    return t.isoformat(timespec="seconds").split("+")[0]


def to_utc_file(t: datetime) -> str:
    """
    Convert a Python datetime to UTC, suitable for a file name.
    :param t: reference time
    :return: UTC string
    """
    return f"{t:%Y-%m-%dT%Hh%Mm%Ss}"


def to_date(utc: str, offset: float = 0) -> datetime:
    """
    Convert utc string to datetime.
    :param utc: utc string
    :param offset to apply, seconds
    :return: python datetime
    """
    dt = datetime.fromisoformat(utc[:-1])
    return dt + timedelta(seconds=offset)


def obt_to_utc(obt: str) -> str:
    """
    Convert an OBT string to UTC.

    :param obt: seconds:subpart
    :return: time correlated UTC
    """
    # Obt to Ephemeris time (seconds past J2000)
    ephemeris_time = spiceypy.scs2e(NAIF_ID, obt)
    # Format of output epoch: ISOC (ISO Calendar format, UTC)
    # Digits of precision in fractional seconds: 3
    return spiceypy.et2utc(ephemeris_time, "ISOC", 3)


def utc_to_obt(utc: str) -> str:
    """
    Convert UTC to OBT.

    :param utc: time correlated UTC
    :return: OBT in SPICE format
    """
    # Utc to Ephemeris time (seconds past J2000)
    ephemeris_time = spiceypy.utc2et(utc)
    # Ephemeris time to Obt
    return spiceypy.sce2s(NAIF_ID, ephemeris_time)


def cuc_to_utc(cuc: int) -> str:
    """
    Convert CUC time to UTC.

    :param cuc: 48-bit CUC time
    :return: time correlated UTC
    """
    seconds = cuc >> 16
    subsecs = cuc & 0xFFFF
    obt = f"{seconds}:{subsecs}"
    return obt_to_utc(obt)


def utc_to_cuc(utc: str) -> int:
    """
    Convert UTC to CUC time.

    :param utc: time correlated UTC
    :return: 48-bit CUC time
    """
    obt = utc_to_obt(utc)
    parts = obt.split("/")[1].split(":")
    seconds = int(parts[0])
    subsecs = int(parts[1])
    return seconds << 16 | subsecs


def date_to_cuc(utc: datetime) -> int:
    return utc_to_cuc(to_utc_string(utc))


def correlate(time: datetime) -> datetime:
    """
    Convert uncorrelated time to correlated time.
    :param time: uncorrelated utc
    :param offset to apply, seconds
    :return: correlated date
    """
    # TODO? Add sub-second part
    # Add the 5 leap seconds since 2000, datetime doesn't support them.
    cuc = int(time.timestamp() - T2000 + 5) << 16
    ut_corr = cuc_to_utc(cuc)
    return datetime.fromisoformat(ut_corr)


def get_position(t: datetime, correct_aberration: bool = True) -> np.array:
    """
    Get the sun position vector in the spacecraft frame.

    :param t: reference time
    :param correct_aberration: if true, correct for light time and aberration
    :return: vector (not normalised)
    """
    et = spiceypy.str2et(to_utc_string(t))
    ab = "LT+S" if correct_aberration else "NONE"
    pos, _ = spiceypy.spkpos("SUN", et, "SOLO_SRF", ab, "SOLO")
    return pos


def get_distance(t: datetime) -> float:
    """
    Get distance Solar Orbiter to sun.

    :param t: reference time
    :return: distance in km
    """
    return spiceypy.vnorm(get_position(t))


def get_radius(t: datetime) -> float:
    """
    Get solar radius as observed by Solar Orbiter.

    :param t: reference time
    :return: solar radius in arc seconds
    """
    return R2S * atan(696342.0 / get_distance(t))


def to_direction(v: np.array) -> Tuple[float, float]:
    """
    Get longitude, latitude from vector.

    Latitude is to solar North; longitude to solar West.
    :param v: pointing vector
    :return: longitude, latitude tuple
    """
    # alpha = atan2(v[1], v[2])
    # delta = asin(v[0])
    # return -delta, alpha
    alpha = atan2(v[1], v[0])
    delta = asin(v[2])
    return alpha, -delta


def get_pointing(t: datetime, correct_aberration: bool = True) -> np.array:
    """
    Get the spacecraft pointing vector.

    :param t: reference time
    :param correct_aberration: if true, correct for light time and aberration
    :return: unit vector
    """
    v = get_position(t, correct_aberration)
    u, _ = spiceypy.unorm(v)
    return u


def get_lon_lat(time: datetime, correct_aberration: bool = True) -> Tuple[float, float]:
    """
    Get solar longitude/latitude at given time.
    :param time: to get
    :param correct_aberration: if true, correct for light time and aberration
    :return: tuple of longitude/latitude, arcseconds
    """
    v = get_pointing(time, correct_aberration)
    lon, lat = to_direction(v)
    return lon * R2S, lat * R2S


def get_sc_lon_lat(time: datetime) -> Tuple[float, float]:
    """
    Get s/c longitude/latitude at given time.
    :param time: to get
    :return: tuple of longitude/latitude, arcseconds
    """
    # This seems  a bit flaky, hopefully comes out right.
    et = spiceypy.str2et(to_utc_string(time))
    px = spiceypy.pxform("SOLO_SRF", "SOLO_SOLAR_MHP", et)
    v = px.dot(VX)
    lat, lon = to_direction(np.flip(v))
    return lon * R2S, lat * R2S


def get_pointing_array(
    start: datetime, end: datetime, delta: timedelta = None
) -> Tuple[List[datetime], np.array, np.array]:
    """
    Get longitude and latitude of spacecraft pointing.

    :param start: of time range
    :param end: of time range
    :param delta: increment, default 15 seconds
    :return: tuple of list of datetime, array of longitude, array of altitude (arcsec)
    """

    tim = []
    lon = []
    lat = []
    if delta is None:
        delta = timedelta(seconds=15)

    while start <= end:
        az, el = get_lon_lat(start)
        tim.append(start)
        lon.append(az)
        lat.append(el)
        start += delta

    return tim, np.array(lon), np.array(lat)


class Plotter:
    def __init__(self, nx: int = 2, ny: int = 2):
        self.nx = nx
        self.ny = ny
        self.count = 0
        self.figure = plt.figure()

    def plot(self, t: List[datetime], y: np.array, title: str = "", units: str = "") -> None:

        self.count += 1
        ax = self.figure.add_subplot(self.nx, self.ny, self.count)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.set_title(title)
        ax.set_xlabel("Time (UTC)")
        ax.set_ylabel(units)
        ax.plot(t, y)

    def save(self, file_name: str) -> None:
        self.figure.subplots_adjust(hspace=0.6)
        self.figure.savefig(file_name + ".png")


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: get_pointing start-utc end-utc [delta-seconds]")
        sys.exit(1)

    load_kernels()
    start_s = args[0]
    end_s = args[1]
    delta_t = float(args[2]) if len(args) == 3 else 10.0
    start = from_utc(start_s)
    end = from_utc(end_s)
    #start = datetime(2021, 8, 17, 5, 0, 0, tzinfo=timezone.utc)
    #end = datetime(2021, 8, 17, 8, 0, 0, tzinfo=timezone.utc)

    ref_time = mid_time(start, end)
    print(f"obt {ref_time} utc {to_utc_string(ref_time)} cuc {hex(date_to_cuc(ref_time))}")

    print(
        f"Sun distance at {ref_time:%Y-%m-%d %H:%M} is "
        f"{get_distance(ref_time)/1e6:.2f}Mkm radius {get_radius(ref_time):.2f}"
    )

    lon, lat = get_lon_lat(ref_time)
    print(f"Solar position lon {lon} lat {lat}")
    lon, lat = get_sc_lon_lat(ref_time)
    print(f"S/C position lon {lon} lat {lat}")

    # Uncorrected UTC 15th May 2020 10:00:02
    cuc = 0x265124A70D4F
    utc = cuc_to_utc(cuc)
    obt = utc_to_obt(utc)
    print(f"utc {utc} obt {obt} -> utc {obt_to_utc(obt)} -> cuc {hex(utc_to_cuc(utc))}")

    # Test date after kernel data.
    now = datetime.now()
    print(f"now {now} -> cuc {hex(date_to_cuc(now))}")

    part_name = "-TO-".join((to_utc_file(start), to_utc_file(end)))
    delta = timedelta(seconds=delta_t)
    tim, lon, lat = get_pointing_array(start, end, delta)

    with open(os.path.join(OUT, "Pointing_Data_" + part_name + ".csv"), "w") as f:
        f.write(MK+"\n")
        f.write("Time (UTC), Longitude (arcsec), Latitude (arcsec)\n")
        for i in range(len(tim)):
            f.write(",".join((to_utc_string(tim[i]) + "Z", f"{lon[i]:.2f}", f"{lat[i]:.2f}\n")))

    dlon = 60 * (lon[1:] - lon[:-1])
    dlat = 60 * (lat[1:] - lat[:-1])
    dtim = [tim[i] + delta / 2 for i in range(1, len(tim))]

    plotter = Plotter(nx=2, ny=1)
    plotter.plot(tim, lon, title="longitude", units="arcsec")
    plotter.plot(tim, lat, title="latitude", units="arcsec")
    # plotter.plot(dtim, dlon, title='delta-longitude', units='arcsec')
    # plotter.plot(dtim, dlat, title='delta-latitude', units='arcsec')
    plotter.save(os.path.join(OUT, "Pointing_Plot_" + part_name))
    #plt.show()


if __name__ == "__main__":
    main()
