from frame.constant.trend_constant import Trend


class DataChoose(object):

    def choose_data(self, strategy, code_collection):
        res_list = []
        choose_code_collection = code_collection.get_data()
        for data in choose_code_collection:
            # 股票代码
            code = data['code']
            # 执行策略
            trend = strategy(code)
            if trend == Trend.UP:
                res_list.append(code)
        return res_list
