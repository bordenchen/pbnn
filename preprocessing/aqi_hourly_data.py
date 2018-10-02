# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 18:19:05 2018

@author: Borden Chen
"""
import numpy as np
import os
import glob
import pandas as pd

def leapyear(year):
    if year%400 == 0:
        return True
    elif year%100 == 0:
        return True
    elif year%4 == 0:
        return True
    else: 
        return False
    
def GetXlsFile(ch_dir,station_name):
    os.chdir(ch_dir)
    xlsfile_list = [file for file in glob.glob('*.xls') if station_name in file]
    return(xlsfile_list)
def ReadCsv(file_list,station_eng):
    for file in file_list:
        aqi_df = pd.read_excel(file)
        aqi_item = (aqi_df['測項']).unique()
        yearly_aqi_df = pd.DataFrame(columns = aqi_item)
        df_year = int(file.split('年')[0])+1911
        is_leap = leapyear(df_year)
        aqi_date=[]
        for month in range(1,13):
            if month in [1,3,5,7,8,10,12]:
                for day in range(1,32):
                    aqi_date.append('%i/%s/%s'%(df_year,str(month).zfill(2),str(day).zfill(2)))
            elif month in [4,6,9,11]: 
                for day in range(1,31):
                    aqi_date.append('%i/%s/%s'%(df_year,str(month).zfill(2),str(day).zfill(2)))
            else:
                if is_leap:
                    for day in range(1,30):
                        aqi_date.append('%i/%s/%s'%(df_year,str(month).zfill(2),str(day).zfill(2)))
                else:
                    for day in range(1,29):
                        aqi_date.append('%i/%s/%s'%(df_year,str(month).zfill(2),str(day).zfill(2)))
        for date in aqi_date:
            daily_aqi_df = aqi_df.loc[aqi_df['日期']==date,:]
            if daily_aqi_df.empty:
                daily_aqi_df_T=pd.DataFrame(columns = aqi_item,index=[str(hour).zfill(2) for hour in range(0,24)])
            else:
                daily_aqi_df_T = daily_aqi_df.iloc[:,2:].T
            newindex={}
            for hour in range(0,24):
                if hour<10:
                    newindex[str(hour).zfill(2)] = '%s %s:00' %(date,str(hour).zfill(2))
                else:
                    newindex[hour] = '%s %s:00' %(date,str(hour).zfill(2))
            daily_aqi_df_T = daily_aqi_df_T.rename(columns = daily_aqi_df_T.iloc[0],index = newindex)
            daily_aqi_df_T = daily_aqi_df_T.drop(daily_aqi_df_T.index[0])
            yearly_aqi_df = pd.concat((yearly_aqi_df,daily_aqi_df_T),axis = 0)
        for item in yearly_aqi_df.values:
            for value in item:
                if any(char in str(value) for char in ['*','%','x','#']):
                    yearly_aqi_df = yearly_aqi_df.replace(value,np.nan)  
        yearly_aqi_df = yearly_aqi_df.replace('NR',0)
        newcolumns = {}
        new_aqi_item=list(yearly_aqi_df)
        for column in new_aqi_item:
            newcolumns[column] = '%s:%s' %(station_eng, column)
        yearly_aqi_df = yearly_aqi_df.rename(columns=newcolumns)
        return(yearly_aqi_df)
        
def Save_Csv(dataframe,filename,filepath):
        print(os.getcwd())    
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        os.chdir(filepath)
        dataframe.to_csv(filename)

def AQI_Hourly(station_chi,station_eng):
        xlsfile_list = GetXlsFile('AQI_Data', station_chi)
        hourly_aqi_df = ReadCsv(xlsfile_list, station_eng)
        Save_Csv(hourly_aqi_df,'%s_2016.csv' %(station_eng),'Hourly_AQI_Data')

AQI_Hourly("橋頭","ciaotou")



"""
data=pd.DataFrame(data=[[1,np.nan,3.6],[2.4,6,3],[1.5,3,7]],columns=['a','b','c'])

range_list=['1-2','2-3','3-4']
for area in range_list:
    area_boundary=area.split('-')
    area_boundary=list(map(int,area_boundary))
    if area_boundary[0]<area_boundary[1]:
        data['WindDirec:%s'%(area)]=(data['a'].map(lambda x: 1 if (int(x)>=area_boundary[0]) and (int(x)<area_boundary[1]) else 0))
    else:
        data['WindDirec:%s'%(area)]=(data['a'].map(lambda x: 1 if (int(x)>=area_boundary[0]) or (int(x)<area_boundary[1]) else 0))

print(list(data))

"""