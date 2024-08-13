import numpy as np
import pandas as pd
import cosmic
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp
import math 
import signal

#data = np.genfromtxt('king.esc.dat')
data = np.genfromtxt('kingres1.esc.dat')
rv20mod_conv = cp.conversion_file('king.conv.sh')

print('len data', len(data))

def handle_timeout(signum, frame):
        raise Exception("timeout")

singles_count = 0
binaries_run_count = 0
binaries_stuck_count = 0
binaries_other_errors_count = 0

BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
for i in range(len(data)):
        if math.isnan(data[i,22]):
                print('it is a single')
                print('i', i)
                print('id', data[i,13])
                print('tphys', data[i,1]*rv20mod_conv.time_myr)
                print('kstar', data[i,21])
                print('mass', data[i,2])
                singles_count += 1
                continue
        print('i', i)
        print('HELLO I AM THE ID', data[i, 17])
        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(5)

        try:
                condition = f'dtp=%f'% (13800.-(data[i,1]*rv20mod_conv.time_myr))
                single_binary = InitialBinaryTable.InitialBinaries(m1=data[i,15], m2=data[i,16], porb=data[i,26], ecc=data[i,20], tphysf=13800., kstar1=data[i,22], kstar2=data[i,23], metallicity=0.00017)
                # single_binary = InitialBinaryTable.InitialBinaries(m1=data[i,15], m2=data[i,16], porb=data[i,26], ecc=data[i,20], tphysf=13800.-(data[i,1]*rv20mod_conv.time_myr), kstar1=data[i,22], kstar2=data[i,23], metallicity=0.00017)
                bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict, timestep_conditions = [condition])
                # bpp.tphys = bpp.tphys+(data[i,1]*rv20mod_conv.time_myr)
                bpp.tphys = data[i,1]*rv20mod_conv.time_myr
                print('tphys', bpp.tphys)
                bpp.mass_1 = data[i,15]
                print('mass1', bpp.mass_1)
                bpp.mass_2 = data[i,16]
                print('mass2', bpp.mass_2)
                bpp.kstar_1 = data[i,22]
                print('kstar1', bpp.kstar_1)
                bpp.kstar_2 = data[i,23]
                print('kstar2', bpp.kstar_2)
                bpp.sep = data[i,19]*215.032 # convert to solar radius
                print('sep', bpp.sep)
                bpp.porb = data[i,26]
                print('porb', bpp.porb)
                bpp.ecc = data[i,20]
                print('ecc', bpp.ecc)
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
                bpp.bin_num = data[i,17]
                for column in bpp.columns:
                        initC = initC.assign(**{column:bpp.iloc[0][column]})
                print('bpp', bpp[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'evol_type']])

                bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initC, timestep_conditions = [condition])
                #initialBinaryTable2 = InitialBinaryTable.InitialBinaries(m1=initC.mass_1, m2=initC.mass_2, porb=initC.porb, ecc=initC.ecc, tphysf=13800.-(data[i,1]*151552.), kstar1=initC.kstar_1, kstar2=initC.kstar_2, metallicity=0.00017)
                #bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initialBinaryTable2, BSEDict=BSEDict)
                print('bpp mid', bpp_mid[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'evol_type']])
                bcm_mid.set_index(pd.Series([int(data[i,17])]*len(bcm_mid.index)), inplace=True)
                bpp_mid.set_index(pd.Series([int(data[i,17])]*len(bpp_mid.index)), inplace=True)
                print('bpp mid2', bpp_mid[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'evol_type']])
                print('bcm', bcm_mid[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep']])

                # for second escape file 
                initC_mid.to_hdf('initC_esc.h5', 'initC', format='table', append=True)
                bpp_mid.to_hdf('bpp_esc.h5', 'bpp',  format='table', append=True)
                bcm_mid.to_hdf('bcm_esc.h5', 'bcm', format='table', append=True)

                # for first escape file
                #if i == 0:
                #        initC_mid.to_hdf('initC_esc.h5', key='initC', format='table')
                #        bpp_mid.to_hdf('bpp_esc.h5', key='bpp', format='table')
                #        bcm_mid.to_hdf('bcm_esc.h5', key='bcm', format='table')
                #else:
                #        initC_mid.to_hdf('initC_esc.h5', 'initC', format='table', append=True)
                #        bpp_mid.to_hdf('bpp_esc.h5', 'bpp',  format='table', append=True)
                #        bcm_mid.to_hdf('bcm_esc.h5', 'bcm', format='table', append=True)
                binaries_run_count += 1
        except Exception as exc:
                if (exc.args[0] == "timeout"):
                        print("took too long, continuing after index", i)
                        print('tphys', data[i,1]*rv20mod_conv.time_myr)
                        print('mass1', data[i,15])
                        print('mass2', data[i,16])
                        print('kstar1', data[i,22])
                        print('kstar2', data[i,23])
                        print('porb', data[i,26])
                        print('ecc', data[i,20])
                        binaries_stuck_count += 1
                        continue
                else:
                        print("A non timeout error occurred")
                        print('tphys', data[i,1]*rv20mod_conv.time_myr)
                        print('mass1', data[i,15])
                        print('mass2', data[i,16])
                        print('kstar1', data[i,22])
                        print('kstar2', data[i,23])
                        print('porb', data[i,26])
                        print('ecc', data[i,20])
                        binaries_other_errors_count += 1
                        continue
print('singles count', singles_count)
print('binaries run count', binaries_run_count)
print('binaries stuck count', binaries_stuck_count)
print('binaries other errors count', binaries_other_errors_count)

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


