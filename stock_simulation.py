# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:44:33 2024

@author: Nathan
"""

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import math

#On suppose qu'aucun évenement ne peut arriver totalement en même temps

lambda1 = 15 #Commande hors ligne
lambda2 = 30 #Commande en ligne
L = 1 #Délai de livraison approvisionnement
W=1 # Délai acceptable pour une commande en ligne
F=18 #Cout de passation de commande
h = 0.05 #Cout de stockage
p = 20 #Cout de perte unitaire
b = 5 #Indemnité de retard
Q = 180 #Quantité de commande
r = 60 #Point de recommande
K = 10 #Priorité de classe

def tirage(l1,l2,n):   
   Tempo = np.full((n,3),0)
   """quantite de la demande"""
   d1 = 1
   d2 = 30
   t1 = 0
   t2 = 0
   i=0
   p1 = np.random.poisson(l1,1)
   p2 = np.random.poisson(l2,1)
   for i in range(100):
       if t1+p1<t2+p2:
           Tempo[i,0]= t1+p1
           Tempo[i,1] = d1
           p1 = np.random.poisson(l1,1)
           t1 = t1+p1
       elif t1+p1==t2+p2: 
           Tempo[i,0]= t2+p2
           Tempo[i,1] = d1
           Tempo[i,2] = d2
           p1 = np.random.poisson(l1,1)
           t1 = t1+p1 
           p2 = np.random.poisson(l2,1)
           t2 = t2+p2
       else : 
           Tempo[i,0]= t2+p2
           Tempo[i,2] = d2
           p2 = np.random.poisson(l2,1)
           t2 = t2+p2            
   return Tempo

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

#Création de l'échéancier en utilisant la librairie pandas
col= ["time","event_type","stock","attente","perte_magasin","deliv","late_cost"]
Timeline = pd.DataFrame(columns=col)
Timeline.loc[0]=np.full(len(col),0)
Timeline["time"]=Timeline["time"].astype(float)
Timeline["late_cost"]=Timeline["late_cost"].astype(float)
Timeline.loc[0,"time"]= -1
Timeline.loc[0,"stock"]=r

#Création de la table d'attente
Wait_col = ["time","late"]
Wait = pd.DataFrame(columns=Wait_col)
w_id = 0

#Init value
i=0
time_appro = 800
t=0
appro=False
appro_count = 0
time_cmd, type_cmd = commande(lambda1,lambda2)
nb_appro_tot = 1000 #Nb d'approvisionnement pour l'horizon de simulation
print_step = 100

while appro_count<nb_appro_tot:
    #Print l'avancement
    if appro_count%print_step==0:
        print("------------------- approvisionnement ",appro_count,"/",nb_appro_tot,"----------------")


    i+=1 #indice du tableau
    #Création nouvelle ligne et conservation des états si nécessaire
    Timeline.loc[i]=np.full(len(col),0)
    Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]


    #Une commande arrive
    if time_cmd<time_appro : 
        Timeline.loc[i,"time"] = time_cmd
        event_temp = type_cmd

        #Commande hors ligne
        if type_cmd ==1: 
            Timeline.loc[i,"event_type"]=1
            if Timeline.loc[i-1,"stock"]>1: #Stock dispo, on livre
                Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]-1
                Timeline.loc[i,"deliv"] = 1
            else : #Stock indispo, perte d'une cmd
                Timeline.loc[i,"perte_magasin"] = 1

        #Commande en ligne
        else : 
            Timeline.loc[i,"event_type"]= 2
            if Timeline.loc[i-1,"stock"]>K: #Stock supérieur à K, on livre
                Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]-1
                Timeline.loc[i,"deliv"] = 1
            else : #Stock inférieur à K, on met en attente
                Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]+1
                Wait.loc[w_id,"time"]=Timeline.loc[i,"time"] #On ajoute un nouveau temps au tableau d'attente
                w_id+=1

        
        #Génération nouvelle commande
        delay_cmd, type_cmd = commande(lambda1,lambda2)
        time_cmd = delay_cmd+Timeline.loc[i,"time"]

    #Une livraison arrive
    else : 
        appro_count += 1
        Timeline.loc[i,"event_type"]= 3
        Timeline.loc[i,"time"] = time_appro
        Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]+ Q
        time_appro += 10*(lambda1+lambda2)
        appro=False
        if Timeline.loc[i-1,"attente"] > 0:
            if Timeline.loc[i-1,"attente"]< Q :
                #Remise à 0 de l'attente sur l'échéancier            
                Timeline.loc[i,"stock"] -= Timeline.loc[i-1,"attente"]
                Timeline.loc[i,"attente"] = 0
                #Calcul du cout d'indémnité
                Wait["late"]=Wait["time"].apply(lambda x: max(0.,Timeline.loc[i,"time"]-W-x))
                Timeline.loc[i,"late_cost"]=sum(Wait["late"])*b
                
                Wait.drop(Wait.index ,inplace=True)
                w_id=0
    
    #Recommande
    if Timeline.loc[i,"stock"] < r and appro==False :
        time_appro = Timeline.loc[i,"time"]+L
        appro=True
    

# Calcul des couts
Timeline["passation_cost"] = Timeline["event_type"].apply(lambda x :F if x==3 else 0)
Timeline["Time_gap"] = Timeline["time"].diff(periods=-1)*-1
Timeline["Time_gap"] = Timeline["Time_gap"].apply(lambda x : 0 if math.isnan(x) else x)
Timeline["stock_cost"] = Timeline["stock"]*h * Timeline["Time_gap"]
Timeline["Loss_cost"] = Timeline["perte_magasin"]*p
Timeline["Total_cost"] = Timeline["Loss_cost"]+Timeline["stock_cost"]+Timeline["late_cost"]+Timeline["passation_cost"]
Timeline["Cum_cost"]= Timeline["Total_cost"].cumsum()
Timeline["mean_cost"] = Timeline["Cum_cost"]/Timeline["time"]

#Indicateurs de stock
stock_avg = sum(Timeline["stock"]*Timeline["Time_gap"])/Timeline.loc[i,"time"]

def line_plot(x,serie,col="black",al=1 ,lab = ""):
    plt.plot([0,max(serie)],[x,x],c=col,alpha = al,label = lab)


#Plot the stock
plt.plot(Timeline.time, Timeline.stock,label = "Stock")
line_plot(stock_avg,Timeline.time,"black",0.8,"Average")
line_plot(r,Timeline.time,"red",0.6,"Recommend threshold")
line_plot(K,Timeline.time,"orange",0.6,"Priority threshold")
plt.title("Stock evolution over time")
plt.xlim(0,max(Timeline.time))
plt.ylim(0,max(Timeline.stock)+20)
plt.legend()
plt.show()

#Plot the cost

plt.plot(Timeline.time,Timeline.mean_cost)
plt.show()