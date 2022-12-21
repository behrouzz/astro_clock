from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp
from funcs import *


obs_loc = (7.744083817548831, 48.58313582900411, 140)
#obs_loc = (139.6503, 35.6762, 0) # tokyo
#obs_loc = (-122.4194, 37.7749, 0) # san francisco

lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030.bsp']

t = datetime.utcnow()
#t = datetime(2022, 6, 12)


t_noon = get_noon(t, obs_loc, kernels)
print(t_noon)


t24 = [t_noon + timedelta(hours=i) for i in range(24)]
sun = apparent_sun_window(t24, obs_loc, kernels)

from hypatie import sph2car

pos = sph2car(sun) * km2au
pos_now = apparent_sun(datetime.utcnow(), obs_loc, kernels)
pos_now = sph2car(pos_now) * km2au

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon, Wedge

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
#plt.axis('off')
ax.set_xticks([])
ax.set_yticks([])

plt.show()
