import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
#from astro_clock import Clock


def my_function(i):
    ax.cla()
    t = datetime.now()
    r = 1
    theta = t.second * 6 * (np.pi/180)
    ax.scatter([theta], [r])
    ax.plot([0, theta], [0, r])
    ax.set_title(str(t)[11:19])
    ax.set_rticks([])#0.8*r])
    #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    #ax.grid(True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.arange(12)*30,
                      ['12'] + [str(i) for i in range(1,12)])


fig = plt.figure()
ax = plt.subplot(projection='polar')
ax.set_theta_direction(-1)

ani = FuncAnimation(fig, my_function, interval=1000)
plt.show()
