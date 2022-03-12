import numpy as np
from datetime import datetime, timedelta
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.time import Time
from hypatie.transform import sph2car, rev
from hypatie.plots import plot_xyz
import matplotlib.pyplot as plt

def mag(x):
    return np.linalg.norm(np.array(x))

lon, lat = (48.58313582900411, 7.744083817548831)
loc = EarthLocation(lon=lon, lat=lat)

t0 = datetime.utcnow()
time_window = [t0 + timedelta(seconds=i*60) for i in range(86400//60)]

T = Time(time_window)

altaz = AltAz(obstime=T, location=loc)

s = get_body('sun', T, loc).transform_to(altaz)

pos = s.cartesian.xyz.to('au').value.T

#==================================================
# Mohasebat bordari
i_zmax = np.argmax(pos[:,2])
i_zmin = np.argmin(pos[:,2])

P = pos[i_zmax]
Q = pos[i_zmin]

d = Q - P

x = P[0] - (d[0]/d[2])*P[2]
y = P[1] - (d[1]/d[2])*P[2]
z = 0

# intersection of PQ with tangent of earth surface
M = np.array([x,y,z])

# observer location
O = np.array([0,0,0])

# Most upper position of Sun
# P

MO = O - M
MP = P - M

# angle between plane in which the sun moves and observers's tangent surface
a = np.arccos( np.dot(MO, MP) / (mag(MO)*mag(MP)) ) *(180/np.pi)
#==================================================
