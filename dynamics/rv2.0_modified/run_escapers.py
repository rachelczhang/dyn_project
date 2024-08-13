import numpy as np
import pandas as pd
import cosmic
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp

rv20mod_conv = cp.conversion_file('king.conv.sh')

def a_to_p(a, m1, m2):
	mtot = m1+m2 # in solar masses
	period=(a**3/mtot)**(1/2) ##in years
	period=period*365 ##in days
	return period

def read_single_escapers():
	m = []
	kstar = []
	t = []
	with open('king.esc.dat', 'r') as g:
		next(g)
		for line in g:
			x = line.split(' ')
			if int(x[14]) == 0:
				m.append(float(x[2]))
				kstar.append(float(x[21])) 
				t_pre = float(x[1])
				t_pre = t_pre*rv20mod_conv.time_myr
				t.append(13800.0-t_pre)
	with open('kingres1.esc.dat', 'r') as f:
		for line in f:
			x = line.split(' ')
			if int(x[14]) == 0:
				m.append(float(x[2]))
				kstar.append(float(x[21]))
				t_pre = float(x[1])
				t_pre = t_pre*rv20mod_conv.time_myr
				t.append(13800.0-t_pre)	
	return m, kstar, t	

def read_binary_escapers():
	m0 = []
	m1 = []
	p = []
	e = []
	kstar1 = []
	kstar2 = []
	t = []
	with open('king.esc.dat', 'r') as g:
		next(g)
		for line in g:
			x = line.split(' ')
			if int(x[14]) == 1:
				m0.append(float(x[15]))
				m1.append(float(x[16]))
				a = float(x[19])
				p.append(a_to_p(a, float(x[15]), float(x[16])))
				e.append(float(x[20]))
				kstar1.append(float(x[22]))
				kstar2.append(float(x[23]))
				t_pre = float(x[1])
				t_pre = t_pre*rv20mod_conv.time_myr
				t.append(13800.0-t_pre)
	with open('kingres1.esc.dat', 'r') as f:
		for line in f:
			x = line.split(' ')
			if int(x[14]) == 1:
				m0.append(float(x[15]))
				m1.append(float(x[16]))
				a = float(x[19])
				p.append(a_to_p(a, float(x[15]), float(x[16])))
				e.append(float(x[20]))
				kstar1.append(float(x[22]))
				kstar2.append(float(x[23]))
				t_pre = float(x[1])
				t_pre = t_pre*rv20mod_conv.time_myr
				t.append(13800.0-t_pre)
	return m0, m1, p, e, kstar1, kstar2, t

def print_counts():
	kstar = read_single_escapers()[1]
	kstar1 = read_binary_escapers()[4]
	kstar2 = read_binary_escapers()[5]
	print('Total singles: ', len(kstar))
	print('BH singles: ', kstar.count(14.0))
	print('NS singles: ', kstar.count(13.0))
	print('WD singles: ', kstar.count(10.0)+kstar.count(11.0)+kstar.count(12.0))
	print('Other singles: ', len(kstar)-kstar.count(14.0)-kstar.count(13.0)-kstar.count(12.0)-kstar.count(11.0)-kstar.count(10.0))
	print('Total binaries: ', len(kstar1))
	BH_binaries = 0
	NS_binaries = 0
	WD_binaries = 0
	for i in range(len(kstar1)):
		if kstar1[i] == 14.0  or kstar2[i] == 14.0:
			BH_binaries += 1
		if (kstar1[i] == 13.0 or kstar2[i] == 13.0) and (kstar1[i] <= 13.0 and kstar2[i] <= 13.0):
			NS_binaries += 1
	print('BH binaries: ', BH_binaries)
	print('NS binaries: ', NS_binaries)

def run_SSE():
	m, kstar, t = read_single_escapers()
	m2 = [0]*len(m)
	porb = [0]*len(m)
	ecc = [0]*len(m)
	kstar2 = [15]*len(m)
	met = [0.017]*len(m)
	single = InitialBinaryTable.InitialBinaries(m1=m, m2=m2, porb=porb, ecc=ecc, tphysf=t, kstar1=kstar, kstar2=kstar2, metallicity=met)
	BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
	bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single, BSEDict=BSEDict)
	bpp.to_hdf('bpp_singles.h5', key='bpp', mode='w')
	bcm.to_hdf('bcm_singles.h5', key='bcm', mode='w')


def run_cosmic():
	m0, m1, p, e, kstar1, kstar2, t = read_binary_escapers()
	binary_set = InitialBinaryTable.InitialBinaries(m1=m0, m2=m1, porb=p, ecc=e, tphysf=t, kstar1=kstar1, kstar2=kstar2, metallicity=[0.017]*len(m0))
	BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
	bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=binary_set, BSEDict=BSEDict)
	print('esc bpp', bpp)	
	bcm.to_hdf('bcm.h5', key='bcm', mode='w')
	bpp.to_hdf('bpp.h5', key='bpp', mode='w')
	return bpp, bcm, initC, kick_info
			
#run_cosmic()
#print_counts()
run_SSE()
