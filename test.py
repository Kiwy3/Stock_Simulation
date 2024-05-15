import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = "C:\\Users\\Nathan\\CL04\\Stock_Simulation\\"
Results = pd.read_csv(path+"results.csv")


from plot_lib import st

st(Results)
