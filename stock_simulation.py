# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:44:33 2024

@author: Nathan
"""

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

lambda1 = 15
lambda1 = 30
L = 1
W=1
F=18 #Price
h = 0.05 #Price
p = 20 #Price
b = 5 #Price
Q = 180
r = 5
K = 10

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

"""Mise en place situation initiale"""
X = pd.DataFrame(tirage(15,30,100),columns= ["time","cmd_type_1","cmd_type_2"])
X["stock"] = 0
X.loc[-1]=[0,0,0,r]
X=X.sort_index().set_index("time")
X["nb_cmd"]= X["cmd_type_1"] + X["cmd_type_2"]
X["deliv"]=0
X["incoming"]=0
X["perte_magasin"]=0
X["en_attente"] = 0


""" full timeline
full_time_array = np.full(max(X["time"]), range(max(X["time"])))
timeline = pd.DataFrame(full_time_array,columns=["time"])"""


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

"""Plot the stock evolution"""
plt.plot(X.index, X.stock)
plt.title("Evolution du stock")
plt.ylim(0)
plt.show()
    
            


