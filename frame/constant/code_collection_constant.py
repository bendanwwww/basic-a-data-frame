from frame.data.static_conf.read import read_csv


class ReadCodeCollection(object):
    def __init__(self, collection_name, code_constant):
        self.collection_name = collection_name
        self.code_constant = code_constant

    def get_data(self):
        return read_csv(self.code_constant)


class CodeCollection(object):

    """
    数据候选集
    TECHNOLOGY_CODE: US 科技类股票代码 113
    """
    US_TECHNOLOGY_CODE = ReadCodeCollection('科技类股票代码', '../frame/data/static_conf/technology_code.csv')

    code_collection_dict = {'technology': US_TECHNOLOGY_CODE}

