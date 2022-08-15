import numpy as np
import os
from fitting_via_partitioning import *
import scipy.io as sio

data_dir = '../data'

os.chdir(data_dir)

all_data=sio.loadmat('remodeling_data.mat')
ind=13 # the index of the trace from the data

stoich=all_data['stoich']
for ind in range(len(stoich[0])):
    frequency = stoich[0, ind]['f'].T
    data=np.concatenate(frequency) # note that here I am converting it into a 1-D vector
    print(data)
    inter, averages, step_fitted, levels=get_int_av(data, res=10, th=0.75, limit_ratio=0.995)    
    np.savetxt('step_fitted_trace_%d.txt'%ind, step_fitted)

