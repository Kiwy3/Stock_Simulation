import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

#path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\"
Results = pd.read_csv("results.csv")


import plotting_lib

#plotting_lib.stock(Results)

Timeline = pd.read_csv("2.Instances_costs\\Finished_T1000_K10.csv")



def line_plot(x,serie,col="black",al=1 ,lab = ""):
    plt.plot([0,max(serie)],[x,x],c=col,alpha = al,label = lab)


def Stock_evolution(Timeline,stock_avg):
    with open('param.json') as json_file:
        param = json.load(json_file)

    plt.plot(Timeline.time, Timeline.stock,label = "Stock")
    plt.plot(Timeline.time, Timeline.attente,label = "attente")
    #line_plot(stock_avg,Timeline.time,"black",0.8,"Average")
    line_plot(param["r"],Timeline.time,"red",0.6,"Recommend threshold")
    line_plot(param["K"],Timeline.time,"orange",0.7,"Priority threshold")
    plt.title("Stock evolution over time")
    plt.xlim(min(Timeline.time),max(Timeline.time))
    plt.ylim(0,max(Timeline.stock)+40)
    plt.ylabel("number of products (unit)")
    plt.xlabel("time")
    plt.legend()
    plt.show()

def cost(Timeline,mean_cost):
    with open('param.json') as json_file:
        param = json.load(json_file)
    plt.plot(Timeline.time, Timeline.mean_cost,label = "Mean cost over time")
    line_plot(mean_cost,Timeline.time,"red",0.6,"average cost")
    plt.title("Mean cost evolution over time")
    plt.xlim(min(Timeline.time),max(Timeline.time))
    plt.ylim(0)
    plt.ylabel("cost (€)")
    plt.xlabel("time")
    plt.legend()
    plt.show()

#cost(Timeline[:4000],31.8)
"""
total_late = Timeline["late_cost"].sum()
total_stock = Timeline["stock_cost"].sum()
total_passation = Timeline["passation_cost"].sum()
total_loss = Timeline["Loss_cost"].sum()
size = [total_late,total_stock,total_passation,total_loss]
label = ["Late costs","Stock costs","Passation costs","Loss costs"]
fig, ax = plt.subplots()
ax.pie(size, labels=label,colors=['olivedrab', 'gray', 'saddlebrown', 'rosybrown'],pctdistance=0.6, autopct='%1.1f%%')
"""

Results["Total cost"] = Results["Late costs"]+Results["Loss costs"]+Results["Passation costs"]+Results["Stock costs"]
Results["loss_pct"] = Results["Loss costs"]/Results["Total cost"]*100
Results["late_pct"] = Results["Late costs"]/Results["Total cost"]*100
Results["stock_pct"] = Results["Stock costs"]/Results["Total cost"]*100
Results["passation_pct"] = Results["Passation costs"]/Results["Total cost"]*100

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
