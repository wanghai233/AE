'''
Author: wanghai hai.wang@linksee-semi.com
Date: 2024-04-15 13:29:38
LastEditors: wanghai hai.wang@linksee-semi.com
LastEditTime: 2024-05-09 17:44:13
FilePath: \Cpk\cal_test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
# import pdb
import os

# 更新：测试项读取FT的，limit读取QA的（limit的值根据芯片不同，而非产品批次）
# 在5.65V下测试Power down ICC电流（最低功耗）。trim基准电压到1.230V ±1.6mv。trim oscillate高频、低频。
# sigma_list = ['ICC_test_5P65_VDD', 'vbgtrim_test_vbg_voltage', 'osctrim_test_rcosc_freq', 'osctrim_test_lcosc_freq']
sigma_list = ['ICC_test_5P65_VDD', 'vbg_osc_QA_test_vbg_QA', 'vbg_osc_QA_test_rcosc_QA', 'vbg_osc_QA_test_lcosc_QA']

HL_Limit = [10, -2, 1242.5, 1213.8, 2.594, 2.303, 2046, 1757]
Normal_Limit = [10, -2, 1233.19995, 1226.80005, 2.575, 2.425, 2046, 1948]


# 读取folder_path路径文件夹中所有的CSV文件并拼接它们
def merge_csv_files(folder_path, output_file):
    
    # 初始化一个空的 DataFrame 用于存储拼接后的结果
    concatenated_df = pd.DataFrame()
    
    # 遍历文件夹中的所有文件
    for file in os.listdir(folder_path):
        # 检查文件是否是 CSV 文件
        if file.endswith('.csv'):
            # 构建 CSV 文件的完整路径
            file_path = os.path.join(folder_path, file)
            # 读取 CSV 文件并将其拼接到结果 DataFrame 中
            df = pd.read_csv(file_path)
            concatenated_df = pd.concat([concatenated_df, df])
    
    # 将拼接后的结果保存为一个单独的 CSV 文件
    concatenated_df.to_csv(output_file, index=False)
    
    print("所有CSV文件已经成功合并为:", output_file)
    
    
# 计算高温和低温的cpk（高低温的测试程序是一样的FT，实际上用的QA） 
def HL_calc_cpk():
    
    chip_number = df_test.shape[0] - 1
    limit_flag = 0
    
    # 1.计算cpk，按行计算
    for chip_flag in range(0, chip_number):

        for column_flag in sigma_list:
            
            # 1.1.取出μ
            μ = df.loc[chip_flag, column_flag]
            # 1.2.取出USL、LSL
            USL = HL_Limit[limit_flag]
            LSL = HL_Limit[limit_flag + 1]
            
            up = (USL - μ) / (3*sigma_values[column_flag])
            down = (μ - LSL) / (3*sigma_values[column_flag])
            
            # 1.3.计算cpk
            cpk_list = []
            if up < down:
                cpk_list.append(up)
                print('第 ',chip_flag ,' pcs遍历结束,cpk为 up = ',up)
            else:
                cpk_list.append(down)
                print('第 ',chip_flag ,' pcs遍历结束,cpk为 down = ', down)
            
            limit_flag = limit_flag + 2
            if limit_flag > 7:
                limit_flag = 0
            
            '''
            column_flag = column_flag + 1
            if column_flag > 3:
                column_flag = 0
            '''
            
            # 1.4.将最终数据放入df_cpk中
            df_cpk[column_flag] = cpk_list
            
        df_cpk.index = df_cpk.index + 1
        df_cpk.to_csv('HL_cpk_data.csv', mode = 'a', header = False)
        
        
# 计算常温的cpk 
def Normal_calc_cpk():
    
    chip_number = df_test.shape[0] - 1
    limit_flag = 0
    
    # 1.计算cpk，按行计算
    for chip_flag in range(0, chip_number):

        for column_flag in sigma_list:
            
            # 1.1.取出μ
            μ = df.loc[chip_flag, column_flag]
            # 1.2.取出USL、LSL
            USL = Normal_Limit[limit_flag]
            LSL = Normal_Limit[limit_flag + 1]
            
            up = (USL - μ) / (3*sigma_values[column_flag])
            down = (μ - LSL) / (3*sigma_values[column_flag])
            
            # 1.3.计算cpk
            cpk_list = []
            if up < down:
                cpk_list.append(up)
                print('第 ',chip_flag ,' pcs遍历结束,cpk为 up = ',up)
            else:
                cpk_list.append(down)
                print('第 ',chip_flag ,' pcs遍历结束,cpk为 down = ', down)
            
            limit_flag = limit_flag + 2
            if limit_flag > 7:
                limit_flag = 0
            
            # 1.4.将最终数据放入df_cpk中
            df_cpk[column_flag] = cpk_list
            
        df_cpk.index = df_cpk.index + 1
        df_cpk.to_csv('Normal_calc_cpk.csv', mode = 'a', header = False)
        
        
if __name__ == "__main__":
    
    #读取所有的测试csv表格，并生成一张csv表格
    #注意：三温需要各自生成！
    folder_path = 'C:/Users/hai/Desktop/QA_FT_DATA'
    output_file = 'test.csv'
    merge_csv_files(folder_path, output_file)
    
    
    #初步简单处理csv文件。目前有个bug，number第一行无法被处理掉，只能强制跳过skiprows = 4
    df_test = pd.read_csv('test.csv', skiprows = 4)
    df_test = df_test[~df_test.iloc[:, 0].str.startswith('Tnumber:')]
    df_test = df_test[~df_test.iloc[:, 0].str.startswith('UpLimit:')]
    df_test = df_test[~df_test.iloc[:, 0].str.startswith('DownLimit:')]
    df_test = df_test[~df_test.iloc[:, 0].str.startswith('Unit:')]
    df_test = df_test[~df_test.iloc[:, 0].str.startswith('Serial#')]

    df_test = df_test[sigma_list] 
    df_test.to_csv('selected_test.csv', index=False)
    
    print("含有特定文本的行已成功删除，并保存为'selected_test.csv'")


    # 读取处理后的整个csv表格，na_values为过滤字段，筛选掉不需要的数据
    df = pd.read_csv('selected_test.csv', header=0, na_values=['PASS', 'FAULT', 'None'])
    df_cpk = pd.DataFrame(columns = ['ICC_test_5P65_VDD', 'vbg_osc_QA_test_vbg_QA', 'vbg_osc_QA_test_rcosc_QA', 'vbg_osc_QA_test_lcosc_QA'])
    # df_cpk.to_csv('cpk_data.csv')
    
    # 处理文件中所有的sigma值，并保存到sigma_values.csv
    # 指定列计算，忽略缺失值，排除非纯数值的行列，自由度修正为样本标准差
    sigma_columns = df[sigma_list]
    sigma_values = sigma_columns.std(axis = 0, skipna = True, numeric_only = True, ddof = 1)
    sigma_values.to_csv('sigma_values.csv', index = False)
    
    # 高低温cpk计算
    HL_calc_cpk()
    
    # 常温cpk计算
    # Normal_calc_cpk()
    
    
    