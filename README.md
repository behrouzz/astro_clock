**Author:** [Behrouz Safari](https://astrodatascience.net/)<br/>

# astro_clock
*Astronomical clock*


## Example 1: Live clock with matplotlib

You can simply play the live clock by passing the longtitude to an instance of LiveClock.

```python
from astro_clock import LiveClock

ac = LiveClock(lon=7.744083817548831)
ac.show()
```

![alt text](https://github.com/behrouzz/astronomy/raw/main/images/anim_clock.jpg)


## Example 2: Live clock with plotly and dash

The live clock in the above example can be created using plotly and dash. The source code is in the file *ex2_dash_live_clock.py*. If you have already installed plotly and dash, you can go to the command line and run the program:

    python ex2_dash_live_clock.py

Then, open your browser and go to this address: 

    http://127.0.0.1:8050/

You can enter your longtitude in the input box of the webpage.

![alt text](https://github.com/behrouzz/astronomy/raw/main/images/dash_live_clock.png)


## Example 3: Apparent positions of sun

Get a plot showing the position of sun now and during 24 hours.

```python
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from astro_clock import Clock, sun24, plot_sun


obs_loc = (7.744083817548831, 48.58313582900411, 140)
lon, lat, h = obs_loc

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr + 'naif0012.tls',
           adr + 'pck00010.tpc',
           adr + 'earth_latest_high_prec.bpc',
           adr + 'de440s.bsp']

t = datetime.utcnow()

c = Clock(t, lon)

pos, pos_now = sun24(t, obs_loc, c.noon, kernels)


lst = 'Local Sidereal Time: ' + str(c.lst)[:8]
mst = 'Mean Solar Time: '+ str(c.mean_solar_time)[:19]
tst = 'True solar Time: ' + str(c.true_solar_time)[:19]

title = lst + '\n' + mst + '\n' + tst

fig, ax = plot_sun(pos, pos_now, title=title)
plt.show()
```

<p align="center">
  <img src="https://github.com/behrouzz/astronomy/raw/main/images/sun_position.jpg" />
</p>
