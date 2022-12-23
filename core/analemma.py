from funcs import apparent_sun_window
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from hypatie.plots import plot_altaz


#obs_loc = (7.744083817548831, 48.58313582900411, 140)
obs_loc = (0, 45, 0)
lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr + 'naif0012.tls',
           adr + 'pck00010.tpc',
           adr + 'earth_latest_high_prec.bpc',
           adr + 'de440s.bsp']

t0 = datetime(2022, 1, 1, 12)
tw = [t0 + timedelta(days=i) for i in range(365)]

pos = apparent_sun_window(tw, obs_loc, kernels)

##ax = plot_altaz(pos[:,0], pos[:,1], size=1)
##plt.show()


x1, x2 = pos[:,0].min()-1, pos[:,0].max()+1
y1, y2 = pos[:,1].min()-1, pos[:,1].max()+1

plt.scatter(pos[:,0], pos[:,1], s=1)
plt.xlim(x1, x2)
plt.ylim(y1, y2)
plt.show()
