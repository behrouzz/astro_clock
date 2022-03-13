import numpy as np
from datetime import datetime
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt

def get_noon(lon):
    tt = (1 - lon/15) + 12
    return tt

lat, lon = (48.58313582900411, 7.744083817548831)
loc = EarthLocation(lon=lon, lat=lat)

now = datetime.utcnow()

time_window = [datetime(now.year, now.month, now.day, i) for i in range(24)]
T = Time(time_window)

T_now = Time(now)

altaz = AltAz(obstime=T, location=loc)
altaz_now = AltAz(obstime=T_now, location=loc)

s = get_body('sun', T, loc).transform_to(altaz)
s_now = get_body('sun', T_now, loc).transform_to(altaz_now)

pos = s.cartesian.xyz.to('au').value.T
pos_now = s_now.cartesian.xyz.to('au').value.T


fig, ax = plt.subplots()
ax.scatter(pos[:,1], pos[:,2])
ax.scatter(pos_now[1], pos_now[2])
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.show()

"""
Z is dec
We need Z and Y
"""
