def st(Results):
    import matplotlib.pyplot as plt
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