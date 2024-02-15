import pandas as pd


'''
time_key: 交易时间
buy_number: 买入股票个数
income: 收益
income_rate: 收益率
winning_rate: 胜率
cumulative_income: 累计收益
cumulative_income_rate: 累计收益率
cumulative_winning_rate: 累计胜率
'''
def get_test_result_table():
    return pd.DataFrame(columns=[
        'time_key',
        'buy_number',
        'income', 'income_rate', 'winning_rate',
        'cumulative_income', 'cumulative_income_rate', 'cumulative_winning_rate'])

