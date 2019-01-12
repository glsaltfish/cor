# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 18:01:22 2018

@author: circle
"""

import numpy as np
import pandas as pd
from pandas import DataFrame,Series
np.set_printoptions(suppress=True)
pd.set_option('display.max_rows', None)

def flattenlist(x):
    x = np.array(x)
    x = x.flatten()
    return x

def findstations(station, staryear, endyear, starmonth, endmonth):
    sta = []
    year = []
    month = [9, 10]*(endyear+1-staryear)
    for i in station:
        sta.append([i] * (57*2))
    for i in range(staryear, endyear+1):
        year.append([i]*2)

    year = year*198
    month = month*198
    sta = flattenlist(sta)
    year = flattenlist(year)
    month = flattenlist(month)
    return sta, year, month

def allfindstations(station, staryear, endyear):
    sta = []
    year = []
    month = [9, 10]*(endyear+1-staryear)
    for i in station:
        sta.append([i] * (57*2))
    for i in range(staryear, endyear+1):
        year.append([i]*12)

    year = year*198
    month = month*198
    sta = flattenlist(sta)
    year = flattenlist(year)
    month = flattenlist(month)
    return sta, year, month



def indexname(station, year, month):
    name = []
    for i in range(len(station)):
        name.append('%s'%(str(int(station[i]))+str(year[i])+str(month[i])))
    return name

rowdata = pd.read_csv(r'D:\a_postgraduate\changjiang\data\pre.csv', index_col=[0])

station = pd.read_csv(r'D:\a_postgraduate\changjiang\data\station_with_ll.csv', usecols=[0])

sta, year, month = allfindstations(station, 1983, 2017)

findnan = DataFrame(year, index=sta, columns=['year'])
findnan['month'] = month
per = np.array([0]*(198*57*2))
pernan = Series(per.flatten(), index=indexname(sta, year, month))

perrowindex = indexname(np.array(rowdata.index), np.array(rowdata['year']), np.array(rowdata['month']))
perrow = Series(np.array(rowdata['per']), index=perrowindex)

fine = pernan+perrow
findnan['per'] = np.array(fine)


findnan.to_csv('try.csv')

