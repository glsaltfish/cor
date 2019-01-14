import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame

#单个z计算
def mkz(data):
    n=len(data)
    s=0
    for k in range(n-1):
        for j in range(k+1,n):
            if data[j] > data[k]:
                s = s+1
            else:
                s=s+0
    if s != 0:
        es = n*(n-1)/4.0
        var = n*(n-1)*(2*n+5)/72.0
        z = (s-es)/(var**0.5)
    else:
        z = 0
        es = 111111
        var = 111111
    return z

def mkmu(data):
    n = len(data)
    uf = np.empty(n-1)
    ub = np.empty(n-1)
    ub_data = data[::-1]
    for k in range(1, n):
        uf[k-1] = mkz(data[0:k+1])
        ub[k-1] = mkz(ub_data[0:k+1])
    ub = -ub[::-1]
    return uf, ub


def plot(time, uf, ub, title, xlabel, ylabel):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(time, uf, label='UF', color='k', linestyle='-.', marker='o')
    plt.plot(time, ub, label='UB', color='k', linestyle='--', marker='v', alpha=0.5)

    ax.axhline(0, color='k')
    ax.axhline(1.96, color='k', linestyle='--', alpha=0.5,label='α=0.05')
    ax.axhline(-1.96, color='k', linestyle='--', alpha=0.5)
    plt.legend()
    plt.title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.show()
    # plt.savefig('%s.png' % (type1 + ' ' + level + ' ' + season))

    return

dels = ''
data = pd.read_csv('year_sum%s.csv'%dels, index_col=[0])
ave = data.groupby('year').mean()

print(ave.shape)

uf,ub = mkmu(np.array(ave['per']))
print(len(uf))

c=plot2(range(1961,2017),uf,ub,dels)

        


