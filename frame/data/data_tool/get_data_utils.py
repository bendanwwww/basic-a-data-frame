import pandas as pd
from futu import RET_OK, OpenQuoteContext


class FuTuData(object):

    # 获取数据客户端
    futu_client = OpenQuoteContext(host='127.0.0.1', port=9001)

    page_size = 100

    # 获取历史 k 线
    def get_history_kline(self, code, start, end, ktype):
        # 分页查询信息
        ret, data, page_offset = self.futu_client.request_history_kline(code, start=start, end=end,
                                                                        max_count=self.page_size, ktype=ktype)
        if ret == RET_OK:
            res = data
        else:
            return None
        while page_offset is not None:
            ret, data, page_offset = self.futu_client.request_history_kline(code, start=start, end=end,
                                                                            max_count=self.page_size, ktype=ktype,
                                                                            page_req_key=page_offset)
            if ret == RET_OK:
                res = pd.concat([res, data], ignore_index=True)
            else:
                return None
        return res
