import numpy as np
import pandas as pd
import beofplot
from eofs.standard import Eof
from pandas import DataFrame

def eoff(sy, ey, data, geosta, neof, lenstation):
    # 剔除无效站点
    nanindex = (data[np.isnan(data['per'])].index).unique()
    for i in nanindex:
        data = data.drop(i)
        geosta = geosta.drop(i)


    n = ey + 1 - sy
    per = np.empty([n, lenstation-len(nanindex)])

    #提取雨量值
    for i, year in enumerate(range(sy, ey+1)):
        per[i, :] = data[data['year'] == year]['per']
    solver = Eof(per)

    eof = solver.eofsAsCorrelation(neofs=neof)
    pc = solver.pcs(npcs=neof, pcscaling=1)
    print(solver.varianceFraction(neigs=neof))
    lisss = ['a', 'c', 'b', 'd']
    for i in range(neof):
        peof = beofplot.ploteofs(eof[i], np.array(geosta['lon']), np.array(geosta['lat']), sy, ey,i, lisss[i])
        peof.savefig('%s' % ('EOF' + str(i + 1) + '   ' + str(sy) + '--' + str(ey)))
        ppc = beofplot.plotpc(pc[:, i], sy, ey, i, lisss[i+2])
        ppc.savefig('%s'%('PC' + str(i+1) +'   '+ str(sy)+'--'+str(ey)))
    return


# data = pd.read_csv('year_sum.csv', index_col=[0])
# geosta = pd.read_csv('geostas.csv',index_col=[0])
# a = eoff(1985, 2016, data,geosta, 1, 198)

data = pd.read_csv('year_sumshp.csv', index_col=[0])
geosta = pd.read_csv('geostashp.csv', index_col=[0])
a = eoff(1983, 2016, data,geosta, 2, 80)

