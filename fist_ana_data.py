import numpy as np
import pandas as pd

#异常数据清除
#data为narray格式
def findnan(data):
    index = np.where(data > 32000)
    data[index] = 1
    index = np.where(data > 31000)
    data[index] = data[index] - 31000
    index = np.where(data > 30000)
    data[index] = data[index] - 30000
    return data/10
#找出所需要的站点
#data为dataframe格式，要求站点一列为['station']
def choose_stations(data, stations):
    data = data.loc[stations]
    return data


# 找出所需要的年份
#data为dataframe格式，要求年份一列为['year']
def choose_year(data, sy, ey, index_name):
    data = data[(data['year'] >= sy) & (data['year'] <= ey)]
    return data

rowdata = pd.read_csv(r'D:\a_postgraduate\changjiang\data\PRE.txt', delim_whitespace=True, header=None, index_col=0, usecols=[0,1,2,4,5,6,7], names=['station','lat','lon','year','month','day','pre'])
station = pd.read_csv(r'D:\a_postgraduate\changjiang\data\station_with_ll.csv', usecols=[0], skiprows=[0], header=None)
data = choose_stations(rowdata, np.array(station).flatten())

data = choose_year(data, 1983, 2017, 'pre')
print(len(data.index.unique()))
data['pre'] = findnan(np.array(data['pre']))
print(len(data.index.unique()))
data.to_csv('resultdata.csv')




