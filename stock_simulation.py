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
r = 60
K = 10

def tirage(l1,l2,n):   
   Tempo = np.full((n,2),0)
   t1 = 0
   t2 = 0
   i=0
   p1 = np.random.poisson(l1,1)
   p2 = np.random.poisson(l2,1)
   print(p1,p2)
   for i in range(100):
       if t1+p1<t2+p2:
           Tempo[i,0]= t1+p1
           Tempo[i,1] = 1
           p1 = np.random.poisson(l1,1)
           t1 = t1+p1
       else : 
           Tempo[i,0]= t2+p2
           Tempo[i,1] = 2
           p2 = np.random.poisson(l2,1)
           t2 = t2+p2      
       
   return Tempo
"""Mise en place situation initiale"""
X = pd.DataFrame(tirage(15,30,100),columns= ["time","cmd type"])
X["stock"] = 0
X.loc[-1]=[0,0,r]
X=X.sort_index().reset_index(drop=True)

for i in range (100): #define it

    if X.type[i] =1 : 
        pass


