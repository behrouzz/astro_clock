import numpy as np
from datetime import datetime
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d.axes3d import Axes3D

lon, lat = (48.58313582900411, 7.744083817548831)
loc = EarthLocation(lon=lon, lat=lat+40)

time_window = [datetime(2022, 12, 11, i) for i in range(24)]
T = Time(time_window)

altaz = AltAz(obstime=T, location=loc)

s = get_body('sun', T, loc).transform_to(altaz)

pos = s.cartesian.xyz.to('au').value.T


N = sph2car(np.array([0, 0, 1]))
E = sph2car(np.array([90, 0, 1]))

color = len(pos) * ['b']
size = len(pos) * [5]

ax = plot_xyz(pos[:,0], pos[:,1], pos[:,2], color=color, size=size)
ax.scatter(N[0],N[1],N[2], c='r')
ax.scatter(E[0],E[1],E[2], c='y')
ax.scatter([0],[0],[0], c='k', s=50, marker='+')



xx, yy = np.meshgrid(np.arange(-1,1.1, 0.5), np.arange(-1,1.1, 0.5))
z = xx*0
ax.plot_surface(xx, yy, z, alpha=0.5)

ax.plot_trisurf(pos[:,0], pos[:,1], pos[:,2], linewidth=0)
#ax.plot_surface(pos[:,0], pos[:,1], pos[:,2], alpha=0.5)


plt.gca().invert_yaxis()
plt.show()

"""
Z is dec
We need Z and Y
"""
