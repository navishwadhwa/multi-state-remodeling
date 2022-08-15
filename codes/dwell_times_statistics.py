import numpy as np
import os
from fitting_via_partitioning import *
from process import dwelltimes


data_dir = '../data'
os.chdir(data_dir)

all_times=[]
res=10
th=0.75
lim_ratio=0.995
count_accepted=0

for j in range(128):
    if j not in (59, 75, 90):
	    print('index = ', j)
	    step_fitted=np.loadtxt('step_fitted_trace_%d.txt'%j)
	    if np.min(step_fitted)<3.:
		    count_accepted+=1
		    levels=list( np.sort( list( set(step_fitted) ) ) )		    	

		    stator_number=[]
		    for i in range(len(step_fitted)):
			    stator_number.append(levels.index(step_fitted[i]))

		    if len(levels)>1:
			    t, t_plus, t_minus, n_plus, n_minus = dwelltimes(np.array(stator_number[3500:]), 0.02)
			    for i in range(len(t)):
				    all_times+=t[i]

Hy, hx = np.histogram(all_times, range=(0, 200), bins=66, density=True)
Hx=(hx[:-1]+hx[1:])/2.
np.savetxt('total_dwell_times_distribution_experiments.txt', np.array([Hx, Hy]).T)
		


