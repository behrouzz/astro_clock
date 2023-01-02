from datetime import datetime, timedelta, time
from hypatie.time import get_lst, get_noon, solar_time


class Clock:
    def __init__(self, t, lon=0, eot_df=None):
        self.t = t
        self.lon = lon
        self.mean_solar_time, self.true_solar_time = \
                solar_time(t=self.t, lon=self.lon, eot_df=eot_df)
        self.noon = get_noon(t=self.t, lon=self.lon, eot_df=eot_df)
        self.eot = (self.mean_solar_time - self.true_solar_time).total_seconds()/60
        self.eot_str = self.__format_eot()
        self.lst_deg = get_lst(self.t, self.lon)
        self.lst = self.__format_lst()

    def __format_lst(self):
        td = timedelta(hours=self.lst_deg/15)
        a = str(td).split(':')
        h = int(a[0])
        m = int(a[1])
        s = int(a[-1].split('.')[0])
        ms = int(a[-1].split('.')[1])
        return time(h,m,s,ms)


    def __format_eot(self):
        sign = '-' if self.eot<0 else '+'
        td = timedelta(minutes=abs(self.eot))
        a = str(td).split(':')
        h = int(a[0])
        m = int(a[1])
        s = int(a[-1].split('.')[0])
        ms = int(a[-1].split('.')[1])
        minsec = str(time(h,m,s,ms))[3:]#.split('.')[0]
        return sign + minsec

