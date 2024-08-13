import numpy as np
import pandas as pd
import cosmic
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve

def a_to_p(a, m1, m2):
        mtot = m1+m2 # in solar masses
        period=(a**3/mtot)**(1/2) ##in years
        period=period*365 ##in days
        return period

def read_id_from_snapshot(id_num):
        cmc = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rvinf_modified/king.window.snapshots.h5', key='1(t=0.10490715Gyr)')
        row = cmc.loc[cmc['id']==id_num] 
        print('row', row)
        m0 = row['m0_MSUN']
        print('m0', m0)
        m1 = row['m1_MSUN']
        p = a_to_p(row['a_AU'], m0, m1)
        print('p', p)
        e = row['e']
        kstar1 = row['bin_startype0']
        kstar2 = row['bin_startype1']
        print('kstar1', kstar1)
        t = 13700.0
        return m0, m1, p, e, kstar1, kstar2, t 

def run_cosmic():
        m0, m1, p, e, kstar1, kstar2, t = read_id_from_snapshot(930654)
        binary_set = InitialBinaryTable.InitialBinaries(m1=m0, m2=m1, porb=p, ecc=e, tphysf=t, kstar1=kstar1, kstar2=kstar2, metallicity=[0.017]*len(m0))
        BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
        bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=binary_set, BSEDict=BSEDict)
        print(bpp[['tphys', 'kstar_1', 'kstar_2', 'mass_1', 'mass_2', 'sep', 'evol_type']])
        return bpp

run_cosmic()
