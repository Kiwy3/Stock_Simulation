import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\"
Results = pd.read_csv(path+"results.csv")


import plotting_lib

a = plotting_lib.st(Results)

Timeline = pd.read_csv("C:\\Users\\Nathan\\CL04\\Stock_Simulation\\2.Instances_costs\\Finished_T1000_K60.csv")

#a = plotting_lib.Stock_evolution(Timeline,60)