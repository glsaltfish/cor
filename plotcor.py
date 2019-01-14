import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np
from scipy.interpolate import Rbf



def plotcors(data, deldata, oslon, oslat, col='bw', ll='0', ranges='all'):
    fig = plt.figure(dpi=400)

    colormap = [ '#5884ff',  '#638cfe', '#7c9eff', '#93b0fe', '#a0b8ff', '#abc0ff', '#b6caff', '#c2d3ff', '#ffffff', '#f3ddcf', '#f3d3c4', '#f3c8b8', '#f3b5a0', '#f4a088', '#f3896f', '#f27557', '#f46140','#f46140']
    colormap5 = [ 'gray', '#ffffff', 'lightgray',  'lightgray']

    # 绘制contour
    levels = [-1, -.9, -.8, -.7, -.6, -.5, -.4, -.3, -.2, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

    levels5 = [-1, -0.0000001, 0.0000001, 1]

    if col == 'color':
        delfill = ax.contourf(oslon, oslat, deldata, 20, transform=ccrs.PlateCarree(), cmap=plt.cm.coolwarm)
        plt.colorbar(delfill, orientation='horizontal')
        ax.coastlines()

    if col == 'bw':
        delfill = ax.contourf(oslon, oslat, deldata, levels5, transform=ccrs.PlateCarree(), colors=colormap5, alpha=0.8)
        fill = ax.contour(oslon, oslat, data, 5, transform=ccrs.PlateCarree(), colors='k')
        clevels = []
        filllevels = fill.levels
        for i in range(0, len(filllevels), 2):
            clevels.append(filllevels[i])
        ax.clabel(fill, clevels)
        ax.coastlines(alpha=0.5)



    # 设置坐标轴经纬度标志
    if ranges == 'area':
        if ll == 'sst':
            plt.subplots_adjust(top=0.98, bottom=0.08, left=0.01, right=0.99)
            ax.set_xticks(range(int(np.min(oslon)), int(np.max(oslon))+20, 20), crs=ccrs.PlateCarree())
            ax.set_yticks(range(int(np.min(oslat)), int(np.max(oslat))+10, 10), crs=ccrs.PlateCarree())
        else:
            plt.subplots_adjust(top=1, bottom=0.02, left=0.08, right=0.99)
            ax.set_xticks(range(int(np.min(oslon)), int(np.max(oslon)), 20), crs=ccrs.PlateCarree())
            ax.set_yticks(range(int(np.min(oslat)), int(np.max(oslat)) + 10, 10), crs=ccrs.PlateCarree())
    else:
        ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
        ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # 其他信息添加
    # 添加网格线
    # ax.gridlines(color='black', linestyle='--', alpha=0.4)
    # 白化
    # clip = maskout.shp2clip(fill,ax,ax,'bianjie_polyline.shp',range(11))
    return plt


