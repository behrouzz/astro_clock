import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
from astro_clock import Clock


class AnimClock:
    def __init__(self, lon=0):
        self.lon = lon
        self.title_mst = 'Mean solar time\n'
        self.title_tst = 'True solar time\n'
        self.title_lst = 'Local sidereal time\n'
        self.fig = plt.figure()
        self.ax_mst = plt.subplot(131, projection='polar')
        self.ax_tst = plt.subplot(132, projection='polar')
        self.ax_lst = plt.subplot(133, projection='polar')
              

    def show(self):
        ani = FuncAnimation(self.fig, self.my_function, interval=1000)
        plt.tight_layout(pad=1, w_pad=0.9)
        plt.show()


    def angles(self, t):
        s = t.second
        m = t.minute + t.second/60 + (t.microsecond/1000000)/60
        h = t.hour + m/60
        theta_s = t.second * 6 * (np.pi/180)
        theta_m = m * 6 * (np.pi/180)
        theta_h = h * 30 * (np.pi/180)
        return theta_h, theta_m, theta_s


    def my_function(self, i):
        self.ax_mst.cla()
        self.ax_tst.cla()
        self.ax_lst.cla()

        
        t = datetime.utcnow()

        c = Clock(t, self.lon)
        
        mst = c.mean_solar_time
        tst = c.true_solar_time
        lst = c.lst
        
        mst_theta_h, mst_theta_m, mst_theta_s = self.angles(mst)
        tst_theta_h, tst_theta_m, tst_theta_s = self.angles(tst)
        lst_theta_h, lst_theta_m, lst_theta_s = self.angles(lst)

        r = 1
        
        self.ax_mst.plot([0, mst_theta_h], [0, 0.6*r], lw=5, c='b')
        self.ax_mst.plot([0, mst_theta_m], [0, 0.9*r], lw=2, c='b')
        self.ax_mst.plot([0, mst_theta_s], [0, r], lw=0.5, c='r')

        self.ax_tst.plot([0, tst_theta_h], [0, 0.6*r], lw=5, c='b')
        self.ax_tst.plot([0, tst_theta_m], [0, 0.9*r], lw=2, c='b')
        self.ax_tst.plot([0, tst_theta_s], [0, r], lw=0.5, c='r')

        self.ax_lst.plot([0, lst_theta_h], [0, 0.6*r], lw=5, c='b')
        self.ax_lst.plot([0, lst_theta_m], [0, 0.9*r], lw=2, c='b')
        self.ax_lst.plot([0, lst_theta_s], [0, r], lw=0.5, c='r')
        
        self.ax_mst.set_title(self.title_mst)
        self.ax_tst.set_title(self.title_tst)
        self.ax_lst.set_title(self.title_lst)

        
        self.ax_mst.set_rticks([])
        self.ax_tst.set_rticks([])
        self.ax_lst.set_rticks([])
        
        self.ax_mst.grid(False)
        self.ax_mst.set_theta_zero_location('N')
        self.ax_mst.set_theta_direction(-1)
        self.ax_mst.set_thetagrids(
            np.arange(12)*30,
            ['12'] + [str(i) for i in range(1,12)]
            )

        self.ax_tst.grid(False)
        self.ax_tst.set_theta_zero_location('N')
        self.ax_tst.set_theta_direction(-1)
        self.ax_tst.set_thetagrids(
            np.arange(12)*30,
            ['12'] + [str(i) for i in range(1,12)]
            )

        self.ax_lst.grid(False)
        self.ax_lst.set_theta_zero_location('N')
        self.ax_lst.set_theta_direction(-1)
        self.ax_lst.set_thetagrids(
            np.arange(12)*30,
            ['12'] + [str(i) for i in range(1,12)]
            )

        self.ax_lst.text(x=np.pi*1.9, y=0.8,
                         s='{0:.2f}'.format(c.lst_deg)+'°',
                     fontsize='small')


ac = AnimClock(52.5)
ac.show()
