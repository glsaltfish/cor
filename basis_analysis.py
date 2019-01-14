import numpy as np
import pandas as pd
from pandas import DataFrame,Series

def basis_analysis(data):
    result = {}
    dfresult = DataFrame()
    mean = data['pre'].groupby(data['month']).sum()/35/80
    contribute_rate = (data['pre'].groupby(data['month']).sum())*100/(data['pre'].sum())
    std = data['pre'].groupby(data['month']).std()
    ske = data['pre'].groupby(data['month']).skew()
    cv = std/mean
    max = data['pre'].groupby(data['month']).idxmax()
    max_pre = data['pre'][max]
    max_year = data['year'][max]


    # data[data['pre'] == 0] = 999
    min = data['pre'].groupby(data['month']).idxmin()
    min_pre = data['pre'][min]
    min_year = data['year'][min]

    result['mean'] = mean
    result['contribute_rate'] = contribute_rate
    result['std'] = std
    result['skew'] = ske
    result['cv'] = cv
    result['max_pre'] = max_pre
    result['max_year'] = max_year
    result['min_pre'] = min_pre
    result['min_year'] = min_year


    dfresult['mean'] = mean
    dfresult['contribute_rate'] = contribute_rate
    dfresult['std'] = std
    dfresult['skew'] = ske
    dfresult['cv'] = cv
    dfresult['max_pre'] = np.array(max_pre)
    dfresult['max_year'] = np.array(max_year)

    # dfresult['min_pre'] = np.array(min_pre)
    # dfresult['min_year'] = np.array(min_year)
    return dfresult

'''默认显著性水平为0.05'''



data = pd.read_csv(r'D:\a_postgraduate\changjiang\data\data.csv')

# data['month'][(data['month'] == 11) | (data['month'] == 12) | (data['month'] == 1) | (data['month'] == 2) | (data['month'] == 3)] = 99
# data['month'][(data['month'] == 6) | (data['month'] == 7) | (data['month'] == 8)] = 77
# data['month'][(data['month'] == 4) | (data['month'] == 5)] = 44

data[(data['month'] == 11) | (data['month'] == 12) | (data['month'] == 1) | (data['month'] == 2) | (data['month'] == 3)].to_csv('data3.csv')
data[(data['month'] == 6) | (data['month'] == 7) | (data['month'] == 8)].to_csv('data2.csv')
data[(data['month'] == 4) | (data['month'] == 5)].to_csv('data1.csv')
