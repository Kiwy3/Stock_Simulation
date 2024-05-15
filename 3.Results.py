# -*- coding: utf-8 -*-
"""
Calcul des indicateurs clés pour l'ensemble des instances utilisées
Dans le cadre du cours de CL04
author : Nathan Davouse
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Global variables
path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\"
load_path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\2.Instances_costs"
K_list = [0,10,20,30,40,50,60]
nb = 1000

#Load instances parameters
with open(path+'param.json') as json_file:
    param = json.load(json_file)

#Calculation func
def indicat(f,K):
    T = pd.read_csv(load_path + "\\"+f,index_col=0)
    temp = np.full(9,0.)
    #Obtain K
    temp[0] = K
    #Niveau moyen de stock
    temp[1] = sum(T["stock"]*T["Time_gap"])/T.time.max()
    #Perte en magasin
    temp[2] = T.where(T.event_type == 1).time.count() #total_mag
    temp[3] = T.where(T.event_type == 1).perte_magasin.sum() #perte_mag
    temp[4] = temp[3]/temp[2]
    #Attente en ligne
    temp[5] = T.where(T.event_type == 2).time.count()
    # A changer quand je run la prochaine simulation
    temp[6] = T.late_nb.sum()
    temp[7] = temp[6]/temp[5]
    #Cout total moyen 
    temp[8] = T.iloc[-1].mean_cost
    #Return
    return temp

#init results df
Results = pd.DataFrame(columns = ["K","stock_avg","total_mag","perte_mag","ratio_mag","total_ligne","perte_ligne","ratio_ligne","avg_total_cost"])

for i,K in enumerate(K_list) :
    file_name = "Finished_T"+str(nb)+"_K"+str(K)+".csv"
    Results.loc[i] = indicat(file_name,K)
Results.sort_values("K",inplace=True)

Results.to_csv(path+"results.csv")
