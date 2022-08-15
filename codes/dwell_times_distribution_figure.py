'''
This file will use the time traces from experiments and from the simulations (simplified model) to make the figure of the distribution of the dwell time.


'''

import numpy as np
import os
import time
import pandas as pd
from dwell_times_function import find_dwell
from matplotlib import pyplot as plt
from simul_parameters import *

top=0.9
btm=0.2
lf=0.2
rt=0.9
ls=120
fts=120
top=0.85
btm=0.35
lf=0.35
rt=0.85

data_dir='../data_simulations'
os.chdir(data_dir)
realizations =130

for koff in (koff1, koff2):
    if not os.path.exists('dwell_times_simplified_simul_koff_%g.txt'%koff):
        dwell=[]
        for realiz in range(realizations):
            if realiz%100==0:
                print('real = ', realiz)
            trace=np.loadtxt('Trace_%d_koff_%g_ttot_%d.txt' % (realiz, koff, ttot))
            last_index=int(360./dt)
            trace=trace[:last_index]
            dwell+=list(find_dwell(trace)[0])

        np.savetxt('dwell_times_simplified_simul_koff_%g.txt'%koff, np.array(dwell)*dt)


symboltab=('v', 'o')

fig=plt.figure('dwell times', figsize=(24, 0.69*20.))
plt.subplots_adjust(left=lf, right=rt, top=top, bottom=btm)
ax=fig.add_subplot(111)

ms=14
o=0
for koff in (koff1, koff2):
    dwell_times=np.loadtxt('dwell_times_simplified_simul_koff_%g.txt'% koff)
    Hy, hx =np.histogram(dwell_times, bins=int(np.max(dwell_times)/2.), density=True)
    Hx=(hx[1:]+hx[:-1])/2.
    dati=np.array([Hx, Hy]).T
    np.savetxt('Fig_1C_k_off_%g.txt'%koff, dati)
    ax.plot(Hx, Hy, symboltab[o], color='k', ms=ms, label=r'two states model ($k_{off}=%g\,s^{-1}$)'%koff)
    o+=1
    ax.set_yscale('log')


for ax in (ax,):
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(4)

data_dir='../data'
os.chdir(data_dir)

exp_distr=np.loadtxt('total_dwell_times_distribution_experiments.txt')
exp_x=exp_distr[:, 0]
exp_y=exp_distr[:, 1]
ax.plot(exp_x, exp_y, 's', color='red', ms=ms, label=r'experiments')
ax.legend(fontsize=30)
ax.set_xlabel(r'$\tau (s)$', fontsize=30, labelpad=30)
ax.set_ylabel(r'$P(\tau)$', fontsize=30, rotation='vertical', labelpad=40)
ax.tick_params(labelsize=25, pad=25, length=10, width=5)

data_dir='../figures'
os.chdir(data_dir)

fig.savefig('dwell_times_distr_simulations_simple_model_and_exp_real_%d.pdf'%realizations)


