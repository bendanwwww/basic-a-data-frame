import pandas as pd

from frame.constant.resource_constant import FUTU_DATA
from frame.data.data_service.data_cache import DataCache
from tools.time_tool import date_format1, date_format2, get_last_n_day, get_today


class DataService(object):
    # 对象缓存
    data_cache = DataCache()

    # 获取历史 k 线 使用缓存
    def get_history_kline_with_cache(self, code, start, end, ktype):
        cache_key = self.__get_history_kline_cache_key(code, ktype)
        # 时间戳转换
        start_timestamp = date_format1(start)
        end_timestamp = date_format1(end)
        # 取缓存
        if self.data_cache.data_contains(cache_key, start_timestamp, end_timestamp):
            return self.data_cache.get_data_by_code(cache_key, start_timestamp, end_timestamp)
        # 刷新缓存 默认 起始时间提早 365 天取值 结束时间为当前时间
        last_start = get_last_n_day(365, start)
        today_end = get_today()
        data = FUTU_DATA.get_history_kline(code, last_start, today_end, ktype)
        if data is None:
            return data
        # 添加时间戳列
        data['time_key_timestamp'] = data.apply(lambda d: date_format2(d['time_key']), axis=1)
        # 写入缓存
        last_start_timestamp = date_format1(last_start)
        today_end_timestamp = date_format1(today_end)
        self.data_cache.data_refresh(cache_key, last_start_timestamp, today_end_timestamp, data)
        return self.data_cache.get_data_by_code(cache_key, start_timestamp, end_timestamp)

    # 获取 历史 k 线 缓存 key
    def __get_history_kline_cache_key(self, code, ktype):
        return "{0}__{1}".format(code, ktype)
