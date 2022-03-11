import numpy as np
from datetime import datetime
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt

lon, lat = (48.58313582900411, 7.744083817548831)
loc = EarthLocation(lon=lon, lat=lat)

time_window = [datetime(2022, 3, 11, i) for i in range(24)]
T = Time(time_window)

altaz = AltAz(obstime=T, location=loc)

s = get_body('sun', T, loc).transform_to(altaz)

pos = s.cartesian.xyz.value.T


N = sph2car(np.array([0, 0, 1]))
S = sph2car(np.array([180, 0, 1]))
E = sph2car(np.array([90, 0, 1]))
W = sph2car(np.array([270, 0, 1]))
OOO = sph2car(np.array([60, 45, 1]))

NEWS = np.vstack((N,S,E,W, OOO))
pos_news = np.vstack((pos,NEWS))

#pos[:,1] = -1 * pos[:,1]

color = len(pos)*['b'] + ['r', 'k', 'y', 'g', 'r']
size = len(pos) * [5] + 4*[10] + [20 ]
ax = plot_xyz(pos_news[:,0], pos_news[:,1], pos_news[:,2], color=color, size=size)
plt.show()

"""
Z (hamoon dec): (-1:payin, 1:bala)
Y (1: east, -1:west)
We need Z and Y
"""
