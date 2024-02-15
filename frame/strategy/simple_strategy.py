from futu import KLType

from frame.constant.trend_constant import Trend
import tools.time_tool
from frame.data.data_service.data_service import DataService


class SimpleStrategy(object):
    data_service = DataService()

    # 简单移动平均
    # 若 最近 30 个交易日 MA:10 曲线趋势向上 且 最近 3 交易日 MA:1 曲线趋势向下, 则下一个交易日预测上涨
    # 当 Σ(MAₙ - MA₍ₙ₋₁₎) > 0 趋势向上, Σ(MAₙ - MA₍ₙ₋₁₎) < 0 趋势向下, Σ(MAₙ - MA₍ₙ₋₁₎) = 0 趋势不变
    def ma_simple_strategy(self, code, start_day=None):
        if start_day is None:
            start_day = tools.time_tool.get_today()
        # 获取当前和 120 天前日期字符串
        last_n_day = tools.time_tool.get_last_n_day(120, start_day_str=start_day)
        # 获取前 120 天股票 天级别 k 线数据
        data = self.data_service.get_history_kline_with_cache(code, last_n_day, start_day, KLType.K_DAY)
        if data is None:
            return Trend.UNKNOWN
        # 计算每日平均价
        data['avg'] = data[['open', 'close']].mean(axis=1)
        # 计算 MA:10 数据
        last_thirty_ma_data = data['avg'].rolling(window=10).mean()
        # 计算 MA:1 数据
        last_three_ma_data = data['avg'].rolling(window=1).mean()
        # 计算 30 天 MA:10 曲线趋势
        last_thirty_ma_trend = 0
        for index in range(len(last_thirty_ma_data) - 1, 30, -1):
            last_thirty_ma_trend += last_thirty_ma_data[index] - last_thirty_ma_data[index - 1]
        # 计算 3 天 MA:1 曲线趋势
        last_three_ma_trend = 0
        for index in range(len(last_three_ma_data) - 1, 5, -1):
            last_three_ma_trend += last_three_ma_data[index] - last_three_ma_data[index - 1]
        if last_thirty_ma_trend > 0 and last_three_ma_trend < 0:
            return Trend.UP
        return Trend.UNKNOWN
