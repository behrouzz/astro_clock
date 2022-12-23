from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp
import pickle


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


##def solar_time(t, lon):
##    t1 = datetime(t.year, 1, 1)
##    t2 = datetime(t.year, t.month, t.day)
##    n = (t2 - t1).days
##    B = (n-1) * (360/365) * (np.pi/180)
##
##    E = 229.2 * (0.000075 + 0.001868*np.cos(B) - 0.032077*np.sin(B)\
##                 - 0.014615*np.cos(2*B) - 0.04089*np.sin(2*B))
##
##    Lst = ((datetime.now() - datetime.utcnow()).total_seconds()/3600) * 15
##    #from hypatie.time import get_lst
##    #Lst = get_lst(t, lon)
##    #print('LST:', Lst)
##    dt = timedelta(minutes=4*(Lst-lon)+E)
##    solar_time = t + dt
##    return solar_time
##
##def get_noon_approx(t, lon):
##    st = solar_time(t, lon)
##    dt = st - datetime(st.year, st.month, st.day, 12)
##    return t - dt


def get_eot(t, eot_cfs_file='equation_of_time.pickle'):
    """
    Equation of time

    t : datetime
    eot_cfs : path of the file containing the dictionary of coefficients
    that should be downloaded from:
    https://github.com/behrouzz/astrodata/raw/main/eot/equation_of_time.pickle
    """
    with open(eot_cfs_file, 'rb') as f:
        dc = pickle.load(f)
    day = (t - datetime(t.year, 1, 1)).days
    coefs =  dc[t.year]
    f = np.poly1d(coefs)
    return timedelta(minutes=f(day))


def solar_time(t_utc, lon, eot_cfs_file='equation_of_time.pickle'):
    """
    t : utc time
    lon: longtitude of observer
    """
    dt_grw = timedelta(hours=(lon/15))
    mean_solar_time = t_utc + dt_grw
    eot = get_eot(t_utc, eot_cfs_file)
    true_solar_time = mean_solar_time + eot
    return mean_solar_time, true_solar_time

def get_noon_simple(t, lon, eot_cfs_file='equation_of_time.pickle'):
    mean_solar_time, true_solar_time = \
            solar_time(t, lon, eot_cfs_file)

    dt = true_solar_time - \
         datetime(true_solar_time.year,
                  true_solar_time.month,
                  true_solar_time.day,
                  12)

    noon = t - dt
    return noon
