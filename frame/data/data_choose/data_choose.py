from frame.constant.strategy_constant import Strategy


class DataChoose(object):

    def choose_data(self, strategy, code_collection, buy_score):
        res_list = []
        strategy_func = strategy.strategy_func
        choose_code_collection = code_collection.get_data()
        for data in choose_code_collection:
            # 股票代码
            code = data['code']
            # 执行策略
            score = strategy_func(code)
            # 可以买入
            if score >= buy_score:
                res_list.append(code)
        return res_list

    # strategy_dict key: namespace value: strategy
    def choose_data_with_strategys(self, strategy_dict, strategies_eval, code_collection, buy_score):
        res_list = []
        choose_code_collection = code_collection.get_data()
        for data in choose_code_collection:
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
                res_list.append(code)
        return res_list
