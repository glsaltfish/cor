import cartopy.crs as ccrs
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
from matplotlib.path import Path
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.patches import PathPatch
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint


def ploteofs(data, lon, lat, sy, ey, i, labela):
    fig = plt.figure(dpi=400)

    # 插值初定义
    olon = np.linspace(89,113,88)
    olat = np.linspace(24,36,88)

    olon,olat = np.meshgrid(olon, olat)
    # 插值处理
    func = Rbf(lon, lat, data, function='linear')
    data_new = func(olon, olat)

    #绘制contour
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=102))
    # plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.94)
    #建立坐标系，并将裁剪的path得出
    plate_carre_data_transform = ccrs.PlateCarree()._as_mpl_transform(ax)
    shps = np.loadtxt('1.txt', usecols=[1, 2])
    plat = shps[:, 1]
    plon = shps[:, 0]
    upath = Path(list(zip(plon, plat)))
    upath = PathPatch(upath, transform=plate_carre_data_transform)

    line= ax.plot(plon, plat ,transform=plate_carre_data_transform, color='k', alpha=0.8)

    fill = ax.contour(olon, olat, data_new, 10, transform=ccrs.PlateCarree(), colors='k', alpha=1)


    for collection in fill.collections:
        collection.set_clip_path(upath)

    CS_label = ax.clabel(fill, fontsize=12, fmt='%6.1f')

    # 删除clabel
    aaa=ccrs.PlateCarree(central_longitude=102).transform_points(ccrs.Geodetic(), plon, plat)
    clip_map_shapely = ShapelyPolygon(aaa)
    for text_object in CS_label:
        if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
            text_object.set_visible(False)

    fill = ax.contourf(olon, olat, data_new, 10, transform=ccrs.PlateCarree(), cmap=plt.cm.gray, alpha=0.4)

    # fill = ax.contourf(olon, olat, data_new, 15, transform=ccrs.PlateCarree(), cmap=plt.cm.RdBu_r)
    # plt.colorbar(fill, orientation='horizontal')

    for collection in fill.collections:
        collection.set_clip_path(upath)

    # #添加shp文件进入图片中

    # fname = r'bianjie.shp'
    # shape_feature = ShapelyFeature(Reader(fname).geometries(), ccrs.PlateCarree(), edgecolor='k', facecolor='none', linewidths=0.55)
    # ax.add_feature(shape_feature)

    #设置坐标轴经纬度标志
    ax.set_xticks(range(89,114,6), crs=ccrs.PlateCarree())
    ax.set_yticks(range(24,37,4), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    plt.text(89.5, 35, labela, transform=ccrs.PlateCarree(),fontsize=12)
    ax.tick_params(labelsize=12)


    return plt

def plotpc(pc, sy, ey, i, labela):
    ma = fast_moving_average(pc, 11)
    fig = plt.figure(dpi=400)
    ax = fig.add_subplot(111)
    years = range(sy, ey + 1)
    ax.bar(years, pc, color='black')
    plt.plot(years, ma, color='k', linewidth=4)
    plt.subplots_adjust(top=1, bottom=0.1, left=0.1, right=0.97)

    ax.axhline(0, color='k')
    ax.axhline(1, color='k', linestyle='--', alpha=0.5)
    ax.axhline(-1, color='k', linestyle='--', alpha=0.5)
    ax.set_xticks(range(sy, ey + 1, 10))
    ax.set_yticks([-2, -1, 0, 1, 2])
    plt.xlim(sy, ey)
    plt.ylim(-3, 3)

    plt.text(sy + 1, 2.5, labela, fontsize=18)
    ax.tick_params(labelsize=18)
    return plt


def fast_moving_average(x, N):
    return np.convolve(x, np.ones((N,)) / N)[(N - 1):]