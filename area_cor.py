from netCDF4 import Dataset
import numpy as np
from scipy.stats.stats import pearsonr
import plotcor
import statsmodels.api as sm

def detime(sy, ey, month, dsy):
    sn = (sy - dsy) * 12
    en = (ey + 1 - dsy) * 12
    time = []
    for i in month:
        mtime = list(range(sn+i-1, en, 12))
        time.append(mtime)
    return time

def dell(data, lons, lats, slat, elat, slon, elon):
    ixlat = [int(np.argwhere((lats[:] == slat))), int(np.argwhere((lats[:] == elat)))]
    ixlon = [int(np.argwhere((lons[:] == slon))), int(np.argwhere((lons[:] == elon)))]
    areadata = data[:, min(ixlat):max(ixlat)+1, min(ixlon):max(ixlon)+1]
    arealons = lons[min(ixlon):max(ixlon)+1]
    arealats = lats[min(ixlat):max(ixlat)+1]

    return areadata, arealons, arealats


def verdata(data, pc, sy, ey, month, dsy):
    dtime = detime(sy, ey, month, dsy)
    ix = np.ix_(dtime[0])
    msst9 = data[ix]  ##########################
    ix = np.ix_(dtime[1])
    msst10 = data[ix] #######################################

    msst = (msst9+msst10)/2

    cordata = np.empty(msst[0].shape)
    r2 = np.empty(msst[0].shape)
    for ilat in range(len(msst[0, :, 0])):
        for ilon in range(len(msst[0, 0, :])):
            w, p = fit_line(msst[:, ilat, ilon], pc)
            cordata[ilat, ilon] = w
            r2[ilat, ilon] = p

    cordata[np.isnan(cordata[:, :])] = 0
    delcordata = cordata.copy()
    delcordata[np.where(r2[:, :] > 0.01)] = 0
    return cordata, delcordata

def fit_line(x, y):
    x = sm.add_constant(x)  # 线性回归增加常数项 y=kx+b
    regr = sm.OLS(y, x)  # 普通最小二乘模型，ordinary least square model
    res = regr.fit()
    pvalue = res.pvalues
    w = res.params
    return w[1], pvalue[1]


def choose(csst=1, cuwnd=1, col='bw'):
    for i in range(2):
        if csst == 1:
            ncin = Dataset('sst.mnmean.v4.nc', 'r')
            sst = ncin.variables['sst'][:]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()

            sst, lons, lats = dell(sst, lons, lats, 40, -40, 50, 130)

            data, deldata = verdata(sst, pc[i], sy, ey, month, 1854)
            # print(np.max(data), np.min(data))
            a = plotcor.plotcors(data, deldata, lons, lats, sy, ey, 'sst  pc%i'%(i+1), col, ll='sst')

        if cuwnd == 1:
            ncin = Dataset('uwnd.mon.mean.nc', 'r')
            uwnd200 = ncin.variables['uwnd'][:, 9, :, :]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()
            # np.savetxt('uwind2.txt',uwnd200[0])
            # np.savetxt('uwind3.txt', uwnd200[1])
            uwnd200, lons, lats = dell(uwnd200, lons, lats, 20, 60, 60, 150)
            data, deldata = verdata(uwnd200, pc[i], sy, ey, month, 1948)

            a = plotcor.plotcors(data, deldata, lons, lats, sy, ey, 'uwind200 pc%i'%(i+1), col)
    return


month = [9, 10]
sy = 1983
ey = 2016

pc1 = np.loadtxt('pc1  %s.txt'%(str(sy) + '--' + str(ey)))
pc2 = np.loadtxt('pc2  %s.txt'%(str(sy) + '--' + str(ey)))
pc = [pc1, pc2]

a = choose(csst=1, cuwnd=0,col='bw')