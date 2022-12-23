from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp
from funcs import *



def get_noon_exact(t, lon, lat):
    t = datetime(t.year, t.month, t.day, 12)
    import ephem
    o = ephem.Observer()
    o.lat, o.long = str(lat), str(lon)
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    #sunset = o.next_setting(sun, start=noon)
    return noon.datetime()


obs_loc = (7.744083817548831, 48.58313582900411, 140)
#obs_loc = (139.6503, 35.6762, 0) # tokyo
#obs_loc = (-122.4194, 37.7749, 0) # san francisco

lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030.bsp']

t = datetime.utcnow()

t0 = get_noon_exact(t, lon, lat)
print(t0)

t1 = get_noon(t, obs_loc, kernels)
print(t1)

t2 = get_noon_approx(t, lon)
print(t2)

Lst = ((datetime.now() - datetime.utcnow()).total_seconds()/3600) * 15

from hypatie.time import get_lst

LST = get_lst(t, lon)



