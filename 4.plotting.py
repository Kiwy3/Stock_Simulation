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
#test = Sample_T.where[Sample_T.attente>0].time
plt.plot(Sample_T.time, Sample_T.stock,label = "Stock")
plt.plot(Sample_T.time, Sample_T.attente,alpha = 0.8,label = "attente")
line_plot(param["r"],Sample_T.time,"red",0.6,"Seuil de recommande")
line_plot(param["K"],Sample_T.time,"orange",0.7,"Seuil de priorité")
plt.xlim(min(Sample_T.time),max(Sample_T.time))
plt.ylim(0,max(Sample_T.stock)+40)
plt.ylabel("nombre de produit (unité)")
plt.xlabel("temps (jours)")
plt.legend()
plt.show()

#F3 : cost evolution
mean_cost = Results.loc[1,"avg_total_cost"]
Sample_T = Timeline[:4000]
plt.plot(Sample_T.time, Sample_T.mean_cost,label = "cout moyen à l'instant t")
line_plot(mean_cost,Sample_T.time,"red",0.6,"cout moyen de l'instance")
plt.xlim(min(Sample_T.time),max(Sample_T.time))
plt.ylim(0)
plt.ylabel("cout (€)")
plt.xlabel("temps (jours)")
plt.legend()
plt.show()

#F4 : pct of cost for K10
myMap = plt.get_cmap('Pastel1')
indices = [0.1,0.2,0.3,0.4]
size = Results.loc[1,"loss_pct":"passation_pct"]
label = ["Perte de vente","Cout de stockage","Indemnité de retard","Cout de passation"]
fig, ax = plt.subplots()
ax.pie(size, labels=label,pctdistance=0.6,colors=myMap(indices), autopct='%1.1f%%')
plt.show()




#F5 : pct of costs for each K
fig, ax = plt.subplots()
ax.bar(Results.K, Results["late_pct"],label = "Indemnité de retard",width=3,color = myMap(0.3))
ax.bar(Results.K, Results["stock_pct"],label = "Cout de stockage", bottom = Results["late_pct"],width=3,color = myMap(0.2) )
ax.bar(Results.K, Results["passation_pct"], bottom=Results["stock_pct"]+Results["late_pct"], label="Cout de passation",width=3,color = myMap(0.4))
ax.bar(Results.K, Results["loss_pct"], bottom=Results["stock_pct"]+Results["late_pct"]+Results["passation_pct"], label="Perte de vente",width=3,color = myMap(0.1))

# Configuration des axes
ax.set_xlabel("K (unité)")
ax.set_ylabel("Pourcentage du cout total (%)")
ax.legend(loc=4)
plt.show()



