from datetime import datetime, timedelta
import numpy as np
import bspice as bs
import spiceypy as sp
from funcs import *



obs_loc = (7.744083817548831, 48.58313582900411, 140)
#obs_loc = (0, 0, 0) # grw
obs_loc = (139.6503, 35.6762, 0) # tokyo
#obs_loc = (-122.4194, 37.7749, 0) # san francisco
#obs_loc = (30.3351, 59.9343, 0) # saint petersburg

lon, lat, h = obs_loc

#t_utc = datetime(2022, 2, 11)
t_utc = datetime.utcnow()
dt_grw = timedelta(hours=(lon/15))

mean_solar_time = t_utc + dt_grw
eot = get_eot(t_utc)
true_solar_time = mean_solar_time + eot

print('EOT:', eot.total_seconds()/60)
print('Mean solar time:', mean_solar_time)
print('True solar time:', true_solar_time)


dt = true_solar_time - \
     datetime(true_solar_time.year,
              true_solar_time.month,
              true_solar_time.day,
              12)

noon = t_utc - dt
print(noon)

def get_noon_exact(t, lon, lat):
    t = t + timedelta(hours=(lon/15)) 
    import ephem
    o = ephem.Observer()
    o.lat, o.long = str(lat), str(lon)
    sun = ephem.Sun()
    sunrise = o.previous_rising(sun, start=ephem.date(t))
    noon = o.next_transit(sun, start=sunrise)
    #sunset = o.next_setting(sun, start=noon)
    return noon.datetime()

print(get_noon_exact(t_utc, lon, lat))

