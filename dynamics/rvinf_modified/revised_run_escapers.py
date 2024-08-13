import numpy as np
import pandas as pd
import cosmic
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp

data = np.genfromtxt('king.esc.dat')
rv20mod_conv = cp.conversion_file('king.conv.sh')

print('len data', len(data))
for i in range(len(data)):
        print('i', i)
        # if i == 4 or i == 43:
        #         continue
        print('HELLO I AM THE ID', data[i, 13])
        print('m1', data[i,15])
        print('m2', data[i,16])
        print('kstar1', data[i,22])
        print('kstar2', data[i,23])
        print('porb', data[i,26])
        print('ecc', data[i,20])
        single_binary = InitialBinaryTable.InitialBinaries(m1=data[i,15], m2=data[i,16], porb=data[i,26], ecc=data[i,20], tphysf=13700.-(data[i,1]*151552.), kstar1=data[i,22], kstar2=data[i,23], metallicity=0.00017)
        print('single binary', single_binary)
        BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
        bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)
        #print('bpp1', bpp)
        bpp.tphys = bpp.tphys+(data[i,1]*151552.)
        #bpp.iloc[0].tphys = bpp.tphys+(data[i,1]*151552.)
        #print('bpp2', bpp)
        #print('tphys', data[i,1]*151552.)
        bpp.mass_1 = data[i,15]
        bpp.mass_2 = data[i,16]
        bpp.kstar_1 = data[i,22]
        #print('kstar1', data[i,22])
        bpp.kstar_2 = data[i,23]
        #print('kstar2', data[i,23])
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
        bpp.mass0_2 = data[i,54]
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
        for column in bpp.columns:
                initC = initC.assign(**{column:bpp.iloc[0][column]})
        print('bpp', bpp)
        print('initC', initC)
        bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initC)
        #initialBinaryTable2 = InitialBinaryTable.InitialBinaries(m1=initC.mass_1, m2=initC.mass_2, porb=initC.porb, ecc=initC.ecc, tphysf=13700.-(data[i,1]*151552.), kstar1=initC.kstar_1, kstar2=initC.kstar_2, metallicity=0.00017)
        #bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initialBinaryTable2, BSEDict=BSEDict)
        print('bpp mid', bpp_mid)
        print('len index', bpp_mid.index)
        bpp_mid.set_index(pd.Series([data[i,13]]*len(bpp_mid.index)), inplace=True)
        print('bpp mid2', bpp_mid)
        if i == 0:
                initC_mid.to_hdf('initC_esc.h5', key='initC', format='table')
                bpp_mid.to_hdf('bpp_esc.h5', key='bpp', format='table')
                bcm_mid.to_hdf('bcm_esc.h5', key='bcm', format='table')
        else:
                initC_mid.to_hdf('initC_esc.h5', 'initC', format='table', append=True)
                bpp_mid.to_hdf('bpp_esc.h5', 'bpp',  format='table', append=True)
                bcm_mid.to_hdf('bcm_esc.h5', 'bcm', format='table', append=True)

#def read_single_escapers():
#        m = []
#        kstar = []
#        t = []
#        with open('king.esc.dat', 'r') as g:
#                next(g)
#                for line in g:
#                        x = line.split(' ')
#                        if int(x[14]) == 0:
#                                m.append(float(x[2]))
#                                kstar.append(float(x[21]))
#                                t_pre = float(x[1])
#                                t_pre = t_pre*rv20mod_conv.time_myr
#                                t.append(5100.4359-t_pre)


