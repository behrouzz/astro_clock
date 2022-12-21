import ephem
import numpy as np

d2r = np.pi/180
r2d = 180/np.pi

obs_loc = (7.744083817548831, 48.58313582900411, 140)
#obs_loc = (139.6503, 35.6762, 0) # tokyo
#obs_loc = (-122.4194, 37.7749, 0) # san francisco

lon, lat, h = obs_loc


o = ephem.Observer()
o.lat, o.long = str(lat), str(lon)
sun = ephem.Sun()
sunrise = o.previous_rising(sun, start=ephem.now())
noon = o.next_transit(sun, start=sunrise)
#sunset = o.next_setting(sun, start=noon)
a = noon.datetime()
print(a)

#==========================================

import bspice as bs
from datetime import datetime, timedelta
import spiceypy as sp

def create_range(t0, steps, dt):
    t1 = t0 - timedelta(seconds=dt)
    t2 = t0 + timedelta(seconds=dt)
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]


def create_range_t1t2(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps)]


def apparent_sun_window(t0, obs_loc, kernels):

    #t_win = create_range(t0, 24, 3600*12)
    t_win = create_range(t0, 100, 3600*2)
    
    for k in kernels:
        sp.furnsh(k)

    #et = sp.str2et(str(t))
    ets = [sp.str2et(str(i)) for i in t_win]
    obs_loc_car = bs.lonlat_to_cartesian(obs_loc)
    pos = []
    for et in ets:
        state, lt  = sp.azlcpo(method='ELLIPSOID', target='sun', et=et,
            abcorr='LT+S', azccw=False, elplsz=True,
            obspos=obs_loc_car, obsctr='earth', obsref='ITRF93')

        r, az, alt = state[:3]
        pos.append([az*r2d, alt*r2d, r])
    pos = np.array(pos)
    sp.kclear()
    return t_win, pos




adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030.bsp']

#t0 = datetime.utcnow()

t0 = datetime(2022, 12, 21, 12-round(lon/15))

t_win, pos = apparent_sun_window(t0, obs_loc, kernels)



x = np.arange(pos.shape[0])
y = pos[:,1]

i_max = np.argmax(y)

i1 = round(i_max/2)
i2 = i_max + round(i_max/2)

x_new = x[i1:i2]
y_new = y[i1:i2]

coefs = np.polyfit(x_new, y_new, 9)
f = np.poly1d(coefs)
xx = np.linspace(0, x_new.max(), 10000)
y_pred = f(xx)

tt_win = create_range_t1t2(t_win[0], t_win[-1], len(y_pred))
t_noon = tt_win[np.argmax(y_pred)]
print(t_noon)



import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(t_win, pos[:,1], c='b')
ax.scatter(tt_win, y_pred, c='r', s=1)
plt.show()

print('-'*70)
print(t0)
print('-'*70)
for i in t_win:
    print(i)
