from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp


km2au = 6.684587122268446e-09

def get_t_win(t0, steps, dt=2):
    t1 = t0 - timedelta(seconds=3600*dt)
    t2 = t0 + timedelta(seconds=3600*dt)
    rng = t2 - t1
    dt = rng / steps
    window = [t1 + dt*i for i in range(steps+1)]
    return window


def apparent_sun(t, obs_loc, kernels):
    r2d = 180/np.pi
    
    for k in kernels:
        sp.furnsh(k)
    
    et = sp.str2et(str(t))
    obs_loc_car = bs.lonlat_to_cartesian(obs_loc)
    pos = []
    
    state, lt  = sp.azlcpo(method='ELLIPSOID', target='sun', et=et,
        abcorr='LT+S', azccw=False, elplsz=True,
        obspos=obs_loc_car, obsctr='earth', obsref='ITRF93')

    r, az, alt = state[:3]
    pos = np.array([az*r2d, alt*r2d, r])
    
    sp.kclear()
    return pos

def apparent_sun_window(t_win, obs_loc, kernels):
    r2d = 180/np.pi
    
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
    return pos


def get_noon(t, obs_loc, kernels, steps=10000):
    t0 = datetime(t.year, t.month, t.day, 12-round(obs_loc[0]/15))
    t_win = get_t_win(t0=t0, steps=steps, dt=2)
    pos = apparent_sun_window(t_win, obs_loc, kernels)
    ind = np.argmax(pos[:,1])
    t_noon = t_win[ind]
    return t_noon


