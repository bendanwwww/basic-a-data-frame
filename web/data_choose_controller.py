import json
import sys

sys.path.append('../basic-a-data-frame')

from flask import Flask, request

from frame.constant.code_collection_constant import CodeCollection
from frame.constant.strategy_constant import Strategy
from frame.data.data_choose.data_choose import DataChoose

app = Flask(__name__)

data_choose_service = DataChoose()


@app.route('/commonTool/chooseData')
def choose_data():
    strategy = request.args.get("strategy")
    code_collection = request.args.get("codeCollection")
    if strategy not in Strategy.strategy_dict or code_collection not in CodeCollection.code_collection_dict:
        return []
    res_list = data_choose_service.choose_data(Strategy.strategy_dict[strategy], CodeCollection.code_collection_dict[code_collection])
    return json.dumps(res_list)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8092)
