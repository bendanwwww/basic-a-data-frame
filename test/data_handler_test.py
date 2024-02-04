from futu import KLType
import numpy as np

from frame.backtest.effect_backtest import EffectBacktest
from frame.constant.strategy_constant import Strategy
from frame.data.data_service.data_service import DataService
from frame.strategy.simple_strategy import SimpleStrategy


def test1():
    data_service = DataService()
    test_k_day_data = data_service.get_history_kline_with_cache('US.TAL', '2023-12-29', '2023-12-29', KLType.K_DAY)
    print(test_k_day_data)


def test2():
    y_true = np.array([1.0, 5.0, 10.0, -21.0])
    # y_pred = np.array([1.0, 4.5, 3.5, 5.0, 8.0, 4.5, 1.0])
    print(np.mean(y_true)) #求均值 -1.25
    print(np.var(y_true)) #方差 ((1+1.25)^2+(5+1.25)^2+(10+1.25)^2+(-21+1.25)^2)/4=140.1875
    print(np.std(y_true)) #标准差
    # print(metrics.mean_squared_error(y_true, y_pred)) # 求MSE
    # print(np.sqrt(metrics.mean_squared_error(y_true, y_pred))) #求RMSE


def test3():
    simple_strategy = SimpleStrategy()
    last_thirty_ma_trend, last_three_ma_trend, trend = simple_strategy.ma_simple_strategy("US.TAL")
    print('last_thirty_ma_trend: ' + str(last_thirty_ma_trend) + ', last_three_ma_trend: ' + str(last_three_ma_trend) + ', trend: ' + trend)


def test4():
    effect_backtest = EffectBacktest()
    backtest_data = effect_backtest.simple_effect_backtest(Strategy.MA_SIMPLE.strategy_func)
    print(backtest_data)


test4()
