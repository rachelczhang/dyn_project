import numpy as np
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp
import pandas as pd

data = np.genfromtxt('king.esc.dat')

total = 0
error = 0
for i in range(len(data)):
        # check if binary
        if i < 6:
        #if i == 10552:
        #if data[i,14] == 1 and data[i,22] >= 2.0 and data[i,22] < 10.0:
        #if data[i,14] == 1 and data[i,22] == 4.0:  
                total += 1
                print(i)
                single_binary = InitialBinaryTable.InitialBinaries(m1=data[i,15], m2=data[i,16], porb=data[i,26], ecc=data[i,20], tphysf=13700., kstar1=data[i,22], kstar2=data[i,23], metallicity=0.00017)
                BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
                bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)

                print('HELLO I AM THE id', data[i, 13])
                bpp.tphys = data[i,1]*151552.
                print('tphys', data[i,1]*151552.)
                bpp.mass_1 = data[i,15]
                bpp.mass_2 = data[i,16]
                bpp.kstar_1 = data[i,22]
                print('kstar1', data[i,22])
                bpp.kstar_2 = data[i,23]
                print('kstar2', data[i,23])
                bpp.sep = data[i,19]*1.5e11/6.95e8
                bpp.porb = data[i,26]
                bpp.ecc = data[i,20]
                bpp.RRLO_1 = data[i,41]
                bpp.RRLO_2 = data[i,42]
                bpp.evol_type = 1
                bpp.aj_1 = data[i,55]
                bpp.aj_2 = data[i,56]
                bpp.tms_1 = data[i,37]
                bpp.tms_2 = data[i,38]
                bpp.massc_1 = data[i,29]
                bpp.massc_2 = data[i,30]
                bpp.rad_1 = data[i,24]
                bpp.rad_2 = data[i,25]
                bpp.mass0_1 = data[i,53]
                print('mass0_1', bpp.mass0_1)
                bpp.mass0_2 = data[i,54]
                print('mass0_2', bpp.mass0_2)
                bpp.lum_1 = data[i,27]
                bpp.lum_2 = data[i,28]
                bpp.teff_1 = (data[i,27]*3.8e26/ (4.*np.pi*(data[i,24]*6.95e8)**2. * 5.67e-8))**(0.25)
                bpp.teff_2 = (data[i,28]*3.8e26/ (4.*np.pi*(data[i,25]*6.95e8)**2. * 5.67e-8))**(0.25)
                bpp.radc_1 = data[i,31]
                bpp.radc_2 = data[i,32]
                bpp.menv_1 = data[i,33]
                bpp.menv_2 = data[i,34]
                bpp.renv_1 = data[i,35]
                bpp.renv_2 = data[i,36]
                bpp.omega_spin_1 = data[i,43]
                bpp.omega_spin_2 = data[i,44]
                bpp.B_1 = data[i,45]
                bpp.B_2 = data[i,46]
                bpp.bacc_1 = data[i,49]
                bpp.bacc_2 = data[i,50]
                bpp.tacc_1 = data[i,51]
                bpp.tacc_2 = data[i,52]
                bpp.epoch_1 = data[i,55]
                bpp.epoch_2 = data[i,56]
                bpp.bhspin_1 = data[i,58]
                bpp.bhspin_2 = data[i,59]
                bpp.bin_num = 1
                #print('mass0', data[i,53])
                for column in bpp.columns:
                        initC = initC.assign(**{column:bpp.iloc[0][column]})  
                        #print(column,bpp.iloc[0][column])
                bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initC)
                bpp_mid = bpp_mid[['tphys', 'kstar_1', 'kstar_2', 'mass_1', 'mass_2', 'sep', 'evol_type']]
                print(bpp_mid)
                print('bpp_mid', bpp_mid.iloc[0]['kstar_1'])
                initC_mid.to_hdf('initC.h5', key='initC')
                
                initC_mid = initC_mid[['tphys','kstar_1', 'kstar_2', 'mass_1', 'mass_2', 'mass0_1', 'mass0_2', 'tphysf', 'epoch_1']]
                print('init', initC_mid)
                print(initC_mid['kstar_1'].iloc[0])
                if bpp_mid.iloc[0]['kstar_1'] < initC_mid['kstar_1'].iloc[0]:
                        error += 1
        print('ERROR COUNT', error)
        print('TOTAL', total)
#print('ERROR COUNT', error)
#print('TOTAL', total)
