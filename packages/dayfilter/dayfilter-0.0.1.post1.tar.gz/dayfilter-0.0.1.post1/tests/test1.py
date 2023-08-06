# test1a
from datetime import datetime

date_string = '2010-01-01-16:58:30.00000'
date_datetime = datetime.strptime(date_string, '%Y-%m-%d-%H:%M:%S.%f')

# WASHINGTON DC DULLES INT'L AR [STERLING - ISIS], VA. data
latitude = 38.98
longitude = -77.47
time_zone = -5

is_daytime(date_datetime, latitude, longitude, time_zone)

# test1b
from dayfilter import DayFilter
import pandas as pd
from datetime import datetime

# WASHINGTON DC DULLES INT'L AR [STERLING - ISIS], VA. data
latitude = 38.98
longitude = -77.47
time_zone = -5

f = DayFilter(latitude, longitude, time_zone)

# df1
date_strings = [
    '2010-01-01-05:58:42.00000',
    '2010-01-01-12:59:32.00000',
    '2010-01-01-13:42:22.00000',
    '2010-01-01-14:39:25.00000',
    '2010-01-01-15:21:45.00000',
    '2010-01-01-18:10:21.00000',
    '2010-01-02-15:12:30.00000',
]
date_format = '%Y-%m-%d-%H:%M:%S.%f'
date_datetimes = [datetime.strptime(date_string, date_format) for date_string in date_strings]
val = [1,2,3,3,2,1]

df1 = pd.DataFrame(index=date_datetimes, data=[1,2,3,3,2,1,0])

df1_ = f.filter(df1)

# df2
date_strings = [
    '2010-01-01-05:58:42.00000',
    '2010-01-01-06:59:22.00000',
    '2010-01-01-13:22:23.00000',
    '2010-01-01-14:54:55.00000',
    '2010-01-01-15:31:45.00000',
    '2010-01-02-11:12:22.00000',
    '2010-01-02-15:12:32.00000',
]
date_format = '%Y-%m-%d-%H:%M:%S.%f'
date_datetimes = [datetime.strptime(date_string, date_format) for date_string in date_strings]
val = [1,2,3,4,5,6]

df2 = pd.DataFrame(index=date_datetimes, data=[1,2,3,3,2,1,0])

df2_ = f.filter(df2)
