import numpy as np
from datetime import datetime, timedelta, time
from hypatie.time import get_lst, get_noon, solar_time
import spiceypy as sp
from hypatie.earth import geodetic_to_geocentric
from hypatie.transform import sph2car

km2au = 6.684587122268446e-09

class Clock:
    def __init__(self, t, lon=0, eot_df=None):
        self.t = t
        self.lon = lon
        self.mean_solar_time, self.true_solar_time = \
                solar_time(t=self.t, lon=self.lon, eot_df=eot_df)
        self.noon = get_noon(t=self.t, lon=self.lon, eot_df=eot_df)
        self.eot = (self.mean_solar_time - self.true_solar_time).total_seconds()/60
        self.eot_str = self.__format_eot()
        self.lst_deg = get_lst(self.t, self.lon)
        self.lst = self.__format_lst()

    def __format_lst(self):
        td = timedelta(hours=self.lst_deg/15)
        a = str(td).split(':')
        h = int(a[0])
        m = int(a[1])
        s = int(a[-1].split('.')[0])
        ms = int(a[-1].split('.')[1])
        return time(h,m,s,ms)


    def __format_eot(self):
        sign = '-' if self.eot<0 else '+'
        td = timedelta(minutes=abs(self.eot))
        a = str(td).split(':')
        h = int(a[0])
        m = int(a[1])
        s = int(a[-1].split('.')[0])
        ms = int(a[-1].split('.')[1])
        minsec = str(time(h,m,s,ms))[3:]#.split('.')[0]
        return sign + minsec


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
    obs_loc_car = geodetic_to_geocentric(obs_loc)
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
    obs_loc_car = geodetic_to_geocentric(obs_loc)
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


def sun24(t, obs_loc, noon, kernels):
    t24 = [noon + timedelta(hours=i) for i in range(24)]
    sun = apparent_sun_window(t24, obs_loc, kernels)
    pos = sph2car(sun) * km2au
    pos_now = apparent_sun(t, obs_loc, kernels)
    pos_now = sph2car(pos_now) * km2au
    return pos, pos_now
