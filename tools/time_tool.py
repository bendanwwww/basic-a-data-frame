import datetime
import time

import tools

data_format1 = "%Y-%m-%d"


def get_today():
    now_time = datetime.datetime.now()
    return now_time.strftime(data_format1)


def get_last_n_day(last_days, start_day_str=None):
    if start_day_str is None:
        start_day_str = tools.time_tool.get_today()
    start_day_array = time.strptime(start_day_str, data_format1)
    start_day_timestamp = int(time.mktime(start_day_array))
    last_day_ago_timestamp = start_day_timestamp - last_days * 24 * 60 * 60
    return time.strftime(data_format1, time.localtime(last_day_ago_timestamp))

