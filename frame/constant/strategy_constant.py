from frame.strategy.simple_strategy import SimpleStrategy


class StrategyEntity(object):

    def __init__(self, strategy_name, strategy_func):
        self.strategy_name = strategy_name
        self.strategy_func = strategy_func


class Strategy(object):
    """
    策略类型
    """
    MA_SIMPLE = StrategyEntity('ma_simple', SimpleStrategy().ma_simple_strategy)

