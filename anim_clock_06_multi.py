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


    def __set_titles(self, lst):
        s = '{0:.2f}'.format(lst)+'°'
        self.ax_mst.set_title('Mean solar time\n')
        self.ax_tst.set_title('True solar time\n')
        #self.ax_lst.rc('text', usetex=True)
        self.ax_lst.set_title('Local sidereal time\n')
        x, y = self.ax_lst.title.get_position()
        font = self.ax_lst.title.get_fontsize()
        #plt.suptitle(x=x, y=y+1, t=s)#, fontsize=font-5)
        #self.ax_lst.text(x=x, y=y, s=s, fontsize=font-5)


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
        
        mst = c.mean_solar_time
        tst = c.true_solar_time
        lst = c.lst
        
        mst_theta_h, mst_theta_m, mst_theta_s = self.__angles(mst)
        tst_theta_h, tst_theta_m, tst_theta_s = self.__angles(tst)
        lst_theta_h, lst_theta_m, lst_theta_s = self.__angles(lst)

        self.ax_mst = self.__plot(self.ax_mst, mst_theta_h, mst_theta_m, mst_theta_s)
        self.ax_tst = self.__plot(self.ax_tst, tst_theta_h, tst_theta_m, tst_theta_s)
        self.ax_lst = self.__plot(self.ax_lst, lst_theta_h, lst_theta_m, lst_theta_s)

        self.__set_titles(c.lst_deg)

        self.ax_mst = self.__config(self.ax_mst)
        self.ax_tst = self.__config(self.ax_tst)
        self.ax_lst = self.__config(self.ax_lst)


        self.ax_lst.text(
            x=np.pi*1.9, y=0.8,
            s='{0:.2f}'.format(c.lst_deg)+'°',
            fontsize='small')


ac = AnimClock(52.5)
ac.show()
