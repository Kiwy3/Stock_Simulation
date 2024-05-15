# -*- coding: utf-8 -*-
"""
Ajout des colonnes concernant les couts liées aux instances de stock
Dans le cadre du cours de CL04
author : Nathan Davouse
"""

import numpy as np
import pandas as pd
import math
from os import listdir
from os.path import isfile, join

param = {
        #Commandes
        "lambda1" : 15 #Commande hors ligne
         ,"lambda2" : 30 #Commande en ligne
        #Approvisionnement
        ,"L" : 2 #Délai de livraison approvisionnement
        ,"W" : 1 # Délai acceptable pour une commande en ligne
        ,"Q" : 180 #Quantité de commande
        ,"r" : 60 #Point de recommande
        #Couts
        ,"F" : 18 #Cout de passation de commandE
        ,"h" : 0.05 #Cout de stockage
        ,"p" : 20 #Cout de perte unitaire
        ,"b" : 5 #Indemnité de retard
        #Paramètre de priorisation
        ,"K" : 10 #Priorité de classe
}




K_list = [0,10,20,30,40,50,60]
nb=10
load_path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\1.Instances"
export_path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\2.Instances_costs"

for K in K_list : 
    #put csv files in pd Dataframe
    T_name = "Timeline"+str(nb)+"_K"+str(K)+".csv"
    Timeline = pd.read_csv(load_path+"\\"+T_name,index_col=0)
    W_name = "Wait"+str(nb)+"_K"+str(K)+".csv"
    Wait = pd.read_csv(load_path+"\\"+W_name,index_col=0)
    #manage time
    Timeline.loc[0,"time"]= 0
    Timeline["Time_gap"] = Timeline["time"].diff(periods=-1)*-1
    Timeline["Time_gap"] = Timeline["Time_gap"].apply(lambda x : 0 if math.isnan(x) else x)
    #Cout de passation, on suppose à réception
    Timeline["passation_cost"] = Timeline["event_type"].apply(lambda x :param["F"] if x==3 else 0)
    #Cout de stockage
    Timeline["stock_cost"] = Timeline["stock"]*param["h"] * Timeline["Time_gap"]
    #Cout de perte de vente en magasin
    Timeline["Loss_cost"] = Timeline["perte_magasin"]*param["p"]
    #cout de retard
    late_table = Wait.groupby("release_id")["late"].sum()
    Timeline.loc[late_table.index,"late_cost"] = late_table
    #Couts totaux
    Timeline["Total_cost"] = Timeline["passation_cost"]+Timeline["stock_cost"]+Timeline["Loss_cost"].to_numpy(na_value=0)+Timeline["late_cost"].to_numpy(na_value=0)
    Timeline["Cum_cost"]= Timeline["Total_cost"].cumsum()
    Timeline["mean_cost"] = np.divide(Timeline["Cum_cost"],Timeline["time"])
    Timeline.loc[0,"mean_cost"] = Timeline.loc[0,"Total_cost"]
    #new file name
    F_name = "Finished_T"+str(nb)+"_K"+str(K)+".csv"
    Timeline.to_csv(export_path+"\\STP2_"+F_name)