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

    def choose_data_with_strategys(self, strategy_dict, code_collection, buy_score):
        res_list = []
        choose_code_collection = code_collection.get_data()
        for data in choose_code_collection:
            # 股票代码
            code = data['code']
            # 最终得分
            final_score = 0.0
            # 遍历策略 计算分数
            for strategy in strategy_dict:
                strategy_func = strategy.strategy_func
                coefficient = strategy_dict[strategy]
                final_score += strategy_func(code) * coefficient
            # 可以买入
            if final_score >= buy_score:
                res_list.append(code)
        return res_list
