# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 11:51:08 2018

@author: fy
"""
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class TrainingData():
    def __init__(self, stations, items, file):
        self.__stations = stations # __xxx : private like variable
        self.__items = items
        self.__file = file
    def GetInput(self):
        aqi_df = self.ReadCSV(self.__file)
        self.select_col = self.SelectVariable(aqi_df, self.__stations, self.__items)
        self.input_value = self.SelectInput(aqi_df, self.select_col)
        self.target_value = self.SelectTarget(aqi_df)

    def ReadCSV(self,filename):
        aqi_df = pd.read_csv(filename, index_col = 0)
        return aqi_df
    
    def SelectVariable(self,dataframe,station,item):
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
    
    def SelectInput(self,dataframe,select_col):
        select_df = dataframe[select_col]
        return(select_df.values)
    def SelectTarget(self,dataframe):
        target_col = [col for col in list(dataframe) if 'target' in col]
        target_df = dataframe[target_col]
        return(target_df.values)

def MultiRegression(input_data):
    output_list=[]
    for data in input_data:
        output_list.append(0.142 -0.198*data[0]+0.083*data[1]+0.115*data[2]-0.068*data[3] +
                           0.047*data[4]-0.033*data[5]-0.006*data[6]+0.010*data[7]+0.004*data[8]+
                           0.340*data[9]+0.354*data[10]+0.157*data[11])
    return output_list
stations = ['chaozhou','meinong','dialiao']
items = ['AMB_TEMP','RAINFALL','RH','WIND_SPEED','WIND_DIREC','PM10']

filepath = 'Random_Select/regression_test1000.csv'
trainingdata = TrainingData(stations, items, filepath)
trainingdata.GetInput()
input_select_item=trainingdata.select_col
inputs=trainingdata.input_value
target=trainingdata.target_value
predict_list = np.array(MultiRegression(inputs)).reshape(1000,1)
target_list = np.array(target)
"""
day = np.array(list(range(0,len(predict_list))))
plt.figure(figsize=(200,20))
plt.plot(day[:], predict_list[:],'r',day[:],target_list[:],'b')
plt.show()
"""

print(np.sum(np.power(predict_list-target_list,2)))
