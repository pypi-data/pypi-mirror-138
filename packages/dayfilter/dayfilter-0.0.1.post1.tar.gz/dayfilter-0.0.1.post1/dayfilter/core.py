import pytz
from suntime import Sun
from datetime import timezone, timedelta

# TODO:
# 1. No need to make sr and ss if we already have the data
# 2. Reimplement suntime.Sun() for speed and because it use LGPL License
# 3. Make a class that will store latitude, longitude, and time_zone
# 4. Embed sun to the class

class DayFilter():
    def __init__(self, latitude, longitude, time_zone, strategy='daytime', ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
        self.sun = Sun(latitude, longitude)
        self.tz = timezone(timedelta(hours=time_zone))

        if strategy == 'daytime':
            self.f = _is_daytime
        elif strategy == 'nighttime':
            self.f = _is_nighttime
        else:
            msg = f"Unknown value of '{strategy}' for strategy!"
            raise ValueError(msg)
    
        self.ceil_sr = ceil_sr,
        self.floor_sr = floor_sr,
        self.ceil_ss = ceil_ss, 
        self.floor_ss = floor_ss

    def filter(self, df):
        idx = self.get_indices(df.index)
        return df.iloc[idx]

    def get_indices(self, ds):
        return [i for i, x in enumerate(self.evaluate(ds)) if x]

    def evaluate(self, ds):
        return [self.f(ds_, self.sun, self.tz, self.ceil_sr, self.floor_sr, self.ceil_ss, self.floor_ss) for ds_ in ds]

    def update_location(self, latitude, longitude, time_zone):
        self.sun = Sun(latitude, longitude)
        self.tz = timezone(timedelta(hours=time_zone))

    def update_time_roundong(self, ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
        self.ceil_sr = ceil_sr,
        self.floor_sr = floor_sr,
        self.ceil_ss = ceil_ss, 
        self.floor_ss = floor_ss

    def update_strategy(self, strategy='daytime'):
        if strategy == 'daytime':
            self.f = are_daytimes
        elif strategy == 'nighttime':
            self.f = are_nighttimes
        else:
            msg = f"Unknown value of '{strategy}' for strategy!"
            raise ValueError(msg)

def are_nighttimes(ds, latitude, longitude, time_zone, ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
    sun = Sun(latitude, longitude)
    tz = timezone(timedelta(hours=time_zone))
    return [_is_nighttime(ds_, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss) for ds_ in ds]

def is_nighttime(ds, latitude, longitude, time_zone, ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
    sun = Sun(latitude, longitude)
    tz = timezone(timedelta(hours=time_zone))
    return _is_nighttime(ds, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss)

def _is_nighttime(ds, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss):
    sr, ss = get_sr_ss(ds, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss)
    if sr <= ds < ss:
        return False
    else:
        return True

def are_daytimes(ds, latitude, longitude, time_zone, ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
    sun = Sun(latitude, longitude)
    tz = timezone(timedelta(hours=time_zone))
    return [_is_daytime(ds_, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss) for ds_ in ds]

def is_daytime(ds, latitude, longitude, time_zone, ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
    sun = Sun(latitude, longitude)
    tz = timezone(timedelta(hours=time_zone))
    return _is_daytime(ds, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss)

def _is_daytime(ds, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss):
    sr, ss = get_sr_ss(ds, sun, tz, ceil_sr, floor_sr, ceil_ss, floor_ss)
    if sr <= ds < ss:
        return True
    else:
        return False

def get_sr_ss(ds_, sun, tz, ceil_sr=False, floor_sr=False, ceil_ss=False, floor_ss=False):
    # sr and ss have precision up to minute, thus ceil and floor only on hour
    sr = sun.get_sunrise_time(ds_).astimezone(tz).replace(tzinfo=None)
    ss = sun.get_sunset_time(ds_).astimezone(tz).replace(tzinfo=None)
    if ceil_sr:
        sr = ceil_date_hour(sr)
    elif floor_sr:
        sr = floor_date_hour(sr)
    if ceil_ss:
        ss = ceil_date_hour(ss)
    elif floor_ss:
        ss = floor_date_hour(ss)
    return sr, ss

def ceil_date_hour(dt):
    # sr and ss have precision up to minute, thus ceil and floor only on hour
    return floor_date_hour(dt) + timedelta(hours=1)

def floor_date_hour(dt):
    # sr and ss have precision up to minute, thus ceil and floor only on hour
    return dt.replace(minute=0)

def get_indices(ds, latitude, longitude, time_zone, strategy='daytime', filter_params={}):
    if strategy == 'daytime':
        f = are_daytimes
    elif strategy == 'nighttime':
        f = are_nighttimes
    else:
        msg = f"Unknown value of '{strategy}' for strategy!"
        raise ValueError(msg)
    
    return [i for i, x in enumerate(f(ds, latitude, longitude, time_zone, **filter_params)) if x]

    # from itertools import compress
    # res = f(ds, latitude, longitude, time_zone, **filter_params)
    # return list(compress(range(len(res)), res))
    # return compress(range(len(res)), res) # generator
    
    # import numpy as np
    # return np.where(f(ds, latitude, longitude, time_zone, **filter_params))[0]