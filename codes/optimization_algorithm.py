import numpy as np
import os
from optimization_algorithm_functions import *

data_dir = '../data'
os.chdir(data_dir)

res=10
th=0.75
lim_ratio=0.995

TP=np.loadtxt('meanTp.txt')
TM=np.loadtxt('meanTm.txt')
VP=np.loadtxt('Vp.txt')
VM=np.loadtxt('Vm.txt')
FP=np.loadtxt('fp.txt')
VF=np.loadtxt('error_fp.txt')
TT=np.loadtxt('meanTtot.txt')
VT=np.loadtxt('varTtot.txt')


KP=FP/TT
PREF=VT/TT**2.
tot_n=9
coef_pr=10.
SSp=[]
SSm=[]
CC1=[]
CC2=[]

def loss(p, B=10., coef_pr=coef_pr):
    total_loss=0.      
    A=1./np.mean(VT)
    lam=1e-1
    exp_pref=0.
    th_pref=0.       
    for N in range(tot_n):        
        exp_pref+=PREF[N]
        th_pref+=pref(N, p)            
        Exp=(TT[N], FP[N])
        Th=(tt(N, p), fp(N, p))        
        if N==0:
            total_loss+=A*(Exp[0]-Th[0])**2.+B*(1.-Th[1])**2.+lam*(p[-1]**2.+p[-2]**2.)
        else:           
            total_loss+=lossN(Exp, Th, A, B)+lam*(p[-1]**2.+p[-2]**2.)
    
    exp_pref/=tot_n
    th_pref/=tot_n
    total_loss+=coef_pr*(exp_pref-th_pref)**2.
    return total_loss

length=5*10**5
number_par=tot_n+5
   
if os.path.exists('fitting_parameters.txt'):
    p0=np.loadtxt('fitting_parameters.txt')
else:
    p0=np.zeros(number_par)+0.01
    for i in range(tot_n):
        p0[i]=KP[i]

p=p0
dp=np.zeros(number_par)+1e-5
eta=np.zeros(number_par)+1e-6
eta[-1]=1e-7
alpha=0.1
a=0.
count=0
Loss=[]

for _ in range(length):       
    grad=gradient(loss, p, dp)    
    if count%100==0:
        np.savetxt('fitting_parameters.txt', p)   
            
    a=alpha*a-eta*grad 
    p=p+a
    for i in range(len(p)):
        p[i]=np.max([p[i], 1e-8])
                   

    if count%1000==0:
        print( 'iteration = ', count)
        if Loss:
            print( 'loss = ', Loss[-1])
        Loss.append(loss(p))

    count+=1  



