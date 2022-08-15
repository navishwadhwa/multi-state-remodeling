'''
Here we create the step function from the time trace of the rotational frequencies as a function of time. 
We iteratively partition the function with a division in the point leading to the lowest variance (where the variance is defined as the square sum of the difference between the averaged step fitting function and the original trace). The iteration stops when a new partition would not provide a new variance that is significantly smaller than what would be obtained with random partitioning. 

Once this first steps is complete, we need to associate the same stator number to segments that are very close. In order to do so, we iteratively select the couple of segments with the minimal difference and we equate both of them to their weighted average until the difference is larger than a given threshold.   

'''


import numpy as np
from scipy.optimize import curve_fit

def get_variance(data, inter, pos):
    attempt=inter[:np.searchsorted(inter, pos)]+[pos]+inter[np.searchsorted(inter, pos):]
    delta=list(data[:attempt[0]]-np.mean(data[:attempt[0]]))            
    for i in range(len(attempt)-1):
        delta+=list( data[attempt[i]:attempt[i+1]]-np.mean(data[attempt[i]:attempt[i+1]]) )
    delta+=list( data[attempt[-1]:]-np.mean(data[attempt[-1]:]) )
    #print(np.mean(np.array(delta)**2.))                   
    return np.mean(np.array(delta)**2.)


def get_pos(data, inter, res=50):
    variance=100
    for pos in range(res, len(data)-res, res):
        if pos not in inter:
            v=get_variance(data, inter, pos)
            if v<variance:
                variance=v
                best_pos=pos
                       
    inter=inter[:np.searchsorted(inter, best_pos)]+[best_pos]+inter[np.searchsorted(inter, best_pos):]      
    return best_pos, inter, variance
    

def get_int_av(data, res, th=0.8, limit_ratio=0.99):
    inter=[0]
    variance=100
    v=1000
    v_random=200
    real=10
    while variance/v_random<limit_ratio:
        print('ratio =',  variance/v_random)
        v=variance        
        v_random=0
        for _ in range(real):
            random_pos=np.random.choice(range(len(data))) 
            v_random+=get_variance(data, inter, random_pos)
        
        v_random/=real                
        best_pos, inter, variance = get_pos(data, inter, res=res)       
        
    averages=[np.mean(data[inter[i]:inter[i+1]]) for i in range(len(inter)-1)]  
    averages+=[np.mean(data[inter[-1]:])]    
    inter+=[len(data)-1]
    ind=np.argsort(averages)
    levels=np.sort(averages)
    positions=[[( inter[ind[i]], inter[ind[i]+1] )] for i in range(len(ind))]
    if len(levels)>1:
        while len(levels)>1 and np.min(levels[1:]-levels[:-1])<th:
            phi=np.argmin(levels[1:]-levels[:-1])        
            distance0=0.
            for j in range(len(positions[phi])):
                distance0+=positions[phi][j][1]-positions[phi][j][0]

            distance1=0.
            for j in range(len(positions[phi+1])):
                distance1+=positions[phi+1][j][1]-positions[phi+1][j][0]        
            
            levels[phi]=(distance0*levels[phi]+distance1*levels[phi+1])/(distance0+distance1)
            levels=np.delete(levels, phi+1)            
            positions[phi]+=positions[phi+1]
            positions.pop(phi+1)

        step_fitted=np.zeros(len(data)-1)
        for i in range(len(positions)):
            for j in range(len(positions[i])):
                step_fitted[positions[i][j][0]:positions[i][j][1]]=levels[i]
    else:
        step_fitted=[]
        for i in range(len(inter)-1):
            step_fitted+=list(np.zeros(inter[i+1]-inter[i])+averages[i])
        
    levels=list(levels)      
    levels=np.array(levels)                       
    return inter, averages, step_fitted, levels 
 
