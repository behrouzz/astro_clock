import numpy as np
from datetime import datetime, timedelta
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def solar_time(t, lon):
    t1 = datetime(t.year, 1, 1)
    t2 = datetime(t.year, t.month, t.day)
    n = (t2 - t1).days
    B = (n-1) * (360/365) * (np.pi/180)

    E = 229.2 * (0.000075 + 0.001868*np.cos(B) - 0.032077*np.sin(B)\
                 - 0.014615*np.cos(2*B) - 0.04089*np.sin(2*B))

    Lst = ((datetime.now() - datetime.utcnow()).total_seconds()/3600) * 15
    dt = timedelta(minutes=4*(Lst-lon)+E)
    solar_time = t + dt
    return solar_time

def get_noon(t, lon):
    st = solar_time(t, lon)
    dt = st - datetime(st.year, st.month, st.day, 12)
    return t - dt

def mag(x):
    return np.linalg.norm(np.array(x))

lat, lon = (48.58313582900411, 7.744083817548831)
loc = EarthLocation(lon=lon, lat=lat)

now = datetime.utcnow()

time_window = [now + timedelta(hours=i) for i in [0, 4, 8, 12, 16, 20]]
T = Time(time_window)

altaz = AltAz(obstime=T, location=loc)

s = get_body('sun', T, loc).transform_to(altaz)

pos = s.cartesian.xyz.to('au').value.T

middle = (pos[0]+pos[3])/2

r = mag(pos[0,1:] - middle[1:])



fig, ax = plt.subplots()
ax.scatter(pos[:,1], pos[:,2])
ax.scatter(pos[0,1], pos[0,2], c='r')
ax.scatter(middle[1], middle[2], c='k', marker='+')
#ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
asp = ax.get_data_ratio()

cir = plt.Circle((middle[1], middle[2]), r)
#cir.height = cir.height * asp
#cir.width = r*2
ax.add_artist(cir)


plt.show()
