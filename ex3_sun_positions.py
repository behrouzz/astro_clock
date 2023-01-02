import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from astro_clock import Clock, sun24, plot_sun


obs_loc = (7.744083817548831, 48.58313582900411, 140)
lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr + 'naif0012.tls',
           adr + 'pck00010.tpc',
           adr + 'earth_latest_high_prec.bpc',
           adr + 'de440s.bsp']

t = datetime.utcnow()

c = Clock(t, lon)

pos, pos_now = sun24(t, obs_loc, c.noon, kernels)


lst = 'Local Sidereal Time: ' + str(c.lst)[:8]
mst = 'Mean Solar Time: '+ str(c.mean_solar_time)[:19]
tst = 'True solar Time: ' + str(c.true_solar_time)[:19]

title = lst + '\n' + mst + '\n' + tst

fig, ax = plot_sun(pos, pos_now, title=title)
plt.show()
