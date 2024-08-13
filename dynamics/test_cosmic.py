import numpy as np
import pandas as pd 
import cosmic
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp

# conversion
rv20mod_conv = cp.conversion_file('rv2.0_modified/king.conv.sh')

###### get ZAMS properties ######
cmc_20 = pd.read_hdf('rv2.0_modified/king.snapshots.h5', key='0(t=0)')

id0_20 = cmc_20['id0']
id1_20 = cmc_20['id1']
m0_20 = cmc_20['m0_MSUN']
m1_20 = cmc_20['m1_MSUN']
a_20 = cmc_20['a_AU']
e_20 = cmc_20['e']
kstar0_20 = cmc_20['bin_startype0']
kstar1_20 = cmc_20['bin_startype1']

def a_to_p(a, m1, m2):
        mtot = m1+m2 # in solar masses
        period=(a**3/mtot)**(1/2) ##in years
        period=period*365 ##in days
        return period
p_20 = a_to_p(a_20, m0_20, m1_20)

# get binary properties for a particular ID-ID
def get_binary(id0, id1):
	for i in range(len(id0_20)):
		if id0_20.iloc[i] == id0:
			index0 = i
		if id1_20.iloc[i] == id1:
			index1 = i
	m0_zams = m0_20.iloc[index0]
	m1_zams = m1_20.iloc[index1]
	p = p_20.iloc[index0]
	e = e_20.iloc[index0]
	kstar1 = kstar0_20.iloc[index0]
	kstar2 = kstar1_20.iloc[index0]
	print('m0', m0_zams, 'm1', m1_zams, 'p', p, 'e', e, 'kstar1', kstar1, 'kstar2', kstar2)
	return m0_zams, m1_zams, p, e, kstar1, kstar2

###### run COSMIC on binary starting at ZAMS ######
def run_cosmic_zams(id0, id1):
	m0_zams, m1_zams, p, e, kstar1, kstar2 = get_binary(id0, id1)
	single_binary = InitialBinaryTable.InitialBinaries(m1=m0_zams, m2=m1_zams, porb=p, ecc=e, tphysf=13700.0, kstar1=kstar1, kstar2=kstar2, metallicity=0.002)
	BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
	bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)
	print('ZAMS bpp', bpp)
	print(bpp['tphys'], bpp['mass_1'], bpp['kstar_1'], bpp['mass_2'], bpp['kstar_2'], bpp['sep'], bpp['porb'], bpp['ecc'], bpp['evol_type'])
	return bpp, bcm, initC, kick_info

###### run COSMIC from middle of evolution of ZAMS case ######
def run_cosmic_middle():
	single_binary = InitialBinaryTable.InitialBinaries(m1=14.850948, m2=38.134630, porb=7810.442249, ecc=0.009437, tphysf=13700.0-5.357126, kstar1=14.0, kstar2=1.0, metallicity=0.002)
	BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
	bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)
	print('middle bpp', bpp)
	print(bpp['tphys'], bpp['mass_1'], bpp['kstar_1'], bpp['mass_2'], bpp['kstar_2'], bpp['sep'], bpp['porb'], bpp['ecc'], bpp['evol_type'])
	return bpp, bcm, initC, kick_inf

###### run COSMIC right at escaper values ######

def read_binary(id0, id1):
	with open('rv2.0_modified/kingres1.esc.dat', 'r') as f:
		count = 0
		for line in f:
			x = line.split(' ')
			if float(x[15]) > 5 and float(x[16]) > 5:
				print('BIG', float(x[17]), float(x[18]))
			if float(x[17]) == id0 and float(x[18]) == id1:
				m0 = float(x[15])
				m1 = float(x[16])
				a = float(x[19])
				p = a_to_p(a, m0, m1)
				e = float(x[20])
				kstar1 = float(x[22])
				kstar2 = float(x[23])
				t = float(x[1])
				break
			count += 1
	print('count', count)
	print('esc', m0, m1, p, e, kstar1, kstar2, t)
	return m0, m1, p, e, kstar1, kstar2, t
	
def run_cosmic_escape(id0, id1):
	m0, m1, p, e, kstar1, kstar2, t_pre = read_binary(id0, id1)
	t = t_pre*rv20mod_conv.time_myr
	print('t', t, 'evol time', 13700.0-t)
	single_binary = InitialBinaryTable.InitialBinaries(m1=m0, m2=m1, porb=p, ecc=e, tphysf=13700.0-t, kstar1=kstar1, kstar2=kstar2, metallicity=0.002)
	BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
	bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)
	print('esc bpp', bpp)
	print(bpp['tphys'], bpp['mass_1'], bpp['kstar_1'], bpp['mass_2'], bpp['kstar_2'], bpp['sep'], bpp['porb'], bpp['ecc'], bpp['evol_type']) 
	return bpp, bcm, initC, kick_info

id0 = 871032 #152029 #489072 #850017 # 319064 #320500
id1 = 1659139 #2115663 #862688 #1850017 #1319064 #1320500
#print(get_binary(id0, id1))
#print(read_binary(id0, id1))
run_cosmic_zams(id0, id1)
run_cosmic_middle()
#run_cosmic_escape(id0, id1)
