import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress
import matplotlib
import  matplotlib.font_manager as fm

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'

def fit_line(x, y):
    (beta_coeff, intercept, rvalue, pvalue, stderr) = linregress(x, y)
    return beta_coeff, intercept, rvalue, pvalue, stderr


def plot(time, line1, month, beta_coeff, intercept, r, p):
    line2 = time * beta_coeff +intercept
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylim(min(min(line1), min(line2)), max(line1)+((max(line1)-min(line1))/4))

    plt.plot(time, line1, label='观测', color='k', marker='o')
    plt.plot(time, line2, label='趋势', color='red')

    plt.text(min(time)-1, max(line1)+(4/5)*((max(line1)-min(line1))/4), '%s的趋势方程为:' % month)
    plt.text(min(time) - 1, max(line1)+(3/5)*((max(line1)-min(line1))/4),  'y = %fx+%f' % (beta_coeff, intercept))
    plt.text(min(time)-1, max(line1)+(2/5)*((max(line1)-min(line1))/4), 'R-value 为 %f ,P-value 为 %f' % (r, p))

    plt.legend(loc=1)
    ax.set_ylabel('降水/mm')
    ax.set_xlabel('年')
    plt.savefig('%s.png' % (month))
    return



# month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
month = range(1,13)
data = pd.read_csv(r'D:\a_postgraduate\changjiang\data\data.csv', index_col=0)
x = range(1983, 2018)

sum = data['pre'].groupby([data['month'], data['year']]).sum()/80
for i in range(1,13):
    beta_coeff, intercept, rvalue, pvalue, stderr = fit_line(x, np.array(sum[i]))

    a = plot(x ,np.array(sum[i]), '%s月'%month[i-1], beta_coeff, intercept, rvalue, pvalue)

ysum = data['pre'].groupby(data['year']).sum()/80/35
beta_coeff, intercept, rvalue, pvalue, stderr = fit_line(x, np.array(ysum))
a = plot(x ,np.array(ysum), '年平均雨量', beta_coeff, intercept, rvalue, pvalue)


#三个汛期计算##############################################################
data['month'][(data['month'] == 4) | (data['month'] == 5)] = 44
data['month'][(data['month'] == 6) | (data['month'] == 7) | (data['month'] == 8)] = 88
data['month'][(data['month'] == 9) | (data['month'] == 10) | (data['month'] == 11)] = 99
sum = data['pre'].groupby([data['month'], data['year']]).sum()/80
month = ['汛前', '汛期', '秋汛']
for i,m in enumerate([44, 88, 99]):
    beta_coeff, intercept, rvalue, pvalue, stderr = fit_line(x, np.array(sum[m]))
    a = plot(x ,np.array(sum[m]), month[i], beta_coeff, intercept, rvalue, pvalue)

#枯期计算##############################################################
data = pd.read_csv(r'D:\a_postgraduate\changjiang\data\data.csv', index_col=0)
data['year'][(data['month'] == 1) | (data['month'] == 2) | (data['month'] == 3)] = np.array(data['year'][(data['month'] == 1) | (data['month'] == 2) | (data['month'] == 3)].apply(lambda x: x-1))

# data['month'][ (data['month'] == 1) | (data['month'] == 2) | (data['month'] == 3)| (data['month'] == 11) | (data['month'] == 12)] = 99

sum = data['pre'].groupby(data['year']).sum()/80/35
sum = sum.drop([1982,2017])
x = range(1983,2017)
beta_coeff, intercept, rvalue, pvalue, stderr = fit_line(x, np.array(sum))
a = plot(x ,np.array(sum), '枯期', beta_coeff, intercept, rvalue, pvalue)