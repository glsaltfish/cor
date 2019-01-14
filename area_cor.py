from netCDF4 import Dataset
import numpy as np
from scipy.stats.stats import pearsonr
import plotcor
import calculate_corr
import statsmodels.api as sm

#col = 'bw'or'color', ranges='all'or'area'


def choose(csst=1, cuwnd=1, col='bw', ranges='all',a=0.01):
    for i in range(2):
        if csst == 1:
            #读取数据
            ncin = Dataset('sst.mnmean.v4.nc', 'r')
            sst = ncin.variables['sst'][:]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()
            #分割时间
            sst = calculate_corr.de_time(sst, sy, ey, month, 1854)
            #计算回归系数
            data, deldata = calculate_corr.verdata(sst, pc[i], a)
            # np.savetxt('data0.txt', data)
            #分割纬度
            if ranges == 'area':
                data, lons, lats = calculate_corr.de_ll(data, lons, lats, 40, -40, 50, 130)
                deldata, lons, lats = calculate_corr.de_ll(deldata, lons, lats, 40, -40, 50, 130)
            #绘图
            # np.savetxt('data.txt', data)
            # np.savetxt('dedata.txt', deldata)
            a = plotcor.plotcors(data, deldata, lons, lats, col=col, ll='sst', ranges=ranges)
            a.savefig('%s' % ('sst' + str(i) + '   ' + str(sy) + '--' + str(ey)))

        if cuwnd == 1:
            #读取数据
            ncin = Dataset('uwnd.mon.mean.nc', 'r')
            uwnd200 = ncin.variables['uwnd'][:, 9, :, :]
            lons = ncin.variables['lon'][:]
            lats = ncin.variables['lat'][:]
            ncin.close()
            #分割时间
            uwnd200 = calculate_corr.de_time(uwnd200, sy, ey, month, 1948)
            #计算回归系数
            data, deldata = calculate_corr.verdata(uwnd200, pc[i], a)
            # np.savetxt('data0.txt', data)
            #分割纬度
            if ranges == 'area':
                data, lons, lats = calculate_corr.de_ll(data, lons, lats, 20, 60, 60, 150)
                deldata, lons, lats = calculate_corr.de_ll(deldata, lons, lats, 20, 60, 60, 150)
            #绘图
            # np.savetxt('data.txt', data)
            # np.savetxt('dedata.txt', deldata)
            a = plotcor.plotcors(data, deldata, lons, lats, col=col, ll='sst', ranges=ranges)
            a.savefig('%s' % ('sst' + str(i) + '   ' + str(sy) + '--' + str(ey)))


            # sst = calculate_corr.de_time(sst, sy, ey, month, 1948)
            # data, deldata = calculate_corr.verdata(uwnd200, pc[i], a)
            # uwnd200, lons, lats = calculate_corr.de_ll(uwnd200, lons, lats, 20, 60, 60, 150)
            #
            # a = plotcor.plotcors(data, deldata, lons, lats, col=col, ranges=ranges)


    return

if __name__ == "__main__":
    month = [9, 10]
    sy = 1983
    ey = 2016

    pc1 = np.loadtxt('pc1  %s.txt'%(str(sy) + '--' + str(ey)))
    pc2 = np.loadtxt('pc2  %s.txt'%(str(sy) + '--' + str(ey)))
    pc = [pc1, pc2]

    a = choose(csst=1, cuwnd=0,col='color',ranges='area', a=0.01)