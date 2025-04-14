import numpy as np
import matplotlib.pyplot as plt

def derivativeNoisy(x_dat , y_dat, xVal, fix):
    
    newx = np.abs(x_dat - xVal)
    index = np.argmin(newx)

    return (y_dat[index+ fix] - y_dat[index-fix]) / (x_dat[index+fix] - x_dat[index-fix])

