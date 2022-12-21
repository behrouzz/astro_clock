from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp


def get_t_win(t0, steps, dt=2):
    t1 = t0 - timedelta(seconds=3600*dt)
    t2 = t0 + timedelta(seconds=3600*dt)
    rng = t2 - t1
    dt = rng / steps
    window = [t1 + dt*i for i in range(steps+1)]
    return window


def apparent_sun_window(t0, obs_loc, kernels, steps=100):
    r2d = 180/np.pi
    
    t_win = get_t_win(t0=t0, steps=steps, dt=2)
    
    for k in kernels:
        sp.furnsh(k)
    
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


def get_noon(t, obs_loc, kernels):
    t0 = datetime(t.year, t.month, t.day, 12-round(obs_loc[0]/15))
    t_win, pos = apparent_sun_window(t0, obs_loc, kernels, steps=10000)
    ind = np.argmax(pos[:,1])
    t_noon = t_win[ind]
    return t_noon


obs_loc = (7.744083817548831, 48.58313582900411, 140)
#obs_loc = (139.6503, 35.6762, 0) # tokyo
#obs_loc = (-122.4194, 37.7749, 0) # san francisco

lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030.bsp']

t = datetime.utcnow()

t_noon = get_noon(t, obs_loc, kernels)
print(t_noon)
