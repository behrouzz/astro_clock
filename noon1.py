import numpy as np
from datetime import datetime, timedelta


def get_noon(lon):
    tt = (1 - lon/15) + 12
    return tt

lat, lon = (48.58313582900411, 7.744083817548831)

t = datetime.now()
t1 = datetime(t.year, 1, 1)
t2 = datetime(t.year, t.month, t.day)
n = (t2 - t1).days


B = (n-1) * (360/365) * (np.pi/180)

E = 229.2 * (0.000075 + 0.001868*np.cos(B) - 0.032077*np.sin(B)\
             - 0.014615*np.cos(2*B) - 0.04089*np.sin(2*B))

Lst = ((datetime.now() - datetime.utcnow()).total_seconds()/3600) * 15

dt = timedelta(minutes=4*(Lst-lon)+E)

solar_time = t + dt

print('Standard time :', t)
print('Solar time    :', solar_time)
