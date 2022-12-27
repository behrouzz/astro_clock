import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


from hypatie.coordinates import RAdeg
from hypatie.time import get_lst, get_noon, solar_time
from hypatie.transform import sph2car

from funcs import *


def format_time(t):
    frm = str(t.h).zfill(2) + ':' + \
          str(t.m).zfill(2) + ':' + \
          str(round(t.s)).zfill(2)
    return frm

obs_loc = (7.744083817548831, 48.58313582900411, 140)
lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr + 'naif0012.tls',
           adr + 'pck00010.tpc',
           adr + 'earth_latest_high_prec.bpc',
           adr + 'de440s.bsp']

t = datetime.utcnow()

t_noon = get_noon(t, lon)

t24 = [t_noon + timedelta(hours=i) for i in range(24)]
sun = apparent_sun_window(t24, obs_loc, kernels)



pos = sph2car(sun) * km2au
pos_now = apparent_sun(datetime.utcnow(), obs_loc, kernels)
pos_now = sph2car(pos_now) * km2au


# Local Sidreal Time (LST)
lst = RAdeg(get_lst(t, lon))
lst_str = format_time(lst)

mst, tst = solar_time(t, lon)
mst_str = 'Mean solar time: ' + str(mst)[11:19]
tst_str = 'True solar time: ' + str(tst)[11:19]

title = 'Local Sidereal Time: ' + lst_str + '\n' + mst_str + '\n' + tst_str
        

fig, ax = plot_clock(pos, pos_now, title=title)
plt.show()
