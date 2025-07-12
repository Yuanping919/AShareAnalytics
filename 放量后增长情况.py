"""
研究放量后第一个涨幅的大小：指当日成交量>=前一日成交量二倍
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

infos = pd.read_excel('股票名称代码映射.xlsx')
new_info = infos[~infos['代码'].str.contains('BJ')&(~infos['股票名称'].str.contains('ST'))]

close_data = pd.read_excel("全市场收盘价成交量.xlsx", sheet_name='Close')
vol_data = pd.read_excel('全市场收盘价成交量.xlsx', sheet_name='VOL')

close_data['日期'] = pd.to_datetime(close_data['日期'])
vol_data['日期'] = pd.to_datetime(vol_data['日期'])

close_data.set_index('日期', inplace=True)
vol_data.set_index('日期', inplace=True)

close_data = close_data[new_info['股票名称']]
vol_data = vol_data[new_info['股票名称']]

ret_data = close_data/close_data.shift(1) - 1


class VolBoom:
    def __init__(self, vol_multiple=2, time_window=10):
        self.vol_multiple = vol_multiple
        self.time_window = time_window
        self.vol_enlarge = None
        self.upward_ret = None
        self.con_fulfilled = None
        self.forward_ret = None
        self.result = None
        self.apply_condition()

    def apply_condition(self):
        self.vol_enlarge = vol_data > vol_data.shift(1) * self.vol_multiple
        self.upward_ret = ret_data > 0
        self.con_fulfilled = self.vol_enlarge & self.upward_ret
        self.forward_ret =  close_data.shift(-self.time_window)/close_data - 1
        temp = self.forward_ret.where(self.con_fulfilled)
        self.result = temp.stack()

    def plot_hist(self):
        plt.figure(figsize=(10, 6))

        # 方法1：使用 matplotlib 的 hist()
        useful_values = self.result.reset_index(drop=True)
        sns.histplot(useful_values, kde=True, color='royalblue', edgecolor='black')
        plt.title(f'放量{self.vol_multiple}倍，{self.time_window}日后收益率分布')
        plt.xlabel('数值')
        plt.ylabel('频数')
        # plt.grid(axis='y', alpha=0.02)
        plt.show()


volboom2_10 = VolBoom(vol_multiple=2, time_window=10)
volboom2_10.plot_hist()




# vol_enlarge = vol_data > vol_data.shift(1)*2
# upward = ret_data > 0
# filter_df = (vol_enlarge & upward)
#
# forward_ret = close_data.shift(10)/close_data - 1
#
# result = forward_ret.where(filter_df)



