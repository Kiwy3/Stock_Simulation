# -*- coding: utf-8 -*-
"""
Génération d'instances résultant de la simulation d'un stock avec une politique de stock
Dans le cadre du cours de CL04
author : Nathan Davouse
"""

import numpy as np
import pandas as pd
import json

#On suppose qu'aucun évenement ne peut arriver totalement en même temps

#Load instances parameters
path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation"
with open(path+"\\"+'param.json') as json_file:
    param = json.load(json_file)


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
    col= ["time","event_type","stock","attente","perte_magasin","deliv"]
    Timeline = pd.DataFrame(columns=col)
    Timeline.loc[0]=np.full(len(col),0)
    Timeline["time"]=Timeline["time"].astype(float)
    #Timeline["late_cost"]=Timeline["late_cost"].astype(float)
    Timeline["deliv"]=Timeline["deliv"].astype(bool)
    Timeline.loc[0,"time"]= 0
    Timeline.loc[0,"stock"]=param["r"]

    #Création de la table d'attente
    Wait_col = ["time","late","release_id"]
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
                    Timeline.loc[i,"deliv"] = True
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
                    Wait.loc[last_w_id:w_id,"release_id"] = i
                    last_w_id = w_id

                #Si la quantité en attente n'est pas comblé par l'approvisionnement
                else : 
                    #Remise à 0 de l'attente sur l'échéancier            
                    Timeline.loc[i,"stock"] -= param["Q"]
                    Timeline.loc[i,"attente"] = Timeline.loc[i-1,"attente"]-param["Q"]
                    #Calcul du cout d'indémnité
                    Wait["late"][Wait["release_id"].isnull()][:param["Q"]]= Wait["time"].apply(lambda x: max(0.,Timeline.loc[i,"time"]-param["W"]-x))
                    Wait["release_id"][Wait["release_id"].isnull()][:param["Q"]] = Timeline.loc[i,"time"]
                    #Gestion de l'échéancier de retard
                    Wait.loc[last_w_id:last_w_id+param["Q"],"late"]=Wait["time"].apply(lambda x: max(0.,Timeline.loc[i,"time"]-param["W"]-x))
                    Wait.loc[last_w_id:last_w_id+param["Q"],"release_id"] = i
                    last_w_id += param["Q"]
                    
        #Recommande
        if Timeline.loc[i,"stock"] < param["r"] and appro==False :
            time_appro = Timeline.loc[i,"time"]+param["L"]
            appro=True

            if appro_count%print_step==0 and impr:
                print("----------------------------------- appro "+str(appro_count)+"/"+str(nb_appro_tot)+"-----------------------------------")

    #return the table
    return Timeline,Wait

def csv_export(Dataf , name,nb_appro,K):
    path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\1.instances"
    csv_name = str(name)+str(nb_appro)+"_K"+str(K)
    path_name = path+"/"+csv_name+".csv"
    Dataf.to_csv(path_name)

K_list = [0,10,20,30,40,50,60]
K_list = [10]
nb_appro = 10
for K in K_list : 
    param["K"] = K
    Tl , W = simulation(param,nb_appro_tot=nb_appro)
    csv_export(Tl,"Timeline",nb_appro,K)
    csv_export(W,"Wait",nb_appro,K)

"""
#small plot
def line_plot(x,serie,col="black",al=1 ,lab = ""):
    plt.plot([0,max(serie)],[x,x],c=col,alpha = al,label = lab)


#Plot the stock
plt.plot(Tl.time, Tl.stock,label = "Stock")
plt.plot(Tl.time, Tl.attente,label = "attente")
line_plot(param["r"],Tl.time,"red",0.6,"Recommend threshold")
line_plot(param["K"],Tl.time,"orange",0.6,"Priority threshold")
plt.title("Stock evolution over time")
plt.xlim(min(Tl.time),max(Tl.time))
plt.ylim(min(Tl.stock),max(Tl.stock)+40)
plt.ylabel("number of products (unit)")
plt.xlabel("time")
plt.legend()
plt.show()"""
