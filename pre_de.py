# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 15:59:59 2018

@author: circle
"""

import numpy as np

import pandas as pd

from pandas import DataFrame
np.set_printoptions(suppress=True)
pd.set_option('max_colwidth',200)

def findmonth(station, data):
    translist = []
    Adata = DataFrame()
    for i, sta in enumerate(station):
        trans = data.loc[sta]
        season = trans[(trans[5]==9)|(trans[5]==10)]
        translist.append(season)
    Adata = Adata.append(translist)

    Adata.to_csv('predata.csv')
    return


def de(A, x, y, z, t):
    A = A[A['l'] > x]
    A = A[A['l'] < y]
    A = A[A['s'] < t]
    A = A[A['s'] > z]
    return A


data = pd.read_excel('data.xls', skiprows=[1])
A = de(data, 24, 36, 90, 112)




    
    