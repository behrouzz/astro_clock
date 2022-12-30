import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
from astro_clock import Clock


class AnimClock:
    def __init__(self, lon=None, kind=None):
        self.lon = lon
        self.kind = kind
        self.title = None
        self.fig = plt.figure()
        self.ax = plt.subplot(projection='polar')
        

    def run(self):
        ani = FuncAnimation(self.fig, self.my_function, interval=1000)
        plt.show()      

    def my_function(self, i):
        self.ax.cla()

        
        t = datetime.utcnow()
        self.title = str(t)[11:19]

        if (self.kind is not None) and (self.lon is not None):
            c = Clock(t, self.lon)
            if self.kind=='true_solar':
                t = c.true_solar_time
            elif self.kind=='mean_solar':
                t = c.mean_solar_time
            elif self.kind=='local_sidereal':
                t = c.lst
            self.title = self.kind.title().replace('_', ' ') + ' Time: ' + str(t)[11:19]

        s = t.second
        m = t.minute + t.second/60 + (t.microsecond/1000000)/60
        h = t.hour + m/60
        
        r = 1
        
        theta_s = t.second * 6 * (np.pi/180)
        theta_m = m * 6 * (np.pi/180)
        theta_h = h * 30 * (np.pi/180)
        
        self.ax.plot([0, theta_h], [0, 0.6*r], lw=5, c='b')
        self.ax.plot([0, theta_m], [0, 0.9*r], lw=2, c='b')
        self.ax.plot([0, theta_s], [0, r], lw=0.5, c='r')
        
        self.ax.set_title(self.title)
        self.ax.set_rticks([])#0.8*r])
        #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        self.ax.grid(False)
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_thetagrids(
            np.arange(12)*30,
            ['12'] + [str(i) for i in range(1,12)]
            )
        
        
        text = 'AstroDataScience.Net'
        angles = np.linspace(215, 145, 20)
        for ii, val in enumerate(text):
            self.ax.text(
                x=angles[ii]*(np.pi/180),
                y=0.98,
                s=val,
                fontfamily='fantasy',
                #horizontalalignment='center',
                fontsize='small',
                #fontstretch='ultra-condensed',
                c = 'purple',
                )


ac = AnimClock(52.5, 'true_solar')
ac.run()
