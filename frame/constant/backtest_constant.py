from frame.backtest.effect_backtest import EffectBacktest


class BacktestEntity(object):

    def __init__(self, backtest_name, backtest_func):
        self.backtest_name = backtest_name
        self.backtest_func = backtest_func


class Backtest(object):
    """
    回测类型
    """
    SIMPLE_EFFECT = BacktestEntity('simple_effect', EffectBacktest().simple_effect_backtest)

    backtest_dict = {'simple_effect': SIMPLE_EFFECT.backtest_func}

