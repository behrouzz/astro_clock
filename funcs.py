from datetime import datetime, timedelta
import numpy as np
from hypatie.earth import geodetic_to_geocentric
import spiceypy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon, Wedge


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


def plot_clock(pos, pos_now, title=""):
    fig, ax = plt.subplots()

    cir = Circle((0, 0), 1, alpha=0.2)
    ax.add_artist(cir)
    
    ls = [(0,30), (60,90), (120,150), (180,210), (240,270), (300,330)]

    tmp = [*range(0, 360, 15)]
    ls = [*zip(tmp[::2], tmp[1:][::2])]

    for i in ls:
        wg = Wedge(0, 1, i[0], i[1], alpha=0.2)
        ax.add_artist(wg)


    ax.plot([0, pos_now[1]], [0, pos_now[2]], c='r')#, marker = 'o')

    ax.scatter(pos[:,1], pos[:,2], c='y', alpha=0.5)
    ax.scatter(pos_now[1], pos_now[2], c='r')
    ax.hlines(y=0, xmin=-1, xmax=1, linewidth=2, color='k')
    ax.vlines(x=0, ymin=-1, ymax=1, linewidth=0.5, color='k')
    ax.set_aspect('equal')
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_xticks([])
    ax.set_yticks([])
    #plt.title(title)
    fig.suptitle(title, fontsize=9)
    return fig, ax
