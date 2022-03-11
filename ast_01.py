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
s_az = s.az.value
s_alt = s.alt.value

"""
m = get_body('moon', T, loc).transform_to(altaz)
m_az = m.az.value
m_alt = m.alt.value
"""

pos = s.cartesian.xyz.value.T

au = 149597870700

N = sph2car(np.array([0,0,au]))
S = sph2car(np.array([180,0,au]))
E = sph2car(np.array([90,0,au]))
W = sph2car(np.array([270,0,au]))

color = len(pos) * ['b']
size = len(pos) * [5]
ax = plot_xyz(pos[:,0], pos[:,1], pos[:,2], color=color, size=size)
ax.scatter(N[0],N[1],N[2], c='r')
ax.scatter(S[0],S[1],S[2], c='g')
ax.scatter(E[0],E[1],E[2], c='b')
ax.scatter(W[0],W[1],W[2], c='y')
plt.show()

"""
Z is dec
We need Z and Y
"""
