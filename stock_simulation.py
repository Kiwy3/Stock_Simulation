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
F=18 #Price
h = 0.05 #Price
p = 20 #Price
b = 5 #Price
Q = 180 #Quantité de commande
r = 5 #Point de recommande
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


col= ["time","event_type","stock","attente","incoming","perte_magasin","deliv"]
timeline = np.full(7,0)
timeline[2] = r


def commande(lamb1,lamb2):
    lamb = lamb1 + lamb2
    t = np.random.exponential(lamb)
    c = np.random.uniform()
    p1 = lamb1/(lamb1+lamb2)
    if c>p1 : 
        cm = 2
    else : 
        cm = 1
    return t,cm

commande(lambda1,lambda2)
i=0
time_appro = 800
t=0
while i<10:
    delay_cmd, type_cmd = commande(lambda1,lambda2)
    time_cmd = delay_cmd+t
    stock_temp = timeline[-1,2]

    #Une commande arrive
    if time_cmd<time_appro : 
        event_temp = type_cmd

        #Commande hors ligne
        if type_cmd ==1: 
            if stock_temp>1: 
                stock_temp -= 1
                deliv_temp = 1
            else : 
                perte_temp = 1

        #Commande en ligne
        else : 
            attente_temp = timeline[-1,3]
            if stock_temp>K:
                stock_temp -= 1
                deliv_temp = 1
            else : 
                attente_temp = 1
    
    #Une livraison arrive
    else : 
        stock_temp += 





    i=i+1




""" full timeline
full_time_array = np.full(max(X["time"]), range(max(X["time"])))
timeline = pd.DataFrame(full_time_array,columns=["time"])"""

"""
i = 1 
while i< len(X):
    X.stock.iloc[i]=X.stock.iloc[i-1]-X.deliv.iloc[i-1]+X.incoming.iloc[i-1]
    X.en_attente.iloc[i]+=X.en_attente.iloc[i-1]
    t = X.index[i]
    
    " => Commande hors ligne (type 1) "
    if X.cmd_type_1.iloc[i]>0:
        if X.stock.iloc[i]>=X.cmd_type_1.iloc[i] : 
            X.deliv.iloc[i] += X.cmd_type_1.iloc[i]
        else : 
            X.perte_magasin.iloc[i] += X.cmd_type_1.iloc[i]
            
            
    " => Commande hors ligne (type 1) "
    if X.cmd_type_2.iloc[i]>0:
        if X.stock.iloc[i]>=X.cmd_type_2.iloc[i] : 
            X.deliv.iloc[i] += X.cmd_type_2.iloc[i]
        else : 
            X.en_attente.iloc[i] += X.cmd_type_2.iloc[i]
            
    " => Recommande fournisseur"
    if X.stock.iloc[i] < r and X.incoming.iloc[i]==0 :
        if t+L in X.index : 
            X.incoming.loc[t+L] = Q
        else : 
            print(X.deliv.iloc[i])
            st = X.stock.iloc[i]-X.deliv.iloc[i]
            X.loc[t+L] = [0,0,st,0,0,Q,0,0]
            X=X.sort_index()
        
        print(t+L)
        X.stock.loc[t+L] = X.stock.loc[t+L]-X.en_attente.loc[t]
        i+=1
        
        
    i+=1
"""
"""Plot the stock evolution
plt.plot(X.index, X.stock)
plt.title("Evolution du stock")
plt.ylim(0)
<<<<<<< HEAD
plt.show()""" 
            

a=1
