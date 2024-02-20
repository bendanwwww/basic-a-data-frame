import json
import sys

sys.path.append('../basic-a-data-frame')

from flask_cors import CORS
from frame.constant.backtest_constant import Backtest
from flask import Flask, request

from frame.constant.code_collection_constant import CodeCollection
from frame.constant.strategy_constant import Strategy
from frame.data.data_choose.data_choose import DataChoose

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

data_choose_service = DataChoose()

# 量化策略列表
@app.route('/commonTool/getStrategyList', methods=['GET'])
def get_strategy_list():
    res_list = []
    index = 0
    for k in Strategy.strategy_dict:
        res_list.append({
            'index': index,
            'strategy_code': k,
            'strategy_name': Strategy.strategy_dict[k].strategy_name,
        })
        index += 1
    return {'strategy': res_list}

# 量化策略回测
# strategies: [[strategy_str, score], [], ...]
@app.route('/commonTool/strategyBacktest', methods=['POST'])
def strategy_backtest():
    params = json.loads(request.get_data())
    backtest = 'simple_effect'
    backtest_day = 180
    if "backtest" in params:
        backtest = params["backtest"]
    if "backtestDay" in params:
        backtest = int(params["backtestDay"])
    strategies = params["strategyInfos"]
    code_collection = params["codeCollection"]
    buy_score = params["buyScore"]
    if code_collection not in CodeCollection.code_collection_dict:
        return json.dumps([])
    strategy_dict = {}
    for strategy_list in strategies:
        strategy_str = strategy_list[0]
        if strategy_str not in Strategy.strategy_dict:
            return json.dumps([])
        strategy = Strategy.strategy_dict[strategy_str]
        strategy_dict[strategy] = strategy_list[1]
    res_table = Backtest.backtest_dict[backtest].backtest_func(strategy_dict, CodeCollection.code_collection_dict[code_collection], buy_score, backtest_day)
    return json.dumps(res_table.to_dict(orient='list'))

# 选择股票 单策略
@app.route('/commonTool/chooseData', methods=['POST'])
def choose_data():
    params = json.loads(request.get_data())
    strategy_str = params["strategy"]
    buy_score = params["buyScore"]
    code_collection = params["codeCollection"]
    if strategy_str not in Strategy.strategy_dict or code_collection not in CodeCollection.code_collection_dict:
        return json.dumps([])
    strategy = Strategy.strategy_dict[strategy_str]
    res_list = data_choose_service.choose_data(strategy, CodeCollection.code_collection_dict[code_collection], buy_score)
    return json.dumps(res_list)

# 选择股票 多策略组合
# strategies: [[strategy_str, score], [], ...]
@app.route('/commonTool/chooseDataWithStrategys', methods=['POST'])
def choose_data_with_strategys():
    params = json.loads(request.get_data())
    strategies = params["strategyInfos"]
    buy_score = params["buyScore"]
    code_collection = params["codeCollection"]
    if code_collection not in CodeCollection.code_collection_dict:
        return json.dumps([])
    strategy_dict = {}
    for strategy_list in strategies:
        strategy_str = strategy_list[0]
        if strategy_str not in Strategy.strategy_dict:
            return json.dumps([])
        strategy = Strategy.strategy_dict[strategy_str]
        strategy_dict[strategy] = strategy_list[1]
    res_list = data_choose_service.choose_data_with_strategys(strategy_dict, CodeCollection.code_collection_dict[code_collection], buy_score)
    return json.dumps(res_list)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8092)
