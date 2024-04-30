# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:44:33 2024

@author: Nathan
"""

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

#On suppose qu'aucun évenement ne peut arriver totalement en même temps

lambda1 = 15 #Commande hors ligne
lambda2 = 30 #Commande en ligne
L = 1
W=1
F=18 #Prices
h = 0.05 #Price
p = 20 #Price
b = 5 #Price
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

col= ["time","event_type","stock","attente","perte_magasin","deliv"]
Timeline = pd.DataFrame(columns=col)
Timeline.loc[0] = [0.,-1,r,0,0,0]

#Init value
i=1
time_appro = 800
t=0

while i<100:
    Timeline.loc[i]=np.full(6,0)
    
    #Génération nouvelle commande
    delay_cmd, type_cmd = commande(lambda1,lambda2)
    time_cmd = delay_cmd+t

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
            else : 
                Timeline.loc[i,"perte_magasin"] = 1

        #Commande en ligne
        else : 
            Timeline.loc[i,"time"] = time_appro
            Timeline.loc[i,"event_type"]= 2
            if Timeline.loc[i-1,"stock"]>K: #Stock dispo, on livre
                Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]-1
                Timeline.loc[i,"deliv"] = 1
            else : 
                Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]+1
    
    #Une livraison arrive
    else : 
        Timeline.loc[i,"stock"] = Timeline.loc[i-1,"stock"]+ Q
        time_appro += 10*(lambda1+lambda2)
        if Timeline.loc[i-1,"attente"] > 0:
            if Timeline.loc[i-1,"attente"]< Q :                
                Timeline.loc[i,"stock"] -= Timeline.loc[i-1,"attente"]
                Timeline.loc[i,"attente"] = 0
    
    #Recommande
    if Timeline.loc[i,"stock"] < r :
        time_appro = Timeline.loc[i,"time"]+L  




    i=i+1



