import numpy as np
from datetime import datetime, timedelta
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon, Wedge

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

T_now = Time(now)
altaz_now = AltAz(obstime=T_now, location=loc)
s_now = get_body('sun', T_now, loc).transform_to(altaz_now)
pos_now = s_now.cartesian.xyz.to('au').value.T

noon = get_noon(now, lon)
t = [noon + timedelta(hours=i) for i in range(24)]
T = Time(t)
altaz = AltAz(obstime=T, location=loc)
s = get_body('sun', T, loc).transform_to(altaz)
pos = s.cartesian.xyz.to('au').value.T


fig, ax = plt.subplots()

cir = Circle((0, 0), 1, alpha=0.2)
ax.add_artist(cir)

ls = [(0,30), (60,90), (120,150), (180,210), (240,270), (300,330)]


tmp = [*range(0, 360, 15)]
ls = [*zip(tmp[::2], tmp[1:][::2])]

for i in ls:
    wg = Wedge(0, 1, i[0], i[1], alpha=0.2)
    ax.add_artist(wg)

ax.scatter(pos[:,1], pos[:,2], c='y', alpha=0.5)
ax.scatter(pos_now[1], pos_now[2], c='r')
ax.set_aspect('equal')
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
plt.show()
