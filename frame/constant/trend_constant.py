class TrendEntity(object):

    def __init__(self, trend_name, trend_score):
        self.trend_name = trend_name
        self.trend_score = trend_score


class Trend(object):
    """
    趋势类型
    NO_CHANGE: 无变化
    UP: 上涨
    DOWN: 下跌
    UNKNOWN: 未知
    """
    NONE = TrendEntity("NO_CHANGE", 0.5)
    UP = TrendEntity("UP", 1.0)
    DOWN = TrendEntity("DOWN", 0.0)
    UNKNOWN = TrendEntity("UNKNOWN", 0.5)
