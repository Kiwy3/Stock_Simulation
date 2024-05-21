# -*- coding: utf-8 -*-
"""
Création de graphique pour alimenter le rapport 
Dans le cadre du cours de CL04
author : Nathan Davouse
"""
#Librairies
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

#Import Data
Results = pd.read_csv("results.csv")
Timeline = pd.read_csv("2.Instances_costs\\Finished_T1000_K10.csv")
with open('param.json') as json_file:
    param = json.load(json_file)

#Useful fonction for figure X
def line_plot(x,serie,col="black",al=1 ,lab = ""):
    plt.plot([0,max(serie)],[x,x],c=col,alpha = al,label = lab)

#F2 : Stock_evolution
Sample_T = Timeline[:1000]
plt.plot(Sample_T.time, Sample_T.stock,label = "Stock")
plt.plot(Sample_T.time, Sample_T.attente,label = "attente")
line_plot(param["r"],Sample_T.time,"red",0.6,"Recommend threshold")
line_plot(param["K"],Sample_T.time,"orange",0.7,"Priority threshold")
plt.title("Stock evolution over time")
plt.xlim(min(Sample_T.time),max(Sample_T.time))
plt.ylim(0,max(Sample_T.stock)+40)
plt.ylabel("number of products (unit)")
plt.xlabel("time")
plt.legend()
plt.show()

#F3 : cost evolution
mean_cost = Results.loc[1,"avg_total_cost"]
Sample_T = Timeline[:4000]
plt.plot(Sample_T.time, Sample_T.mean_cost,label = "Mean cost over time")
line_plot(mean_cost,Sample_T.time,"red",0.6,"average cost")
plt.title("Mean cost evolution over time")
plt.xlim(min(Sample_T.time),max(Sample_T.time))
plt.ylim(0)
plt.ylabel("cost (€)")
plt.xlabel("time")
plt.legend()
plt.show()

#F4 : pct of cost for K10
size = Results.loc[1,"loss_pct":"passation_pct"]
label = ["Late costs","Stock costs","Passation costs","Loss costs"]
fig, ax = plt.subplots()
ax.pie(size, labels=label,colors=['olivedrab', 'gray', 'saddlebrown', 'rosybrown'],pctdistance=0.6, autopct='%1.1f%%')
plt.show()

#F5 : pct of costs for each K

plt.plot(Results.K,Results["late_pct"],label = "late")
plt.plot(Results.K,Results["stock_pct"],label = "stock")
plt.plot(Results.K,Results["passation_pct"],label = "passation")
plt.plot(Results.K,Results["loss_pct"],label = "loss")
plt.title("Percentage of each costs by K")
plt.ylim(0,100)
plt.xlim(0,60)
plt.xlabel("K")
plt.ylabel("Pourcentage du cout")
plt.legend()
plt.show()
