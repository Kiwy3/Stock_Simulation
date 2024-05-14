# -*- coding: utf-8 -*-
"""
Projet de CL04 portant sur la simulation d'une gestion de stock pour estimer une politique de gestion
Fait au semestre de printemps 2024
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

#On suppose qu'aucun évenement ne peut arriver totalement en même temps
param = {
        #Commandes
        "lambda1" : 15 #Commande hors ligne
         ,"lambda2" : 30 #Commande en ligne
        #Approvisionnement
        ,"L" : 5 #Délai de livraison approvisionnement
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


def commande(lamb1,lamb2):
    lamb = lamb1 + lamb2
    t = np.random.exponential(1/lamb)
    c = np.random.uniform()
    p1 = lamb1/(lamb1+lamb2)
    if c>p1 : 
        cm = 2
    else : 
        cm = 1
    return t,cm
def simulation (param,impr = True,print_step = 100,nb_appro_tot = 1000):
    #Création de l'échéancier en utilisant la librairie pandas
    col= ["time","event_type","stock","attente","perte_magasin","deliv","late_cost"]
    Timeline = pd.DataFrame(columns=col)
    Timeline.loc[0]=np.full(len(col),0)
    Timeline["time"]=Timeline["time"].astype(float)
    Timeline["late_cost"]=Timeline["late_cost"].astype(float)
    Timeline["deliv"]=Timeline["deliv"].astype(bool)
    Timeline.loc[0,"time"]= -1
    Timeline.loc[0,"stock"]=param["r"]

    #Création de la table d'attente
    Wait_col = ["time","late","release_date"]
    Wait = pd.DataFrame(columns=Wait_col)
    w_id = 0
    last_w_id = 0

    #Init appro
    appro=False
    time_appro = 10*(param["lambda1"]+param["lambda2"])
    #Init commande
    time_cmd, type_cmd = commande(param["lambda1"],param["lambda2"])
    #Init iterations variable
    i=0 
    appro_count = 0

    while appro_count<nb_appro_tot:

        i+=1 #indice du tableau

        #Création nouvelle ligne et conservation des états si nécessaire
        #Timeline.loc[i]=np.full(len(col),0) to let it
        Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]

        #Une commande arrive
        if time_cmd<time_appro : 
            Timeline.loc[i,"time"] = time_cmd
            Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"] #continuité du stock

            #Commande magasin
            if type_cmd ==1: 
                Timeline.loc[i,"event_type"]=1
                if Timeline.loc[i-1,"stock"]>1: #Stock dispo, on livre
                    Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]-1
                    Timeline.loc[i,"deliv"] = True
                else : #Stock indispo, perte d'une cmd
                    Timeline.loc[i,"perte_magasin"] = 1

            #Commande en ligne
            else : 
                Timeline.loc[i,"event_type"]= 2
                if Timeline.loc[i-1,"stock"]>param["K"]: #Stock supérieur à K, on livre
                    Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]-1
                    Timeline.loc[i,"deliv"] = True
                else : #Stock inférieur à K, on met en attente
                    Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]+1
                    Wait.loc[w_id,"time"]=Timeline.loc[i,"time"] #On ajoute un nouveau temps au tableau d'attente
                    w_id+=1

            #Génération nouvelle commande
            delay_cmd, type_cmd = commande(param["lambda1"],param["lambda2"])
            time_cmd = delay_cmd+Timeline.loc[i,"time"]

        #Une livraison arrive
        else : 
            appro_count += 1
            Timeline.loc[i,"event_type"]= 3
            Timeline.loc[i,"time"] = time_appro
            Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]+ param["Q"]
            time_appro += 10*(param["lambda1"]+param["lambda2"])
            appro=False
            Timeline.loc[i,"deliv"] = True

            if Timeline.loc[i-1,"attente"] > 0:
                #Si la quantité en attente est comblé par l'approvisionnement
                if Timeline.loc[i-1,"attente"]< param["Q"] :
                    #Remise à 0 de l'attente sur l'échéancier            
                    Timeline.loc[i,"stock"] -= Timeline.loc[i-1,"attente"]
                    Timeline.loc[i,"attente"] = 0
                    #Gestion de l'échéancier de retard
                    Wait.loc[last_w_id:w_id,"late"]=Wait["time"].apply(lambda x: max(0.,Timeline.loc[i,"time"]-param["W"]-x))
                    Wait.loc[last_w_id:w_id,"release_date"] = Timeline.loc[i,"time"]
                    last_w_id = w_id

                #Si la quantité en attente n'est pas comblé par l'approvisionnement
                else : 
                    #Remise à 0 de l'attente sur l'échéancier            
                    Timeline.loc[i,"stock"] -= param["Q"]
                    Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]-param["Q"]
                    #Calcul du cout d'indémnité
                    Wait["late"][Wait["release_date"].isnull()][:param["Q"]]= Wait["time"].apply(lambda x: max(0.,Timeline.loc[i,"time"]-param["W"]-x))
                    Wait["release_date"][Wait["release_date"].isnull()][:param["Q"]] = Timeline.loc[i,"time"]
                    #Gestion de l'échéancier de retard
                    Wait.loc[last_w_id:last_w_id+param["Q"],"late"]=Wait["time"].apply(lambda x: max(0.,Timeline.loc[i,"time"]-param["W"]-x))
                    Wait.loc[last_w_id:last_w_id+param["Q"],"release_date"] = Timeline.loc[i,"time"]
                    last_w_id += param["Q"]
                    
        #Recommande
        if Timeline.loc[i,"stock"] < param["r"] and appro==False :
            time_appro = Timeline.loc[i,"time"]+param["L"]
            appro=True

            if appro_count%print_step==0 and impr:
                print("----------------------------------- appro "+str(appro_count)+"/"+str(nb_appro_tot)+"-----------------------------------")

    #return the table
    return Timeline,Wait

def csv_export(Dataf , name):
    path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\export_test_stp1"
    csv_name = str(name)+str(nb_appro)+"_K"+str(K)
    path_name = path+"/"+csv_name+".csv"
    Dataf.to_csv(path_name)

K_list = [10]

nb_appro = 10
for K in K_list :
    param["K"] = K
    Tl , W = simulation(param,nb_appro_tot=nb_appro)
    csv_export(Tl,"Timeline")
    csv_export(W,"Wait")

