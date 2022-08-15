'''
Here we compute the quantities in which we are interested from the experimental data. We use the time traces after the step fitting process and calculate everything we need for the dwell time statistics. 
Then we will save the results in txt files. 

'''

import numpy as np
import os
from fitting_via_partitioning import *
from process import dwelltimes
from matplotlib import pyplot as plt
import scipy.io as sio
from scipy import optimize as opt

data_dir = '../data'

os.chdir(data_dir)

time=[]
timep=[]
timem=[]

all_times=[]
T_tot=[[] for i in range(12)]
T_plus=[[] for i in range(12)]
T_minus=[[] for i in range(12)]
N_plus=np.zeros(12)
N_minus=np.zeros(12)

res=10
th=0.75
lim_ratio=0.995
all_plus=[[],[],[],[],[],[],[],[],[],[],[],[]]
all_minus=[[],[],[],[],[],[],[],[],[],[],[],[]]


for j in range(128):
	print( 'index = ', j)
	step_fitted=np.loadtxt('step_fitted_trace_%d.txt'%j)
	if np.min(step_fitted)<1.:
		levels=list(np.sort(list(set(step_fitted))))					
		stator_number=[]
		for i in range(len(step_fitted)):
			stator_number.append(levels.index(step_fitted[i]))
					
		if len(levels)>1:
			t, t_plus, t_minus, n_plus, n_minus = dwelltimes(np.array(stator_number[3500:]), 0.02)
			for i in range(min([len(t), len(T_tot)])):
				all_times+=t[i]
				T_tot[i]+=t[i]
				T_plus[i]+=t_plus[i]
				T_minus[i]+=t_minus[i]
				N_plus[i]+=n_plus[i]
				N_minus[i]+=n_minus[i]
				all_plus[i]+=[n_plus[i]]
				all_minus[i]+=[n_minus[i]]

sp=[]
sm=[]
mp=[]
mm=[]
for i in range(len(all_plus)):
    sp.append(np.sqrt(np.var(all_plus[i])))
    sm.append(np.sqrt(np.var(all_minus[i])))
    mp.append(np.mean(all_plus[i]))
    mm.append(np.mean(all_minus[i]))

sp=np.array(sp)
sm=np.array(sm)
mp=np.array(mp)
mm=np.array(mm)


error_r=np.sqrt( ( sp/(mm+mp)-sp*mp/(mm+mp)**2. )**2. + ( -sm*mp/(mm+mp)**2. )**2.  )
tt=[np.mean(T_tot[i]) for i in range(len(T_tot))]
vt=[np.var(T_tot[i]) for i in range(len(T_tot))]
tp=[np.mean(T_plus[i]) for i in range(len(T_plus))]
vp=[np.var(T_plus[i]) for i in range(len(T_plus))]
tm=[np.mean(T_minus[i]) for i in range(len(T_minus))]
vm=[np.var(T_minus[i]) for i in range(len(T_minus))]
r=np.array(N_plus)/(np.array(N_plus)+np.array(N_minus))

np.savetxt('meanTtot.txt', tt)
np.savetxt('varTtot.txt', vt)
np.savetxt('meanTp.txt', tp)
np.savetxt('meanTm.txt', tm)
np.savetxt('Vp.txt', vp)
np.savetxt('Vm.txt', vm)
np.savetxt('fp.txt', r)
np.savetxt('error_fp.txt', error_r)

