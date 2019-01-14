from netCDF4 import Dataset
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
from scipy.stats.mstats import zscore

# 根据时间切割数据，返回切割好的数据
# 给出起始年份，终止年份，所需月份，以及数据本身的终止年份
# 可以算出其在序列中的位子，并返回位子信息
def de_time(data, sy, ey, month, dsy):
    sn = (sy - dsy) * 12
    en = (ey + 1 - dsy) * 12
    dtime = []
    for i in month:
        mtime = list(range(sn + i - 1, en, 12))
        dtime.append(mtime)

    ix = np.ix_(dtime[0])
    msst9 = data[ix]  ##########################
    ix = np.ix_(dtime[1])
    msst10 = data[ix]  #######################################
    msst = (msst9 + msst10) / 2
    return msst


# 根据经纬度切割数据，返回切割好的数据，和对应经纬度
def de_ll(data, lons, lats, slat, elat, slon, elon):
    ixlat = [int(np.argwhere((lats[:] == slat))), int(np.argwhere((lats[:] == elat)))]
    ixlon = [int(np.argwhere((lons[:] == slon))), int(np.argwhere((lons[:] == elon)))]
    areadata = data[min(ixlat):max(ixlat) + 1, min(ixlon):max(ixlon) + 1]
    arealons = lons[min(ixlon):max(ixlon) + 1]
    arealats = lats[min(ixlat):max(ixlat) + 1]
    return areadata, arealons, arealats

#计算数据空间点与pc的回归系数，返回回归系数矩阵
#给出对应的数据、pc，计算回归系数，以及信度。不满足信度的将会被视为0
def verdata(msst, pc, a):
    cordata = np.empty(msst[0].shape)
    r2 = np.empty(msst[0].shape)
    for ilat in range(len(msst[0, :, 0])):
        for ilon in range(len(msst[0, 0, :])):
            w, p = fit_line2(msst[:, ilat, ilon], pc)
            cordata[ilat, ilon] = w
            r2[ilat, ilon] = p
    # np.savetxt('cor.txt', cordata, fmt='%6.1f')
    # cordata[np.isnan(cordata[:, :])] = 0
    delcordata = cordata.copy()
    delcordata[np.where(r2[:, :] > 0.01)] = 0
    # np.savetxt('delcor.txt', delcordata, fmt='%6.1f')
    # np.savetxt('p.txt', r2)
    return cordata, delcordata


def fit_line(x, y):
    try:
        x = sm.add_constant(x)  # 线性回归增加常数项 y=kx+b
        regr = sm.OLS(y, x)  # 普通最小二乘模型，ordinary least square model
        res = regr.fit()
        pvalue = res.pvalues
        w = res.params
        pvalue1 = pvalue[1]
        w1 = w[1]
    except:
        pvalue1 = 1
        w1 = 999

    return w1, pvalue1

def fit_line1(x, y):
    data = np.append(x.T, y,axis=1)
    regr = LinearRegression()
    regr = regr.fit(data)
    pvalue = regr.pvalues
    w = regr.params
    return w[1], pvalue[1]


def fit_line2(x, y):
    (beta_coeff, intercept, rvalue, pvalue, stderr) = linregress(zscore(x), zscore(y))
    return beta_coeff,pvalue