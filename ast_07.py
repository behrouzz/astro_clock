import numpy as np
from datetime import datetime, timedelta
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon, Wedge
import ephem

def get_noon(lon, lat):
    o = ephem.Observer()
    o.lat, o.long = str(lat), str(lon)
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.now())
    noon = o.next_transit(sun, start=sunrise)
    #sunset = o.next_setting(sun, start=noon)
    return noon.datetime()
    

lat, lon = (48.58313582900411, 7.744083817548831)
loc = EarthLocation(lon=lon, lat=lat)

now = datetime.utcnow()

T_now = Time(now)
altaz_now = AltAz(obstime=T_now, location=loc)
s_now = get_body('sun', T_now, loc).transform_to(altaz_now)
pos_now = s_now.cartesian.xyz.to('au').value.T

noon = get_noon(lon, lat)
t = [noon + timedelta(hours=i) for i in range(24)]
T = Time(t)
altaz = AltAz(obstime=T, location=loc)
s = get_body('sun', T, loc).transform_to(altaz)
pos = s.cartesian.xyz.to('au').value.T


fig, ax = plt.subplots()

cir = Circle((0, 0), 1, alpha=0.2)
ax.add_artist(cir)

x1, y1 = [0, pos_now[1]], [0, pos_now[2]]
ax.plot(x1, y1, c='r')#marker = 'o')


ax.scatter(pos[:,1], pos[:,2], c='y', alpha=0.5)
ax.scatter(pos_now[1], pos_now[2], c='r')
ax.hlines(y=0, xmin=-1, xmax=1, linewidth=2, color='k')
ax.vlines(x=0, ymin=-1, ymax=1, linewidth=0.1, color='k')
ax.set_aspect('equal')
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
plt.show()
