'''
Author: wanghai hai.wang@linksee-semi.com
Date: 2024-04-15 13:29:38
LastEditors: wanghai hai.wang@linksee-semi.com
LastEditTime: 2024-04-16 09:12:24
FilePath: \Cpk\calbak.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd

# 读取mcu_info文件
mcu_info = pd.read_csv('mcu_info.csv')
G_column = mcu_info['OPEN_SHORT_TEST_VPP_D']

# 计算标准差σ
print(type(G_column))
G_sigma = G_column.std()
print(G_sigma)

# 读取lim文件
lim = pd.read_csv('lim.csv')
limG1 = float(lim['OPEN_SHORT_TEST_VPP_D'][1])
limG2 = float(lim['OPEN_SHORT_TEST_VPP_D'][2])

# 计算cpk
print(type(limG1))
print(type(G_column[0]))
up = (limG1- G_column[0])/(G_sigma*3)
down = (G_column[0]-limG2)/(G_sigma*3)
print(min(up,down))

# 打印列数据
# print(sigma)