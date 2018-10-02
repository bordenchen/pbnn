# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 14:59:02 2018

@author: fy
"""
import pandas as pd
import numpy as np
import os
import glob

class cd():
    def __init__(self, newpath):
        self.newpath_ = newpath
        self.currentpath_ = os.getcwd()
    def __enter__(self):
        os.chdir(self.newpath_)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.currentpath_)
def ReadCsv(filepath, filename):
    with cd(filepath):
        aqi_combine_df = pd.read_csv(filename,index_col = 0)
    return(aqi_combine_df)
def RandomSelect(index, random_num):
    random_row_list = list(np.random.choice(index, random_num,replace = False))
    return(random_row_list)
def SelectDataFrame(dataframe, select_list,output_name):
    select_df = dataframe.loc[select_list]
    if not os.path.exists('Random_Select'):
        os.mkdir('Random_Select')
    with cd('Random_Select'):
        select_df.to_csv(output_name)
aqi_df = ReadCsv('Station_Combine_Select','select_aqi.csv')
select_list_4000 = RandomSelect(aqi_df.index,4000)
without_4000_index = [row for row in aqi_df.index if row not in select_list_4000]
select_list_1000 = RandomSelect(without_4000_index,1000)
SelectDataFrame(aqi_df,select_list_4000,'training_4000.csv')
SelectDataFrame(aqi_df,select_list_1000,'testing_1000.csv')