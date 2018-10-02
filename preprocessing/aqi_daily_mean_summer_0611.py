# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 17:38:20 2018

@author: Borden Chen
"""

import pandas as pd
import numpy as np
import os
import glob
import time
import datetime
from random import randint
g_start_time=time.time() #start counting process time

#declare change directory class
class Cd:   
    def __init__(self, newpath):
        self.new_path_=newpath   #new working directory
        self.current_path_=os.getcwd() #current working directory
    def __enter__ (self):
        if self.new_path_[0] == '~':
            print('change directory')
            os.chdir(self.current_path_+self.new_path_[1:])
        else:
            os.chdir(self.new_path_)
    def __exit__ (self, etype, value, traceback):
        os.chdir(self.current_path_)
    
#declare get station AQI data daily mean class
class Station_Daily_Mean:
    def __init__ (self, folderpath, year, date_col, item_col, ran_number):
        self.search_year_=year #the duration of year to collect AQI data
        self.folder_path_=folderpath
        self.date_col_=date_col #the name of column that contain PublishTime
        self.item_col_=item_col #the name fo column that contain element of AQI
        self.ran_number_=ran_number
    def __enter__ (self):
        for year_ in range(self.search_year_[0], self.search_year_[1]): #iteration search for the specific year
            self.Read_File(year_)
        return(self)
    def Read_File(self, year): #using pandas dataframe read AQI data
        list_filepath_=[file_ for file_ in glob.glob('%i*' %(year)) \
                        if any(filetype_ in file_ for filetype_ in ['.csv','.xls'])]       
        if list_filepath_:
            for file_ in list_filepath_:
                self.station_name_=(file_.split('.'))[0]
                if 'csv' in file_:
                    df_aqi_data_=pd.read_csv(file_, 'r', encoding='big5')
                else:
                    df_aqi_data_=pd.read_excel(file_)
                df_aqi_data_['Daily_Mean']=df_aqi_data_.apply(self.Average, axis=1)  #apply row vector (hourly data)
                list_aqi_element_=df_aqi_data_[self.item_col_].unique()
                self.df_daily_aqi_=pd.DataFrame(columns=list_aqi_element_)
                for date_ in df_aqi_data_[self.date_col_].unique():
                    df_daily_aqi_select_=pd.DataFrame(df_aqi_data_.loc[df_aqi_data_[self.date_col_]==date_,[self.item_col_,'Daily_Mean']].T.values)
                    df_daily_aqi_select_.columns=df_daily_aqi_select_.iloc[0]
                    df_daily_aqi_select_=df_daily_aqi_select_.drop(0)  
                    df_daily_aqi_select_.index=[date_]
                    self.df_daily_aqi_=self.df_daily_aqi_.append(df_daily_aqi_select_)
                self.Save_Csv()
                self.Random_Select(self.ran_number_)
    def Average(self, data):
        element_name_=data[2]
        hourly_data_=data[3:]
        if any([True for item_ in hourly_data_ if any(char_ in str(item_) for char_ in ['#','*','x'])]):
              hourly_data_=hourly_data_.replace([item_ for item_ in data.values if any((char_ in str(item_) for char_ in ['#','*','x']))],np.nan).dropna()
        hourly_data_=hourly_data_.replace('NR',0)
        if element_name_=='RAINFALL':
              return(hourly_data_.sum())
        else: 
              return(hourly_data_.mean())
    
    def Random_Select(self, random_number):  #select an amount of randam days and save as .csv file end with "aqi_daily_avg_random"
        list_date_range_=[x for x in range(90, 304) if datetime.datetime.strptime('2016 %i' %x, '%Y %j').weekday()<5]
        list_random_index_=np.random.choice(list_date_range_, random_number,replace=False)
        df_random_select_=self.df_daily_aqi_.iloc[list_random_index_]
        self.Save_Csv(df_random_select_, 'aqi_daily_avg_random_summer' + str(random_number))      
        
    def Save_Csv(self,dataframe = None, file_name = None):  #using pandas saving AQI daily mean
        file_name = 'aqi_daily_avg' if file_name == None else file_name
        dataframe = self.df_daily_aqi_ if dataframe is None else dataframe
        os.chdir(self.folder_path_)
        if not os.path.exists('daily_avg'):
            os.makedirs('daily_avg')
        with Cd('~/daily_avg/'):
            dataframe.to_csv(self.station_name_ + '_' + file_name +'.csv', encoding='big5')
    def __exit__ (self, etype, value, tracback):
            pass
with Station_Daily_Mean('C:/Users/CID/Desktop/aqi_dataset_v0604', [105,107], '日期', '測項', 100) as station_daily_mean:   
    print("---%s seconds ---" %(time.time() - g_start_time))