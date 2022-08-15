import numpy as np

'''
input: an array. The step-wise time trace, providing the number of stator units for each time instant. 

output: (1) the dwell times (waiting time for each step), (2) the indices of the array where a change in value occurs (no matter whether it is an increase or a decrease in the number of stator units), (3) the indices where a binding reaction takes place and (4) the indices where an unbinding reaction occurs
'''

def find_dwell(a):    
    d=a[1:]-a[:-1]
    positions=np.where(d**2.>0)[0]
    posP=np.where(d> 0.)[0]
    posM=np.where(d<-0.)[0]
    positions=np.insert(positions, 0, 0)
    dwell_times=positions[1:]-positions[:-1]
    return dwell_times, positions, posP, posM


