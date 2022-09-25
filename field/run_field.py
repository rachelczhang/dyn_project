import numpy as np 
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import h5py
import pandas as pd 
import pickle

# read t=0 snapshot file from different rv's 
def read_snap(rv):
	snap = pd.read_hdf('../dynamics/rv%s/king.snapshots.h5' % (rv,), key='0(t=0)')
	return snap 

def a_to_p(a, m1, m2):
	mtot = m1+m2 # in solar masses
	period=(a**3/mtot)**(1/2) ##in years
	period=period*365 ##in days
	return period

snap = read_snap(2.0)

# read parameters
m1_list = snap['m0_MSUN']
m2_list = snap['m1_MSUN']
porb_list = []
for (i, j, k) in zip(snap['a_AU'], m1_list, m2_list):
	porb_list.append(a_to_p(i, j, k))

ecc_list = snap['e']
tphysf_list = [13700.0]*len(snap['e'])
kstar1_list = snap['bin_startype0']
kstar2_list = snap['bin_startype1']
met_list = [0.017]*len(snap['e'])

# put together grid of binaries
binary_grid = InitialBinaryTable.InitialBinaries(m1=m1_list, m2=m2_list, porb=porb_list, ecc=ecc_list, tphysf=tphysf_list, kstar1=kstar1_list, kstar2=kstar2_list, metallicity=met_list)

BSEDict = {'xi': 0.5, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.05, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 1, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': -2.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.5, 'ecsn_mlow' : 1.4, 'aic' : 1, 'ussn' : 1, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}

print('initial conditions set!')

bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=binary_grid, BSEDict=BSEDict)

print('evolution complete!')
bcm.to_hdf('bcm.h5', key='bcm', mode='w')
bpp.to_hdf('bpp.h5', key='bpp', mode='w')

#bpp_data = open('bpp_data', 'wb')
#pickle.dump(bpp, bpp_data)
#bcm_data = open('bcm_data', 'wb')
#pickle.dump(bcm, bcm_data)
#with open('bpp.txt', 'w') as bpp_file:
	#print(bpp, file=bpp_file)
	#bpp_file.close()

#with open ('bcm.txt', 'w') as bcm_file:
	#print(bcm, file=bcm_file)
	#bcm_file.close()

print('saved to files!')
