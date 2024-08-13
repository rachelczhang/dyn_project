import numpy as np 
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp
import pandas as pd

rv20mod_conv = cp.conversion_file('king.conv.sh')
pd.set_option('display.max_columns', 500)

pd.set_option('max_colwidth', 800)

def a_to_p(a, m1, m2):
        mtot = m1+m2 # in solar masses
        period=(a**3/mtot)**(1/2) ##in years
        period=period*365 ##in days
        return period

def read_binary_escapers():
        m0 = []
        m1 = []
        p = []
        a = []
        e = []
        kstar1 = []
        kstar2 = []
        t = []
        radrol0 = []
        radrol1 = []
        tms0 = []
        tms1 = []
        massc0 = []
        massc1 = []
        rad0 = []
        rad1 = []
        mass0_0 = []
        mass0_1 = []
        lum0 = []
        lum1 = []
        radc0 = []
        radc1 = []
        menv0 = []
        menv1 = []
        renv0 = []
        renv1 = []
        ospin0 = []
        ospin1 = []
        B0 = []
        B1 = []
        bacc0 = []
        bacc1 = []
        tacc0 = []
        tacc1 = []
        epoch0 = []
        epoch1 = []
        bhspin = []
        bhspin1 = []
        with open('king.esc.dat', 'r') as g:
                next(g)
                for line in g:
                        x = line.split(' ')
                        if int(x[14]) == 1 and (float(x[22]) == 4.0):
                        #if int(x[14]) == 1 and float(x[22]) != 0.0 and float(x[22]) != 1.0 and float(x[23]) != 1.0 and float(x[23]) != 14.0 and float(x[23]) != 4.0 and float(x[23]) != 7.0:
                                m0.append(float(x[15]))
                                m1.append(float(x[16]))
                                a.append(float(x[19]))
                                p.append(float(x[26]))
                                #p.append(a_to_p(a, float(x[15]), float(x[16])))
                                e.append(float(x[20]))
                                kstar1.append(float(x[22]))
                                kstar2.append(float(x[23]))
                                t_pre = float(x[1])
                                t_pre = t_pre*rv20mod_conv.time_myr
                                t.append(t_pre)
                                #t.append(13700-t_pre)
                                radrol0.append(float(x[41]))
                                radrol1.append(float(x[42]))
                                tms0.append(float(x[37]))
                                tms1.append(float(x[38]))
                                massc0.append(float(x[29]))
                                massc1.append(float(x[30]))
                                rad0.append(float(x[24]))
                                rad1.append(float(x[25]))
                                mass0_0.append(float(x[53]))
                                mass0_1.append(float(x[54]))
                                lum0.append(float(x[27]))
                                lum1.append(float(x[28]))
                                radc0.append(float(x[31]))
                                radc1.append(float(x[32]))
                                menv0.append(float(x[33]))
                                menv1.append(float(x[34]))
                                renv0.append(float(x[35]))
                                renv1.append(float(x[36]))
                                ospin0.append(float(x[43]))
                                ospin1.append(float(x[44]))
                                B0.append(float(x[45]))
                                B1.append(float(x[46]))
                                bacc0.append(float(x[49]))
                                bacc1.append(float(x[50]))
                                tacc0.append(float(x[51]))
                                tacc1.append(float(x[52]))
                                epoch0.append(float(x[55]))
                                epoch1.append(float(x[56]))
                                if x[57] != 'na': 
                                        bhspin.append(float(x[57]))
                                else:
                                        bhspin.append(0)
                                bhspin1.append(float(x[58]))
                                print(m0, m1, a, p, e, kstar1, kstar2, t_pre)
                                break
        return m0, m1, a, p, e, kstar1, kstar2, t, radrol0, radrol1, tms0, tms1, massc0, massc1, rad0, rad1, mass0_0, mass0_1, lum0, lum1, radc0, radc1, menv0, menv1, renv0, renv1, ospin0, ospin1, B0, B1, bacc0, bacc1, tacc0, tacc1, epoch0, epoch1, bhspin, bhspin1

def get_teff(R, L):
        T = (L/R**2)**(1/4) #solar temperatures
        return T * 5800 # K

m0, m1, a, p, e, kstar1, kstar2, t, radrol0, radrol1, tms0, tms1, massc0, massc1, rad0, rad1, mass0_0, mass0_1, lum0, lum1, radc0, radc1, menv0, menv1, renv0, renv1, ospin0, ospin1, B0, B1, bacc0, bacc1, tacc0, tacc1, epoch0, epoch1, bhspin, bhspin1 = read_binary_escapers()

binary_set = InitialBinaryTable.InitialBinaries(m1=m0, m2=m1, porb=p, ecc=e, tphysf=t, kstar1=kstar1, kstar2=kstar2, metallicity=[0.017]*len(m0))

print (binary_set)

BSEDict = {'xi': 0.5, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.05, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 1, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': -2.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.5, 'ecsn_mlow' : 1.4, 'aic' : 1, 'ussn' : 1, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}

bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=binary_set, BSEDict=BSEDict)

print(t[0])
print( bpp)
bpp.tphys = t[0]
bpp.mass_1 = m0[0]
bpp.mass_2 = m1[0]
bpp.kstar_1 = kstar1[0] 
bpp.kstar_2 = kstar2[0] 
bpp.sep = a[0]*215.032 
bpp.porb = p[0] 
bpp.ecc = e[0] 
bpp.RRLO_1 = radrol0[0]
bpp.RRLO_2 = radrol1[0]
bpp.evol_type = 1.0
bpp.aj_1 = 0.0
bpp.aj_2 = 0.0
bpp.tms_1 = tms0[0]
bpp.tms_2 = tms1[0]
bpp.massc_1 = massc0[0]
bpp.massc_2 = massc1[0]
bpp.rad_1 = rad0[0]
bpp.rad_2 = rad1[0]
bpp.mass0_1 = mass0_0[0]
bpp.mass0_2 = mass0_1[0]
bpp.lum_1 = lum0[0]
bpp.lum_2 = lum1[0]
bpp.teff_1 = get_teff(rad0[0], lum0[0])
bpp.teff_2 = get_teff(rad1[0], lum1[0])
bpp.radc_1 = radc0[0]
bpp.radc_2 = radc1[0]
bpp.menv_1 = menv0[0]
bpp.menv_2 = menv1[0]
bpp.renv_1 = renv0[0]
bpp.renv_2 = renv1[0]
bpp.omega_spin_1 = ospin0[0]
bpp.omega_spin_2 = ospin1[0]
bpp.B_1 = B0[0]
bpp.B_2 = B1[0]
bpp.bacc_1 = bacc0[0]
bpp.bacc_2 = bacc1[0]
bpp.tacc_1 = tacc0[0]
bpp.tacc_2 = tacc1[0]
bpp.epoch_1 = epoch0[0]
bpp.epoch_2 = epoch1[0]
bpp.bhspin_1 = bhspin[0]
bpp.bhspin_2 = bhspin1[0]
bpp.bin_num = 0.0
print ("bpp after",bpp)

for column in bpp.columns:
        initC = initC.assign(**{column:bpp.iloc[0][column]})  
        print(column,bpp.iloc[0][column])
bpp_mid, bcm_mid, initC_mid, kick_info = Evolve.evolve(initialbinarytable=initC)
bpp_mid = bpp_mid[['tphys','mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep']]

print('bpp_mid', bpp_mid)
