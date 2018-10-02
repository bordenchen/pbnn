# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 09:17:46 2018

@author: Borden Chen
"""
import pandas as pd
import numpy as np

def ReadCSV(filename):
    aqi_df = pd.read_csv(filename, index_col = 0)
    return aqi_df

def SelectVariable(dataframe,station,item):
    df_col = list(dataframe)
    select_station_col = []
    for station in stations:
        for col in df_col:
            if station in col:
                select_station_col.append(col)
    select_col=[]
    for item in items:
        for col in select_station_col:
            if item in col:
                select_col.append(col)
    return(select_col)

def SelectInput(dataframe,select_col):
    select_df = dataframe[select_col]
    return(select_df.values)
def SelectTarget(dataframe):
    target_col = [col for col in list(dataframe) if 'target' in col]
    target_df = dataframe[target_col]
    return(target_df.values)


stations = ['chaozhou']
items = ['AMB_TEMP','CO']

aqi_df = ReadCSV('combine_aqi_data.csv')
select_col = SelectVariable(aqi_df,stations,items)
input_value = SelectInput(aqi_df,select_col)
target_value = SelectTarget(aqi_df)