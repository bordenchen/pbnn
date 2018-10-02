# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 02:02:27 2018

@author: fy
"""

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
                    print(station)
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
        
stations = ['chaozhou','meinong','dialiao']
items = ['AMB_TEMP','RAINFALL','RH','WIND_SPEED','WIND_DIREC','PM10']

filepath = 'Random_Select/training_4000.csv'
trainingdata = TrainingData(stations, items, filepath)
trainingdata.GetInput()
input_select_item=trainingdata.select_col
print(input_select_item)
print(trainingdata.input_value)
print(trainingdata.target_value)