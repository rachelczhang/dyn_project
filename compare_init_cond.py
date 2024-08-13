import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 

##### ensure that all of the initial conditions across the COSMIC and CMC simulations are all the same #####

# extract COSMIC data

bcm_data = pd.read_hdf('fieldmetfix/bcm.h5', 'bcm')

#bcm_init_kstar1 = bcm_data[bcm_data['tphys'] == 0]['kstar_1']
#bcm_init_kstar2 = bcm_data[bcm_data['tphys'] == 0]['kstar_2']
#bcm_init = pd.concat([bcm_init_kstar1, bcm_init_kstar2])

sep = bcm_data[bcm_data['tphys'] == 0]['sep'] # in solar radii
sep = [i/215.032 for i in sep] # in AU
#porb = bcm_data[bcm_data['tphys'] == 0]['porb']
print('COSMIC sep', [i for i in sep if i > 250])
ecc = bcm_data[bcm_data['tphys'] == 0]['ecc']

# extract CMC data for each rv
#cmc_15 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv1.5/king.snapshots.h5', key='0(t=0)')
#cmc_20 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0/king.snapshots.h5', key='0(t=0)')
cmc_20_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0_modified/king.snapshots.h5', key='0(t=0)')
#cmc_20_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0_modified/king.snapshots.h5', key='1(t=9.026307e-07)')
#cmc_60 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv6.0_modified/king.snapshots.h5', key='0(t=0)')
#cmc_80 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv8.0/king.snapshots.h5', key='0(t=0)')
cmc_100_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv10.0_modified/king.snapshots.h5', key='0(t=0)')
cmc_200_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv20_modified/king.snapshots.h5', key='0(t=0)')

#a_15 = cmc_15['a_AU']
#a_20 = cmc_20['a_AU']
a_20 = cmc_20_mod['a_AU']
#a_60 = cmc_60['a_AU']
#a_80 = cmc_80['a_AU']
a_100 = cmc_100_mod['a_AU']
a_200 = cmc_200_mod['a_AU']
#print('a 15', a_15)
#print('a 20', a_20)
e_20 = cmc_20_mod['e']
e_100 = cmc_100_mod['e']
e_200 = cmc_200_mod['e']

plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams.update({'font.size': 13})
plt.hist(sep, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 100), label='COSMIC', histtype='step')
#plt.hist(a_15, bins=np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50), label='CMC rv1.5', linewidth=2.5, histtype='step')
#plt.hist(a_20_mod, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 200), label='CMC rv2.0 mod', histtype='step')
#plt.hist(a_60, bins=np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50), label='CMC rv6.0', histtype='step')
#plt.hist(a_80, bins=np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50), label='CMC rv8.0', histtype='step')
#plt.hist(a_200, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 100), label='CMC rv20', histtype='step')
#plt.hist(a_100, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 100), label='CMC rv10', histtype='step')
plt.hist(a_20, bins=np.logspace(np.log10(10**(-3)), np.log10(10**4), 100), label='CMC rv2', histtype='step')
plt.title('Semimajor axis of all binaries initially')
plt.xlabel('Semimajor Axis [AU]')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.savefig('init_a.png')

#plt.hist(ecc, bins=np.linspace(0, 1, 50), label='COSMIC', histtype='step')
#plt.hist(e_200, bins=np.linspace(0, 1, 50), label='CMC rv20', histtype='step')
#plt.hist(e_100, bins=np.linspace(0, 1, 50), label='CMC rv10', histtype='step')
#plt.hist(e_20, bins=np.linspace(0, 1, 50), label='CMC rv2', histtype='step')
#plt.legend()
#plt.title('Eccentricity of all binaries initially')
#plt.xlabel('Eccentricity')
#plt.savefig('init_e.png')
