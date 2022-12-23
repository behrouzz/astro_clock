from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp
#from funcs import *
from hypatie.time import get_noon
import ephem


def get_noon_exact(t, lon, lat):
    t = t + timedelta(hours=(lon/15))
    o = ephem.Observer()
    o.lat, o.long = str(lat), str(lon)
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    return noon.datetime()


#obs_loc = (7.744083817548831, 48.58313582900411, 140)
#obs_loc = (0, 0, 0) # grw
obs_loc = (139.6503, 35.6762, 0) # tokyo
#obs_loc = (-122.4194, 37.7749, 0) # san francisco
#obs_loc = (30.3351, 59.9343, 0) # saint petersburg

lon, lat, h = obs_loc

aa = []
for i in range(1, 13):
    t = datetime(2022, i, 24, 17)
    t1 = get_noon_exact(t, lon, lat)
    t2 = get_noon(t, lon)
    dt = (t2-t1).total_seconds()
    aa.append(dt)


for i in range(12):
    print(i+1, ':', aa[i])

##t = datetime.utcnow()
##print(get_noon_exact(t, lon, lat))
##print(get_noon(t, lon))
