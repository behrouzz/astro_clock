import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from astro_clock import Clock


class AnimClock:
    def __init__(self, lon=0):
        self.lon = lon
        self.fig = plt.figure()
        self.ax_mst = plt.subplot(131, projection='polar')
        self.ax_tst = plt.subplot(132, projection='polar')
        self.ax_lst = plt.subplot(133, projection='polar')
              

    def show(self):
        ani = FuncAnimation(self.fig, self.__core, interval=1000)
        plt.tight_layout(pad=1, w_pad=0.9)
        plt.show()
        

    def __clear(self):
        self.ax_mst.cla()
        self.ax_tst.cla()
        self.ax_lst.cla()


    def __config(self, ax):
        ax.grid(False)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetagrids(
            np.arange(12)*30,
            ['12'] + [str(i) for i in range(1,12)]
            )
        ax.set_rticks([])
        return ax


    def __set_titles(self):
        self.ax_mst.set_title('Mean solar time\n')
        self.ax_tst.set_title('True solar time\n')
        self.ax_lst.set_title('Local sidereal time\n')


    def __set_lst_text(self, lst_deg):
        a = self.ax_lst.get_position()
        x0, y0, x1, y1 = a.x0, a.y0, a.x1, a.y1        
        self.ax_lst.text(
            x=(x0+x1)/2,
            y=((y0+y1)/2)*1.2,
            s='{0:.3f}'.format(lst_deg)+'°',
            fontsize='small',
            horizontalalignment='center',
            transform=plt.gcf().transFigure)


    def __angles(self, t):
        s = t.second
        m = t.minute + t.second/60 + (t.microsecond/1000000)/60
        h = t.hour + m/60
        theta_s = t.second * 6 * (np.pi/180)
        theta_m = m * 6 * (np.pi/180)
        theta_h = h * 30 * (np.pi/180)
        return theta_h, theta_m, theta_s


    def __plot(self, ax, theta_h, theta_m, theta_s):
        r = 1
        ax.plot([0, theta_h], [0, 0.6*r], lw=5, c='b')
        ax.plot([0, theta_m], [0, 0.9*r], lw=2, c='b')
        ax.plot([0, theta_s], [0, r], lw=0.5, c='r')
        return ax

    
    def __core(self, i):
        self.__clear()
        
        t = datetime.utcnow()
        c = Clock(t, self.lon)
        
        mst_theta_h, mst_theta_m, mst_theta_s = self.__angles(c.mean_solar_time)
        tst_theta_h, tst_theta_m, tst_theta_s = self.__angles(c.true_solar_time)
        lst_theta_h, lst_theta_m, lst_theta_s = self.__angles(c.lst)

        self.ax_mst = self.__plot(self.ax_mst, mst_theta_h, mst_theta_m, mst_theta_s)
        self.ax_tst = self.__plot(self.ax_tst, tst_theta_h, tst_theta_m, tst_theta_s)
        self.ax_lst = self.__plot(self.ax_lst, lst_theta_h, lst_theta_m, lst_theta_s)

        self.__set_titles()

        self.ax_mst = self.__config(self.ax_mst)
        self.ax_tst = self.__config(self.ax_tst)
        self.ax_lst = self.__config(self.ax_lst)

        self.__set_lst_text(c.lst_deg)


lon = 7.744083817548831

ac = AnimClock(lon)
ac.show()

