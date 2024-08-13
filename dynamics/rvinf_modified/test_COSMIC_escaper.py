import numpy as np 
from cosmic.sample.initialbinarytable import InitialBinaryTable
from cosmic.evolve import Evolve
import cmc_parser as cp

rv20mod_conv = cp.conversion_file('king.conv.sh')

def a_to_p(a, m1, m2):
        mtot = m1+m2 # in solar masses
        period=(a**3/mtot)**(1/2) ##in years
        period=period*365 ##in days
        return period

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
                        if int(x[14]) == 1 and (float(x[22]) == 4.0):
                        #if int(x[14]) == 1 and float(x[22]) != 0.0 and float(x[22]) != 1.0 and float(x[23]) != 1.0 and float(x[23]) != 14.0 and float(x[23]) != 4.0 and float(x[23]) != 7.0:
                                m0.append(float(x[15]))
                                m1.append(float(x[16]))
                                a = float(x[19])
                                p.append(a_to_p(a, float(x[15]), float(x[16])))
                                e.append(float(x[20]))
                                kstar1.append(float(x[22]))
                                kstar2.append(float(x[23]))
                                t_pre = float(x[1])
                                t_pre = t_pre*rv20mod_conv.time_myr
                                #t.append(5100.4359-t_pre)
                                t.append(13700-t_pre)
                                print(m0, m1, a, p, e, kstar1, kstar2, t_pre)
                                break
        return m0, m1, p, e, kstar1, kstar2, t

#single_binary = InitialBinaryTable.InitialBinaries(m1=2.0, m2=0.5, porb=446.795757, ecc=0.448872, tphysf=13700.0, kstar1=10, kstar2=0, metallicity=0.002)

m0, m1, p, e, kstar1, kstar2, t = read_binary_escapers()

mid = 3.259268



print('t to put into COSMIC', t)

binary_set = InitialBinaryTable.InitialBinaries(m1=m0, m2=m1, porb=p, ecc=e, tphysf=t, kstar1=kstar1, kstar2=kstar2, metallicity=[0.017]*len(m0))

BSEDict = {'xi': 0.5, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 1, 'alpha1': 1.0, 'pts1': 0.05, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 0.5, 'ck': 1000, 'bwind': 0.0, 'lambdaf': 0.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'grflag' : 1, 'remnantflag': 4, 'ceflag': 1, 'eddfac': 1.0, 'ifflag': 0, 'bconst': 3000, 'sigma': 265.0, 'gamma': -2.0, 'pisn': -2.0, 'natal_kick_array' : [[-100.0,-100.0,-100.0,-100.0,0.0], [-100.0,-100.0,-100.0,-100.0,0.0]], 'bhsigmafrac' : 1.0, 'polar_kick_angle' : 90, 'qcrit_array' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], 'cekickflag' : 2, 'cehestarflag' : 0, 'cemergeflag' : 0, 'ecsn' : 2.5, 'ecsn_mlow' : 1.4, 'aic' : 1, 'ussn' : 1, 'sigmadiv' :-20.0, 'qcflag' : 1, 'eddlimflag' : 0, 'fprimc_array' : [2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0,2.0/21.0], 'bhspinflag' : 0, 'bhspinmag' : 0.0, 'rejuv_fac' : 1.0, 'rejuvflag' : 0, 'htpmb' : 1, 'ST_cr' : 1, 'ST_tide' : 1, 'bdecayfac' : 1, 'rembar_massloss' : 0.5, 'kickflag' : 0, 'zsun' : 0.014, 'bhms_coll_flag' : 0, 'don_lim' : -1, 'acc_lim' : -1}

# fig 2 
bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=binary_set, BSEDict=BSEDict)
print("binary set 1", bpp['tphys'], bpp['kstar_1'], bpp['kstar_2'], bpp['mass_1'], bpp['mass_2'], bpp['evol_type'], bpp['sep'], bpp['ecc'])

print(initC['tphys'], initC['kstar_1'])

for column in bpp.columns:
       initC = initC.assign(**{column:bpp.iloc[5][column]})
       print(initC['tphys'], initC['kstar_1'])
bppmid, bcmmid, initCmid, kickinfo = Evolve.evolve(initialbinarytable=initC)
print(bppmid['tphys'], bppmid['kstar_1'], bppmid['kstar_2'], bppmid['mass_1'], bppmid['mass_2'], bppmid['evol_type'], bppmid['sep'], bppmid['ecc'])


binary_set2 = InitialBinaryTable.InitialBinaries(m1=m0, m2=m1, porb=p, ecc=e, tphysf=[t[0]-mid], kstar1=kstar1, kstar2=kstar2, metallicity=[0.017]*len(m0))

 
bpp, bcm, initC, kick_info = Evolve.evolve(initialbinarytable=binary_set2, BSEDict=BSEDict)
print("binary set 2", bpp['tphys'], bpp['kstar_1'], bpp['kstar_2'], bpp['mass_1'], bpp['mass_2'], bpp['evol_type'], bpp['sep'], bpp['ecc'])



#print(bcm)
#bpp.to_hdf('bpp_singlebinary.h5', key='bpp', mode='w')

