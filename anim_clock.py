import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
#from astro_clock import Clock


def my_function(i):
    ax.cla()
    t = datetime.now()

    s = t.second
    m = t.minute + t.second/60 + (t.microsecond/1000000)/60
    h = t.hour + m/60
    
    r = 1
    
    theta_s = t.second * 6 * (np.pi/180)
    theta_m = m * 6 * (np.pi/180)
    theta_h = h * 30 * (np.pi/180)
    
    ax.plot([0, theta_h], [0, 0.7*r], lw=5)
    ax.plot([0, theta_m], [0, 0.9*r], lw=2)
    ax.plot([0, theta_s], [0, r], lw=1)
    
    #ax.scatter([theta_s], [r])
    #ax.scatter([theta_m], [0.9*r], c='g')
    
    
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
#ax.set_theta_direction(-1)

ani = FuncAnimation(fig, my_function, interval=1000)
plt.show()
