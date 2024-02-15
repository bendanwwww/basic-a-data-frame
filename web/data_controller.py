import json
import sys

from frame.constant.backtest_constant import Backtest

sys.path.append('../basic-a-data-frame')

from flask import Flask, request

from frame.constant.code_collection_constant import CodeCollection
from frame.constant.strategy_constant import Strategy
from frame.data.data_choose.data_choose import DataChoose

app = Flask(__name__)

data_choose_service = DataChoose()

# 量化策略列表
@app.route('/commonTool/getStrategyList')
def get_strategy_list():
    res_list = []
    for v in Strategy.strategy_dict.values():
        res_list.append(v.strategy_name)
    return json.dumps(res_list)

# 量化策略回测
@app.route('/commonTool/strategyBacktest')
def strategy_backtest():
    backtest = request.args.get("backtest", default='simple_effect')
    backtest_day = int(request.args.get("backtestDay", default='180'))
    strategy = request.args.get("strategy")
    code_collection = request.args.get("codeCollection")
    if strategy not in Strategy.strategy_dict or code_collection not in CodeCollection.code_collection_dict:
        return json.dumps([])
    res_table = Backtest.backtest_dict[backtest](Strategy.strategy_dict[strategy].strategy_func, CodeCollection.code_collection_dict[code_collection], backtest_day)
    return json.dumps(res_table.to_dict(orient='list'))

# 选择股票
@app.route('/commonTool/chooseData')
def choose_data():
    strategy = request.args.get("strategy")
    code_collection = request.args.get("codeCollection")
    if strategy not in Strategy.strategy_dict or code_collection not in CodeCollection.code_collection_dict:
        return json.dumps([])
    res_list = data_choose_service.choose_data(Strategy.strategy_dict[strategy].strategy_func, CodeCollection.code_collection_dict[code_collection])
    return json.dumps(res_list)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8092)
