# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:18:08 2018
normalize input values

@author: Borden Chen
"""

import pandas as pd
import numpy as np
import os
import glob


class cd:
    def __init__(self, newpath):
        self.newpath = newpath
        self.currentpath = os.getcwd()
    def __enter__(self):
        os.chdir(self.newpath)
    def __exit__(self,etype, value, traceback):
        os.chdir(self.currentpath)
def ReadCSV(filepath):
    with cd(filepath):
        file_list = [file for file in glob.glob('*.csv')]
        for file in file_list:
            if 'aqi_data' not in locals():
                aqi_data = pd.read_csv(file,index_col = 0)
            else:
                aqi_data = pd.concat((aqi_data,pd.read_csv(file,index_col = 0)),axis = 1)
        aqi_data = aqi_data.dropna()
    return(aqi_data)
def Normalize(dataframe,target_station,target_item):
    item_list = list(dataframe)
    for item in item_list:
        print('current normalize item--> ', item)
        station = item.split(':')[0]
        if item.split(':')[1] == 'WIND_DIREC': 
            range_list=['45-135','135-225','225-315','315-45']
            for area in range_list:
                area_boundary=area.split('-')
                area_boundary=list(map(int,area_boundary))
                if area_boundary[0]<area_boundary[1]:
                    dataframe[station + ':WIND_DIREC_%s'%(area)]=(dataframe[station + ':WIND_DIREC'].map(lambda x: 1 if (int(x)>=area_boundary[0]) and (int(x)<area_boundary[1]) else 0))
                else:
                    dataframe[station + ':WIND_DIREC_%s'%(area)]=(dataframe[station + ':WIND_DIREC'].map(lambda x: 1 if (int(x)>=area_boundary[0]) or (int(x)<area_boundary[1]) else 0))
            dataframe = dataframe.drop(columns=[('%s:WIND_DIREC'%(station))])
        else:
            item_df = dataframe[item]
            normalize = lambda x: (x-item_df.min())/(item_df.max()-item_df.min())
            dataframe[item] = dataframe[item].map(normalize)
    dataframe['target_%s'%(target_item)]=np.insert(np.delete(np.array(list(map(float,dataframe['%s:%s'%(target_station,target_item)].values))),-1,0),0,np.nan)
    dataframe = dataframe.dropna()
    return(dataframe)
def Get_Normalize_Data():
    aqi_df = ReadCSV('Hourly_AQI_Data')
    aqi_data = Normalize(aqi_df,'pingtung','PM10')
    if os.path.exists('Station_Combine'):  
        os.chdir('Station_Combine')
        aqi_data.to_csv('pm10_traingdata.csv')
    else:
        os.mkdir('Station_Combine')
        os.chdir('Station_Combine')
        aqi_data.to_csv('pm10_traingdata.csv')
Get_Normalize_Data()
"""
data = pd.DataFrame(data=[[1.5,3.1],[4.6,65.44]])
#data['target'] = np.insert(map(float,np.delete(data[1].values,-1,0)),0,np.nan)
ddd=np.array(list(map(int,data[1].values)))
print(ddd)
"""

