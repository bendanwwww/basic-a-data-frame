from futu import KLType

from frame.backtest.backtest_common import get_test_result_table
from frame.data.data_service.data_service import DataService
from tools.time_tool import get_last_n_day


class EffectBacktest(object):

    data_service = DataService()

    # 简单效果回测 默认回测 90 天样本
    # strategy_dict 策略函数集合 key: namespace value: strategy
    # code_collection 回测股票集合
    # buy_score 买入分数
    def simple_effect_backtest(self, strategy_dict, strategies_eval, code_collection, buy_score, test_day=None):
        res_table = get_test_result_table()
        test_codes = code_collection.get_data()
        if test_day is None:
            test_day = 90
        cumulative_buy_num = 0
        cumulative_income = 0.0
        cumulative_unit_income = 0.0
        cumulative_winning = 0.0
        for last_day_age in range(test_day, 1, -1):
            time_key = get_last_n_day(last_day_age - 1)
            buy_num = 0
            income = 0.0
            unit_income = 0.0
            winning = 0
            lose = 0
            for data in test_codes:
                # 股票代码
                code = data['code']
                # 遍历策略 计算分数
                namespace_dict = {}
                for strategy_var in strategy_dict:
                    strategy_func = strategy_dict[strategy_var].strategy_func
                    namespace_dict[strategy_var] = strategy_func(code)
                # 最终得分
                final_score = eval(strategies_eval, namespace_dict)
                # 可以买入
                if final_score >= buy_score:
                    # 获取当天收盘价
                    data = self.data_service.get_history_kline_with_cache(code, time_key, time_key, KLType.K_DAY)
                    # 若当日未开盘, 直接跳过, 下一轮回测会命中
                    if data is None or len(data) == 0:
                        continue
                    code_open_price = data.iloc[-1]['open']
                    code_close_price = data.iloc[-1]['close']
                    income += code_close_price - code_open_price
                    cumulative_income += code_close_price - code_open_price
                    unit_income += income / code_open_price
                    cumulative_unit_income += income / code_open_price
                    buy_num += 1
                    cumulative_buy_num += 1
                    if code_open_price > code_close_price:
                        lose += 1
                    elif code_open_price < code_close_price:
                        winning += 1
                        cumulative_winning += 1
            if buy_num != 0:
                res_table.loc[len(res_table.index)] = [
                    time_key,
                    buy_num,
                    income, unit_income / buy_num, winning / buy_num,
                    cumulative_income, cumulative_unit_income / cumulative_buy_num, cumulative_winning / cumulative_buy_num
                ]

        return res_table
