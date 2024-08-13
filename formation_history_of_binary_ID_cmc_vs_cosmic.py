import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

cmc20_init = pd.read_hdf('dynamics/rv2.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
cmc20_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700022Gyr)')
cosmic_data = pd.read_hdf('field/bcm.h5', 'bcm')
cosmic_present = cosmic_data[cosmic_data['tphys'] == 13700.0]
cosmic_init = cosmic_data[cosmic_data['tphys'] == 0.000000]

cmc_binaries_greater_1 = [661481.0, 363396.0, 903140.0, 188952.0, 489455.0, 352402.0, 448977.0, 874562.0, 409023.0, 407968.0, 64829.0, 835494.0, 910883.0, 613028.0, 733483.0, 609833.0, 939813.0, 848242.0, 673445.0, 308328.0, 777022.0, 953426.0, 840785.0, 325876.0, 684468.0, 375400.0, 813952.0, 375082.0, 211627.0, 811660.0, 187153.0, 483403.0, 99042.0, 948522.0, 835102.0, 727795.0, 885529.0, 626047.0, 531081.0, 846168.0, 978869.0, 940405.0, 30950.0, 468554.0, 760377.0, 581545.0, 969352.0, 828775.0, 820036.0, 546866.0, 73100.0, 924645.0, 285323.0, 899703.0, 72498.0, 142287.0, 649585.0, 949799.0, 232240.0, 581231.0, 812218.0, 796851.0, 385058.0, 231179.0, 119698.0, 891882.0, 402716.0, 402445.0, 942248.0, 18847.0, 896284.0, 85443.0, 280296.0, 960945.0, 514717.0, 782452.0, 692122.0, 858035.0, 819884.0, 296651.0, 895939.0, 58516.0, 511592.0, 785310.0, 367630.0, 568539.0, 373003.0, 964958.0, 616276.0, 188833.0, 931079.0, 188766.0, 551682.0, 128128.0, 256257.0, 102077.0, 502777.0, 755939.0, 657962.0, 347616.0, 279145.0, 877123.0, 233389.0, 883411.0, 900382.0, 748375.0, 991831.0, 16442.0, 711394.0, 260642.0, 323844.0, 912024.0, 971574.0, 891819.0, 281449.0, 757011.0, 847654.0, 968867.0, 129312.0, 831540.0, 212618.0, 389576.0, 406780.0, 525983.0, 878435.0, 211742.0, 108207.0, 641782.0, 636518.0, 930511.0, 73449.0, 997796.0, 47106.0, 712570.0, 887718.0, 947392.0, 755276.0, 667969.0, 39511.0, 452415.0, 50945.0, 336607.0, 695403.0, 963468.0, 429308.0, 418623.0, 425768.0, 969319.0, 328162.0, 84315.0, 482769.0, 915111.0, 958190.0, 912046.0, 865651.0, 991728.0, 978985.0, 618455.0, 934956.0, 556241.0, 953829.0, 999287.0, 915681.0, 977011.0]

# get kstars, masses, a's, of IDs at present day

greater_1 = cmc20_present.loc[cmc20_present['id'].isin(cmc_binaries_greater_1)]
greater_AU = greater_1[(greater_1['a_AU'] > 0.2)]
print(greater_AU)
snapshot0 = cmc20_init.loc[cmc20_init['id'].isin(greater_AU['id'])]
print(snapshot0)
cosmic = cosmic_present.filter(items=[i-1 for i in greater_AU['id']], axis=0)
cosmic_in = cosmic_init.filter(items=[i-1 for i in greater_AU['id']], axis=0)

kstar1init = snapshot0['bin_startype0']
kstar2init = snapshot0['bin_startype1']
kstar1 = greater_AU['bin_startype0']
kstar2 = greater_AU['bin_startype1']

m1init = snapshot0['m0_MSUN']
m2init = snapshot0['m1_MSUN']
m1 = greater_AU['m0_MSUN']
m2 = greater_AU['m1_MSUN']
m1cosmic = cosmic['mass_1']
m2cosmic = cosmic['mass_2']

ainit = snapshot0['a_AU']
a = greater_AU['a_AU']
cosmic_a = [i/215.032 for i in cosmic['sep']]
cosmic_a_in = [i/215.032 for i in cosmic_in['sep']]

einit = snapshot0['e']
e = greater_AU['e']
ecosmicfinal = cosmic['ecc']

plt.hist(kstar1init, label='kstar1 init', histtype='step')
plt.hist(kstar2init, label='kstar2 init', histtype='step')
plt.hist(kstar1, label='kstar1 final', histtype='step')
plt.hist(kstar2, label='kstar2 final', histtype='step')
plt.legend()
plt.savefig('kstars_of_greater_1.png')
plt.clf()

plt.hist(m1init, label='m1 init', histtype='step')
plt.hist(m2init, label='m2 init', histtype='step')
plt.hist(m1, label='m1 final', histtype='step')
plt.hist(m2, label='m2 final', histtype='step')
plt.legend()
plt.savefig('ms_of_greater_1.png')
plt.clf()

plt.hist(ainit, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='ainit', histtype='step', linewidth=2)
plt.hist(a, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='afinal', histtype='step')
plt.hist(cosmic_a, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='cosmicafinal', histtype='step')
#plt.hist(cosmic_a_in, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='cosmicainit', histtype='step')
plt.legend()
plt.xscale('log')
plt.yscale('log')
#plt.xlim(0, 1)
plt.xlabel('Semimajor Axis [AU]')
plt.savefig('as_of_greater_1.png')
plt.clf()

plt.hist(einit, label='einit', histtype='step')
plt.hist(e, label='efinalcmc', histtype='step')
plt.hist(ecosmicfinal, label='efinalcosmic', histtype='step')
plt.legend()
plt.xlabel('Eccentricity')
plt.savefig('es_of_greater_1.png')
plt.clf()

plt.scatter(ainit, einit, label='initial', s=5)
plt.scatter(a, e, label='final CMC', s=5)
plt.scatter(cosmic_a, ecosmicfinal, label='final COSMIC', s=5)
plt.xscale('log')
plt.xlim(0.003, 10)
plt.xlabel('Semimajor Axis [AU]')
plt.ylabel('Eccentricity')
plt.ylim(0, 1)
plt.legend(loc='upper left')
plt.savefig('avse.png')
plt.clf()
print('len a', len(a))
print('len cosmic a', len(cosmic_a))
print('len init', len(ainit))

plt.scatter(m1init, m2init, label='initial', s=5)
plt.scatter(m1, m2, label='final CMC', s=5)
plt.scatter(m1cosmic, m2cosmic, label='final COSMIC', s=5)
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlim(0.3, 6)
plt.ylim(0.3, 6)
plt.xlabel('Primary mass [M_sol]')
plt.ylabel('Secondary mass [M_sol]')
plt.savefig('mvsm.png')
