'''
Author: wanghai hai.wang@linksee-semi.com
Date: 2024-05-09 11:01:26
LastEditors: wanghai hai.wang@linksee-semi.com
LastEditTime: 2024-05-09 17:25:04
FilePath: \QA_FT_DATA\normal_distribution.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

# -------------------验证calc_cpk.py算法----------------------
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
  
# 生成一个200个数据点的标准正态分布随机样本。均值，标准差，数据量
data = np.random.normal(0, 1, 200)
print(data)

# 导出正态分布随机数
df = pd.DataFrame(data)
df.to_csv('files.csv', index = False)
  
# 拟合正态分布曲线，拟合均值mu，拟合标准差std
mu, std = norm.fit(data)
  
# 绘制直方图。数据，区间个数，图标样式颜色
plt.hist(data, bins=25, density=True, alpha=0.6, color='b')

# 绘制PDF
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)

# 设置标题为拟合后的均值和标准差  
plt.plot(x, p, 'k', linewidth=2)
title = "Fit Values: {:.2f} and {:.2f}".format(mu, std)
plt.title(title)
  
plt.show()


# 计算标准正态分布的数据的cpk
cpk_list = []
df_out = pd.DataFrame()
for chip_flag in range(0, 200):

    μ = df.iloc[chip_flag][0]

    USL = 0 + 3*1
    LSL = 0 - 3*1
    
    up = (USL - μ) / 3
    down = (μ - LSL) / 3
    
    # print(df)
    if up < down:
        cpk_list.append(up)
        print('第 ',chip_flag ,' pcs遍历结束,cpk为 up = ',up)
    else:
        cpk_list.append(down)
        print('第 ',chip_flag ,' pcs遍历结束,cpk为 down = ', down)
    
    # df_out[chip_flag] = cpk_list
    
# df_out.index = df.index + 1
# df_out.to_csv('test_cpk_data.csv')

print('.')