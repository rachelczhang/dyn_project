import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 

##### ensure that all of the initial conditions across the COSMIC and CMC simulations are all the same #####

# extract COSMIC data

bcm_data = pd.read_hdf('field/bcm.h5', 'bcm')

#bcm_init_kstar1 = bcm_data[bcm_data['tphys'] == 0]['kstar_1']
#bcm_init_kstar2 = bcm_data[bcm_data['tphys'] == 0]['kstar_2']
#bcm_init = pd.concat([bcm_init_kstar1, bcm_init_kstar2])

sep = bcm_data[bcm_data['tphys'] == 0]['sep'] # in solar radii
sep = [i/215.032 for i in sep] # in AU
#porb = bcm_data[bcm_data['tphys'] == 0]['porb']
print('COSMIC sep', [i for i in sep if i > 250])

# extract CMC data for each rv
cmc_15 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv1.5/king.snapshots.h5', key='0(t=0)')
cmc_20 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0/king.snapshots.h5', key='0(t=0)')
#cmc_20_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0_modified/king.snapshots.h5', key='0(t=0)')
cmc_20_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0_modified/king.snapshots.h5', key='1(t=9.026307e-07)')
cmc_60 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv6.0/king.snapshots.h5', key='0(t=0)')
cmc_80 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv8.0/king.snapshots.h5', key='0(t=0)')
a_15 = cmc_15['a_AU']
a_20 = cmc_20['a_AU']
a_20_mod = cmc_20_mod['a_AU']
a_60 = cmc_60['a_AU']
a_80 = cmc_80['a_AU']
print('a 15', a_15)
print('a 20', a_20)

#plt.hist(sep, bins=np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50), label='COSMIC', histtype='step', linewidth=2.5)
plt.hist(a_15, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 200), label='CMC rv1.5', linewidth=2.5, histtype='step')
plt.hist(a_20, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 200), label='CMC rv2.0', histtype='step')
plt.hist(a_20_mod, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 200), label='CMC rv2.0 mod', histtype='step')
#plt.hist(a_60, bins=np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50), label='CMC rv6.0', histtype='step')
#plt.hist(a_80, bins=np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50), label='CMC rv8.0', histtype='step')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.savefig('init_a.png')

