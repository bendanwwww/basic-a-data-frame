import pandas as pd
from futu import KLType

from frame.constant.trend_constant import Trend
from frame.data.data_service.data_service import DataService
from tools.time_tool import get_last_n_day


class EffectBacktest(object):

    data_service = DataService()

    # 简单效果回测 回测 90 天样本
    def simple_effect_backtest(self, test_codes, strategy_func, test_day=None):
        # TODO 需要增加列
        res_table = pd.DataFrame(columns=['time_key', 'income', 'income_rate', 'winning_rate'])
        if test_day is None:
            test_day = 90
        for last_day_age in range(test_day, 1, -1):
            time_key = get_last_n_day(last_day_age - 1)
            income = 0.0
            unit_income = 0.0
            winning = 0
            lose = 0
            all = 0
            for data in test_codes:
                # 股票代码
                code = data['code']
                # 根据策略判断是否买入
                trend = strategy_func(code, get_last_n_day(last_day_age))
                # 可以买入
                if trend == Trend.UP:
                    # 获取当天收盘价
                    data = self.data_service.get_history_kline_with_cache(code, time_key, time_key, KLType.K_DAY)
                    # 若当日未开盘, 直接跳过, 下一轮回测会命中
                    if len(data) == 0:
                        continue
                    code_open_price = data.iloc[-1]['open']
                    code_close_price = data.iloc[-1]['close']
                    income += code_close_price - code_open_price
                    unit_income += income / code_open_price
                    all += 1
                    if code_open_price > code_close_price:
                        lose += 1
                    elif code_open_price < code_close_price:
                        winning += 1
            # if all == 0:
            #     res_table.loc[len(res_table.index)] = [time_key, income, None, None]
            # else:
            #     res_table.loc[len(res_table.index)] = [time_key, income, unit_income / all, winning / all]
            if all != 0:
                res_table.loc[len(res_table.index)] = [time_key, income, unit_income / all, winning / all]

        return res_table
