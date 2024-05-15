
import json
path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation"

param = {
        #Commandes
        "lambda1" : 15 #Commande hors ligne
         ,"lambda2" : 30 #Commande en ligne
        #Approvisionnement
        ,"L" : 2 #Délai de livraison approvisionnement
        ,"W" : 1 # Délai acceptable pour une commande en ligne
        ,"Q" : 180 #Quantité de commande
        ,"r" : 60 #Point de recommande
        #Couts
        ,"F" : 18 #Cout de passation de commandE
        ,"h" : 0.05 #Cout de stockage
        ,"p" : 20 #Cout de perte unitaire
        ,"b" : 5 #Indemnité de retard
        #Paramètre de priorisation
        ,"K" : 10 #Priorité de classe
}


with open(path + "\\param.json", "w") as outfile: 
    json.dump(param, outfile)

