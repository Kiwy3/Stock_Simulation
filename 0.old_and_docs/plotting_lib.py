import matplotlib.pyplot as plt
import json

def stock(Results):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    fig.suptitle("Comparaison entre le stock moyen et la perte induite ")
    #Axe 2
    ax1.plot(Results.K,Results.stock_avg,c="orange",label="stock average")
    ax1.set_ylim(50,105)
    ax1.set_ylabel("Stock moyen (unité)")
    #Axe 2
    ax2 = ax1.twinx()  
    ax2.set_ylim(0, 50)
    ax2.plot(Results.K,Results.ratio_mag*100,c = "red",label = "Magasin")
    ax2.plot(Results.K,Results.ratio_ligne*100,c="blue",label="En ligne")
    ax2.set_ylabel("Perte ou retard (%)")
    #Global fig
    ax1.set_xlabel("K")
    fig.legend()
    fig.show()
    return 0

def line_plot(x,serie,col="black",al=1 ,lab = ""):
    plt.plot([0,max(serie)],[x,x],c=col,alpha = al,label = lab)


def Stock_evolution(Timeline,stock_avg):
    with open('param.json') as json_file:
        param = json.load(json_file)

    plt.plot(Timeline.time, Timeline.stock,label = "Stock")
    plt.plot(Timeline.time, Timeline.attente,label = "attente")
    line_plot(stock_avg,Timeline.time,"black",0.8,"Average")
    line_plot(param["r"],Timeline.time,"red",0.6,"Recommend threshold")
    line_plot(param["r"],Timeline.time,"orange",0.6,"Priority threshold")
    plt.title("Stock evolution over time")
    plt.xlim(min(Timeline.time),max(Timeline.time))
    plt.ylim(min(Timeline.stock),max(Timeline.stock)+40)
    plt.ylabel("number of products (unit)")
    plt.xlabel("time")
    plt.legend()
    plt.show()

