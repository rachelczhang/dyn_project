import numpy as np
import pandas as pd
import cosmic
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp

# read data from the escape file
data = np.genfromtxt('../rv2.0_modified/kingres1.esc.dat')
rv20mod_conv = cp.conversion_file('../rv2.0_modified/king.conv.sh')

# looking into the frozen binaries; frozen at i = 4, 43, and 136
i = 9001
# # print the parameters of the frozen binaries 
# single_binary = InitialBinaryTable.InitialBinaries(m1=data[i,15], m2=data[i,16], porb=data[i,26], ecc=data[i,20], tphysf=13700.0-(data[i,1]*rv20mod_conv.time_myr), kstar1=data[i,22], kstar2=data[i,23], metallicity=0.00017)
# print('m1', data[i,15])
# print('m2', data[i,16])
# print('porb', data[i,26])
# print('ecc', data[i,20])
# print('tphys', data[i,1]*rv20mod_conv.time_myr)
# print('tphysf', 13700.0-(data[i,1]*rv20mod_conv.time_myr))
# print('kstar1', data[i,22])
# print('kstar2', data[i,23])

# # manually entering the parameters of the frozen binaries

# # for i = 4
# # single_binary = InitialBinaryTable.InitialBinaries(m1=1.4956561, m2=0.50638494, porb=7.03609, ecc=0.52764865, tphysf=13699.863204509122, kstar1=1, kstar2=0, metallicity=0.00017)

# # for i = 43
# # single_binary = InitialBinaryTable.InitialBinaries(m1=1.251485, m2=0.88989959, porb=24.34, ecc=0.88480177, tphysf=13699.863204509122, kstar1=1, kstar2=1, metallicity=0.00017)

# # for i = 136
# #single_binary = InitialBinaryTable.InitialBinaries(m1=1.0817482, m2=0.9454433, porb=1.73458, ecc=0.40755512, tphysf=13699.863204509122, kstar1=1, kstar2=1, metallicity=0.00017)


# pd.set_option('display.max_columns', 500)

# pd.set_option('max_colwidth', 800)

# # single_binary = InitialBinaryTable.InitialBinaries(m1=25.543645, m2=20.99784, porb=446.795757, ecc=0.448872, tphysf=13700.0, kstar1=1, kstar2=1, metallicity=0.002)

# BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'remnantflag': 3, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.5, 'ecsn_mlow' : 1.4, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 0, 'bdecayfac' : 1, 'randomseed' : -1235453, 'grflag' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014,  'grflag' : 1, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}
BSEDict = {'xi': 1.0, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.001, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 0, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': 45.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.25, 'ecsn_mlow' : 1.6, 'aic' : 1, 'ussn' : 0, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}

# bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)
# print('bpp1', bpp[['tphys', 'mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'porb', 'evol_type']])
# # print('evolved ', i)
# bpp.tphys = data[i,1]*rv20mod_conv.time_myr
# bpp.mass_1 = data[i,15]
# bpp.mass_2 = data[i,16]
# bpp.kstar_1 = data[i,22]
# bpp.kstar_2 = data[i,23]
# bpp.sep = data[i,19]*215.032 # convert to solar radius
# bpp.porb = data[i,26]
# bpp.ecc = data[i,20]
# bpp.RRLO_1 = data[i,41]
# bpp.RRLO_2 = data[i,42]
# bpp.evol_type = 1
# bpp.aj_1 = data[i,55]
# bpp.aj_2 = data[i,56]
# bpp.tms_1 = data[i,37]
# bpp.tms_2 = data[i,38]
# bpp.massc_1 = data[i,29]
# bpp.massc_2 = data[i,30]
# bpp.rad_1 = data[i,24]
# bpp.rad_2 = data[i,25]
# bpp.mass0_1 = data[i,53]
# bpp.mass0_2 = data[i,54]
# bpp.lum_1 = data[i,27]
# bpp.lum_2 = data[i,28]
# bpp.teff_1 = (data[i,27]*3.8e26/ (4.*np.pi*(data[i,24]*6.95e8)**2. * 5.67e-8))**(0.25)
# bpp.teff_2 = (data[i,28]*3.8e26/ (4.*np.pi*(data[i,25]*6.95e8)**2. * 5.67e-8))**(0.25)
# bpp.radc_1 = data[i,31]
# bpp.radc_2 = data[i,32]
# bpp.menv_1 = data[i,33]
# bpp.menv_2 = data[i,34]
# bpp.renv_1 = data[i,35]
# bpp.renv_2 = data[i,36]
# bpp.omega_spin_1 = data[i,43]
# bpp.omega_spin_2 = data[i,44]
# bpp.B_1 = data[i,45]
# bpp.B_2 = data[i,46]
# bpp.bacc_1 = data[i,49]
# bpp.bacc_2 = data[i,50]
# bpp.tacc_1 = data[i,51]
# bpp.tacc_2 = data[i,52]
# bpp.epoch_1 = data[i,55]
# bpp.epoch_2 = data[i,56]
# bpp.bhspin_1 = data[i,58]
# bpp.bhspin_2 = data[i,59]
# bpp.bin_num = 1
# print('bpp2 ', bpp[['tphys', 'mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'porb', 'evol_type']])
# #print ("bpp", bpp)
# for column in bpp.columns:
#         initC = initC.assign(**{column:bpp.iloc[0][column]})
# # print('made it to evolve2')
# # print('m1', initC.mass_1)
# # print('m2', initC.mass_2)
# # print('porb', initC.porb)
# # print('ecc', initC.ecc)
# # print('kstar1', initC.kstar_1)
# # print('kstar2', initC.kstar_2)
# # print('initC columns', initC.columns)

# #initialBinaryTable2 = InitialBinaryTable.InitialBinaries(m1=initC.mass_1, m2=initC.mass_2, porb=initC.porb, ecc=initC.ecc, tphysf=13699.863204509122, kstar1=initC.kstar_1, kstar2=initC.kstar_2, metallicity=0.00017)        

# #print ("PING", i, "\n", initialBinaryTable2)

# # bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initialBinaryTable2, BSEDict=BSEDict)
# bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initC)
# print("Started in middle at Index {0}".format(0))
# print('bpp mid', bpp_mid)


single_binary = InitialBinaryTable.InitialBinaries(m1=data[i,15], m2=data[i,16], porb=data[i,26], ecc=data[i,20], tphysf=13700.-(data[i,1]*rv20mod_conv.time_myr), kstar1=data[i,22], kstar2=data[i,23], metallicity=0.00017)
bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=single_binary, BSEDict=BSEDict)
print('bpp1', bpp[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'evol_type']])
# bpp.tphys = bpp.tphys+(data[i,1]*rv20mod_conv.time_myr)
bpp.tphys = data[i,1]*rv20mod_conv.time_myr
bpp.mass_1 = data[i,15]
bpp.mass_2 = data[i,16]
bpp.kstar_1 = data[i,22]
bpp.kstar_2 = data[i,23]
bpp.sep = data[i,19]*215.032 # convert to solar radius
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
print('bpp2', bpp[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'evol_type']])

print('initC', initC)
bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initC)
print('bpp mid', bpp_mid)
#initialBinaryTable2 = InitialBinaryTable.InitialBinaries(m1=initC.mass_1, m2=initC.mass_2, porb=initC.porb, ecc=initC.ecc, tphysf=13700.-(data[i,1]*151552.), kstar1=initC.kstar_1, kstar2=initC.kstar_2, metallicity=0.00017)
#bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initialBinaryTable2, BSEDict=BSEDict)
bcm_mid.set_index(pd.Series([int(data[i,17])]*len(bcm_mid.index)), inplace=True)
bpp_mid.set_index(pd.Series([int(data[i,17])]*len(bpp_mid.index)), inplace=True)
print('bpp mid2', bpp_mid[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'evol_type']])
print('bcm', bcm_mid[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep']])
