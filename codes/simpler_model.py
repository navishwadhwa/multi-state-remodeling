'''
Here we create time traces in the case of a simple model of binding/unbinding through stochastic simulations. 
We use two values of the unbinding rate koff.


'''

import numpy as np
import os
from simul_parameters import *


def update_site(site):
    if site==0:
        if np.random.rand()<dt*kon:    
            return 1    
        else:
            return 0

    else:
        if np.random.rand()<dt*koff:    
            return 0    
        else:
            return 1


data_dir='../data_simulations'
os.chdir(data_dir)


for koff in (koff1, koff2):
    for realiz in range(realizations):
        sites=np.zeros(number_sites)
        print('realiz = ', realiz)
        stator_number=[]
        count=0
        for _ in range(n_steps):
            count+=1
            if count%10000==0:
                print('count = ', count)
            for i in range(len(sites)):
                sites[i]=update_site(sites[i])
            
            stator_number.append(np.sum(sites))
        
        np.savetxt('Trace_%d_koff_%g_ttot_%d.txt'%(realiz, koff, ttot), stator_number)
    

