'''
Author: wanghai hai.wang@linksee-semi.com
Date: 2024-04-15 13:29:38
LastEditors: wanghai hai.wang@linksee-semi.com
LastEditTime: 2024-04-19 16:43:26
FilePath: \Cpk\cal_test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
import pdb

sigma_list = ['OPEN_SHORT_TEST_VPP_D', 'OPEN_SHORT_TEST_GPIO0_D', 'OPEN_SHORT_TEST_GPIO1_D', 
              'OPEN_SHORT_TEST_GPIO2_D', 'OPEN_SHORT_TEST_GPIO3_D', 'OPEN_SHORT_TEST_GPO0_D', 
              'OPEN_SHORT_TEST_GPIO4_D', 'OPEN_SHORT_TEST_GPIO5_D', 'OPEN_SHORT_TEST_GPIO6_D', 
              'OPEN_SHORT_TEST_GPIO7_D', 'OPEN_SHORT_TEST_GPIO8_D', 'OPEN_SHORT_TEST_GPIO9_D', 
              'POWER_SHORT_VDD', 'CHECK_SITE_I_site', 'CHECK_SITE_code_check_sum', 
              'ICC_test_5P65_VDD', 'vbgtrim_test_vbg_voltage', 'vbgtrim_test_vbg_value', 
              'vbgtrim_test_vbg_diff', 'vbgtrim_test_vbg_value_final', 'acmptrim_test_acmp_trim_value', 
              'osctrim_test_rcosc_freq', 'osctrim_test_rcosc_diff', 'osctrim_test_rcosc_trimvalue', 
              'osctrim_test_rcosc_trimvalue_final', 'osctrim_test_lcosc_freq', 'osctrim_test_lcosc_diff', 
              'osctrim_test_lcosc_trimvalue', 'osctrim_test_lcosc_trimvalue_final']

if __name__ == "__main__":
    # 读取整个csv表格，na_values为过滤字段，筛选掉不需要的数据
    df = pd.read_csv('mcu_info.csv', header=0, na_values=['PASS', 'FAIL','None'])
    df_lim = pd.read_csv('lim.csv', header=0,na_values=['PASS', 'None'])
    
    # 处理文件中所有的sigma值，并保存到sigma_values_data.csv
    sigma_columns = df[sigma_list]
    sigma_values = sigma_columns.std()
    sigma_values.to_csv('sigma_values_data.csv', index = False)
    print(sigma_values)
    
    #测试芯片数量
    chip_number = 1537
    
    # 1.计算cpk，按列计算
    # 1.1.取出USL、LSL
    for sigma_list_value in sigma_list:
        USL = float(df_lim.loc[1, sigma_list_value])
        LSL = float(df_lim.loc[2, sigma_list_value])
        
        # 1.2.取出μ
        for chip_flag in range(0,chip_number):
            μ = df.loc[chip_flag, sigma_list_value]
            # print(USL, μ, LSL)
            
            up = (USL - μ) / (3*sigma_values[0])
            down = (μ - LSL) / (3*sigma_values[0])
            # print(sigma_values)
            
            # 1.3.计算cpk
            if up < down:
                # 最终值即up
                print('up = ',up)
            else:
                # 最终值即down
                print('down = ', down)

    # 2.替换掉μ?
    
    