# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 18:31:52 2018
@Describe: select combine_aqi_data.csv by date
@author: BordenChen
"""
import numpy as np
import pandas as pd
import glob
import os


class cd():
    def __init__(self, newpath):
        if newpath[0] != '~':
            self.newpath_ = newpath
        else:
            self.newpath_ = os.getcwd()+newpath[1:]
        self.currentpath_ = os.getcwd()
    def __enter__ (self):
        os.chdir(self.newpath_)
    def __exit__ (self, etype, value, traceback):
        os.chdir(self.currentpath_)
class SelectData():
    def __init__ (self,filepath, date):
        self.filepath_ = filepath
        self.date_ = date
        self.ReadFile()
        self.SelectData()
    def ReadFile(self):
        with cd(self.filepath_):
            self.dataframe_ = pd.read_csv('pm10_traingdata.csv',index_col = 0)
    def SelectData(self):
        return(self.dataframe_.loc[[date for date in self.dataframe_.index.values if any('/%s/'%(str(month).zfill(2)) in date for month in range(self.date_[0],self.date_[1]))]])
selectdata = SelectData('Station_Combine',[5,10])
df = selectdata.SelectData()
if not os.path.exists('Station_Combine_Select'):
    os.mkdir('Station_Combine_Select')
with cd('Station_Combine_Select'): 
    df.to_csv('select_aqi.csv')