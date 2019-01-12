from netCDF4 import Dataset
import numpy as np
from scipy.stats.stats import pearsonr
import plotcor

def detime(sy, ey, month, dsy):
    sn = (sy - dsy) * 12
    en = (ey + 1 - dsy) * 12
    time = []
    for i in month:
        mtime = list(range(sn+i-1, en, 12))
        time.append(mtime)
    return time

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
            a, b, w, sr2 = fit_line(msst[:, ilat, ilon], pc)
            cordata[ilat, ilon] = w
            r2[ilat, ilon] = sr2
    cordata[np.isnan(cordata[:, :])] = 0
    delcordata = cordata.copy()
    delcordata[np.where(r2[:, :] > 0.1)] = 0
    return cordata, delcordata

def fit_line(x_data, y_data):
    ivalid = np.logical_not(np.ma.getmaskarray(y_data))
    A = np.ones((np.ma.count(y_data), 2))
    A[:, 0] = x_data[ivalid]
    w = np.linalg.lstsq(A, y_data[ivalid])[0]
    yf = w[0]*x_data[ivalid]+w[1]
    coef = np.corrcoef(y_data, yf)[0, 1]
    print(coef)
    eqn = u'趋势方程 y=%.2fx+%.2f \n ${R^2}$=%5.3f' % (w[0], w[1], coef**2)
    return eqn, yf, w[0], coef**2



def choose(csst=1, chgt=1, cuwnd=1, col='bw'):
    for i in range(2):
        if chgt == 1:
            ncin = Dataset('hgt.mon.mean.nc', 'r')
            hgt850 = ncin.variables['hgt'][:,2,:,:]
            hgt500 = ncin.variables['hgt'][:,5,:,:]
            hgt300 = ncin.variables['hgt'][:,7,:,:]
            hgt100 = ncin.variables['hgt'][:,11,:,:]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()

            level = [hgt850, hgt500, hgt300, hgt100]
            levelname = ['hgt850', 'hgt500', 'hgt300', 'hgt100']
            for j in range(len(level)):
                data, deldata = verdata(level[j], pc[i], sy, ey, month, 1948)
                a = plotcor.plotcors(data, deldata, lons, lats, sy, ey, (levelname[j]+'pc%i'%(i+1)), col)

        if csst == 1:
            ncin = Dataset('sst.mnmean.nc', 'r')
            sst = ncin.variables['sst'][:]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()

            data, deldata = verdata(sst, pc[i], sy, ey, month, 1854)
            #print(np.max(data), np.min(data))
            a = plotcor.plotcors(data, deldata, lons, lats, sy, ey, 'sst  pc%i'%(i+1), col)

        if cuwnd == 1:
            ncin = Dataset('uwnd.mon.mean.nc', 'r')
            uwnd200 = ncin.variables['uwnd'][:,9,:,:]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()

            data, deldata = verdata(uwnd200, pc[i], sy, ey, month, 1948)
            a = plotcor.plotcors(data, deldata, lons, lats, sy, ey, 'uwind200 pc%i'%(i+1), col)
    return

month = [9, 10]
sy = 1983
ey = 2016

pc1 = np.loadtxt('pc1  %s.txt'%(str(sy) + '--' + str(ey)))
pc2 = np.loadtxt('pc2  %s.txt'%(str(sy) + '--' + str(ey)))
pc = [pc1, pc2]

a = choose(csst=1, chgt=1, cuwnd=1,col='bw')