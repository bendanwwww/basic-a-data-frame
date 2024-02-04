class CacheEntity(object):
    def __init__(self, cache_key, start_timestamp, end_timestamp, data_table):
        self.cache_key = cache_key
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.data_table = data_table


class DataCache(object):
    def __init__(self):
        self.cache_dict = {}

    # 缓存 key 是否完整
    def data_contains(self, cache_key, start_timestamp, end_timestamp):
        if cache_key not in self.cache_dict:
            return False
        data = self.cache_dict[cache_key]
        # 判断时间
        if data.start_timestamp > start_timestamp or data.end_timestamp < end_timestamp:
            return False
        return True

    # 根据 key 获取时间范围内的数据表
    def get_data_by_code(self, cache_key, start_timestamp, end_timestamp):
        if not self.data_contains(cache_key, start_timestamp, end_timestamp):
            return None
        data = self.cache_dict[cache_key]
        res = data.data_table[(data.data_table.time_key_timestamp >= start_timestamp) & (data.data_table.time_key_timestamp <= end_timestamp)]
        return res.reset_index(drop=True)

    # 新增 & 更新缓存
    def data_refresh(self, cache_key, start_timestamp, end_timestamp, data_table):
        data = CacheEntity(cache_key, start_timestamp, end_timestamp, data_table)
        self.cache_dict[cache_key] = data
