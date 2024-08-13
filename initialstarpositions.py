import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

cmc2_init = pd.read_hdf('dynamics/rv2.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
cmc6_init = pd.read_hdf('dynamics/rv6.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
cmc10_init = pd.read_hdf('dynamics/rv10.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
cmc20_init = pd.read_hdf('dynamics/rv20_modified/king.window.snapshots.h5', key='0(t=0Gyr)')

r_2 = [i*2 for i in cmc2_init['r']]
r_6 = [i*6 for i in cmc6_init['r']]
r_10 = [i*10 for i in cmc10_init['r']]
r_20 = [i*20 for i in cmc20_init['r']]

m0_2 = [i for i in cmc2_init['m0_MSUN']]
m0_6 = [i for i in cmc6_init['m0_MSUN']]
m0_10 = [i for i in cmc10_init['m0_MSUN']]
m0_20 = [i for i in cmc20_init['m0_MSUN']]

if m0_2 == m0_6:
        print('rv2 and 6 are the same')
if m0_6 == m0_10:
        print('rv6 and 10 are the same')
if m0_10 == m0_20:
        print('rv10 and 20 are the same')

plt.hist(r_2,  bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, label='rv2', histtype='step')
plt.hist(r_6, bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, label='rv6', histtype='step')
plt.hist(r_10, bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, label='rv10', histtype='step')
plt.hist(r_20, bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, label='rv20', histtype='step')
plt.legend(loc='upper left')
plt.xscale('log')
plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams.update({'font.size': 18})
plt.xlabel('Clustercentric radial position [pc]')
plt.ylabel('Fraction of binaries')
plt.savefig('initpositions.png')
