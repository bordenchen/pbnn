# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:15:28 2018

@author: USER
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

def initialize_network(n_inputs, n_hidden,n_outputs, layer_n_hidden):
    network=list()
    network.append(np.random.rand(n_inputs,n_hidden))
    for i in range(1,layer_n_hidden):
        network.append(np.random.rand(n_hidden,n_hidden))
    network.append(np.random.rand(n_hidden, n_outputs))
    return network

def activate(weight, inputs, bias):
    activation = bias + np.dot(inputs,weight)
    return transfer(activation)
    
def transfer(activation):
    return 1.0/(1.0 + np.exp(-activation))

def forward_propagate(weight_network, inputs, bias):
    output_network=[]
    output_network.append(inputs)
    for weight in weight_network:
        inputs=activate(weight, inputs, bias)
        output_network.append(inputs)
    return output_network
    
def back_propagate(target, weights_network, outputs_network):
    weights_change=[]
    delta_network=[]
    for i in reversed(range(len(weights_network))):
        if len(delta_network)==0:
            output_layer=outputs_network[i+1]
            input_layer=outputs_network[i]    
            #print(input_layer)
            new_delta_layer=-(target-output_layer)*(output_layer*(1-output_layer))
            delta_network.insert(0,new_delta_layer)
            weights_change.insert(0,np.dot(input_layer[:,None],new_delta_layer[None,:]))     
        else:
            output_layer=outputs_network[i+1]
            output_weight_layer=weights_network[i+1]
            input_layer=outputs_network[i]
            delta_layer=delta_network[0]
            new_delta_layer=delta(delta_layer, output_weight_layer, output_layer)
            delta_network.insert(0,new_delta_layer)
            weights_change.insert(0,np.dot(input_layer[:,None],new_delta_layer[None,:]))
    return(weights_change)

def delta(delta_value, weight, output):
    return np.dot(weight,delta_value)*(output*(1-output))

def adjust_weight(weight_network, weight_change, learning_rate):
    new_weight=[]
    for i in range(len(weight_network)):
        new_weight.append(weight_network[i]-learning_rate*weight_change[i])
    return new_weight



stations = ['chaozhou','meinong','dialiao']
items = ['AMB_TEMP','RAINFALL','RH','WIND_SPEED','WIND_DIREC','PM10']

filepath = 'Random_Select/testing_1000.csv'
trainingdata = TrainingData(stations, items, filepath)
trainingdata.GetInput()
input_select_item=trainingdata.select_col
inputs=trainingdata.input_value
target=trainingdata.target_value
    
def bpnn(input_data, target_data):
    input_node = len(input_data.T)
    output_node = len(target_data.T)
    bias=0
    learn_rate=0.7
    network=initialize_network(input_node,10,output_node,2)
    for _iter in range(100000):
        error=0
        for i in range(len(input_data)):
            inputs=input_data[i]
            target=target_data[i]
            outputs_networks=(forward_propagate(network, inputs, bias))
            error+=(np.sum(0.5*np.power(target-outputs_networks[-1],2)))            
            #print("target: %i  predict: %f" %(target, outputs_networks[-1]))
            weight_change=(back_propagate(target,network,outputs_networks))
            network=adjust_weight(network, weight_change, learn_rate)
        print("iter: %i    error: %f " %(_iter,error))
    return network

def PredictValue(network, input_data):
    network_ = network
    output_list = []
    bias_ = 0.5
    for i in range(len(input_data)):
        inputs = input_data[i]
        outputs_network = forward_propagate(network_,inputs, bias_)
        predict = outputs_network[-1]
        output_list.append(predict.tolist())
    return(output_list)
#network = bpnn(inputs,target)

predict_list = np.array(PredictValue(network, inputs))

target_list = np.array(target)
"""
day = np.array(list(range(0,len(predict_list))))
plt.figure(figsize=(50,20))
plt.plot(day[:200], predict_list[:200],'r',day[:200],target_list[:200],'b')
plt.show()
"""
print(np.sum(np.power(predict_list-target_list,2)))