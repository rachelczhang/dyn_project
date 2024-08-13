import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

cosmic_data = pd.read_hdf('field/bcm.h5', 'bcm')
cmc20_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700022Gyr)')
cmc100_present = pd.read_hdf('dynamics/rv10.0_modified/king.window.snapshots.h5', key='137(t=13.700056Gyr)')
cmc200_present = pd.read_hdf('dynamics/rv20_modified/king.window.snapshots.h5', key='137(t=13.700347Gyr)')
cosmic_present = cosmic_data[cosmic_data['tphys'] == 13700.0]

def find_common_ids(id1list, id2list):
        common_ids = []
        id1 = {}
        for i in id1list:
                id1[i] = True
        for j in id2list:
                if j in id1 and j != 0:
                        common_ids.append(j)
        return common_ids

def count(cond, data):
	cond_count = len(data[cond].index)
	return cond_count

def print_counts(name, data):
	if name=='COSMIC':
		count1 = count((data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] == -1.000000), data)
		print(name+' Total # systems: ', count((data['tphys'] > 0), data)+count1)
		print(name+' Total # single systems: ', count((data['tphys'] > 0) & ((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0)), data))
		print(name+' Total # BH singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
		print(name+' Total # NS singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
		print(name+' Total # WD singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
		print(name+' Total # MS singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
		print(name+' Total # binary systems: ', count((data['tphys'] > 0) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] != -1.000000), data))
		print(name+' Total # binaries with BHs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0)) & (data['sep'] != -1.000000), data))
		print(name+' Total # BH-BHs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0) & (data['sep'] != -1.000000), data))
		print(name+' Total # binaries with NSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0)) & (data['sep'] != -1.000000), data))
		print(name+' Total # NS-NSs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0) & (data['sep'] != -1.000000), data))
		print(name+' Total # WD-WDs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))) & (data['sep'] != -1.000000), data))
		print(name+' Total # MS-MSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) & (data['sep'] != -1.000000), data))
		print(name+' Total # WD-MS: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))) & (data['sep'] != -1.000000), data))	
		#print(name+' Total # blue stragglers: ', count((data['evol_type'] == 14.0)))
	if 'CMC' in name:
		print(name+' Total # systems: ', count((data['startype'] >= 0.0) | (data['bin_startype0'] >= 0.0) | (data['bin_startype1'] >= 0.0), data))
		#print(name+' Total # systems: ', count(((data['startype'] >= 0.0) & (data['startype'] <= 15.0)) | ((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0)), data))
		print(name+' Total # single systems: ', count((data['startype'] >= 0.0) & (data['startype'] <= 15.0), data))
		print(name+' Total # BH singles: ', count((data['startype'] == 14.0), data))
		print(name+' Total # NS singles: ', count((data['startype'] == 13.0), data))
		print(name+' Total # WD singles: ', count(((data['startype'] == 10.0) | (data['startype'] == 11.0) | (data['startype'] == 12.0)), data))
		print(name+' Total # MS singles: ', count(((data['startype'] == 0.0) | (data['startype'] == 1.0)), data))
		print(name+' Total # other singles: ', count((data['startype'] > 1.0) & (data['startype'] < 10.0), data))
		print(name+' Total # binary systems: ', count((data['bin_startype0'] < 15.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 15.0), data))
		#print(name+' Total # binary systems: ', count((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0), data))
		print(name+' Total # binaries with BHs: ', count((data['bin_startype0'] == 14.0) | (data['bin_startype1'] == 14.0), data))
		print(name+' Total # BH-BHs: ', count((data['bin_startype0'] == 14.0) & (data['bin_startype1'] == 14.0), data))
		print(name+' Total # binaries with NSs: ', count(((data['bin_startype0'] == 13.0) & (data['bin_startype1'] < 14.0) & (data['bin_startype1'] >= 0.0)) | ((data['bin_startype0'] < 14.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] == 13.0)), data))
		print(name+' Total # NS-NSs: ', count((data['bin_startype0'] == 13.0) & (data['bin_startype1'] == 13.0), data))
		print(name+' Total # WD-WDs: ', count(((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0)), data))
		print(name+' Total # WD-non WDs: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & (data['bin_startype1'] < 10.0)) | ((data['bin_startype0'] < 10.0) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
		print(name+' Total non-compact-object binaries: ', count((data['bin_startype0'] < 10.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 10.0), data))
		print(name+' Total # MS-MS: ', count(((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0)), data))
		print(name+' Total # WD-MS: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0))) | (((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
		print(name+' Total 15-15s: ', count((data['bin_startype0'] == 15.0) & (data['bin_startype1'] == 15.0), data))


rv2_rv10_ids = find_common_ids(cmc20_present['id'], cmc100_present['id'])
print('len ids', len(rv2_rv10_ids))
rv210_rv20_ids = find_common_ids(rv2_rv10_ids, cmc200_present['id'])
print('len ids', len(rv210_rv20_ids))
cosmic_cmc_ids = find_common_ids(rv210_rv20_ids, [i+1 for i in cosmic_present.index])
print('len ids', len(cosmic_cmc_ids))

relevant_cosmic = cosmic_present.filter(items=[i-1 for i in cosmic_cmc_ids], axis=0)
relevant_cmc20 = cmc200_present.loc[cmc200_present['id'].isin(cosmic_cmc_ids)]
relevant_cmc10 = cmc100_present.loc[cmc100_present['id'].isin(cosmic_cmc_ids)]
relevant_cmc2 = cmc20_present.loc[cmc20_present['id'].isin(cosmic_cmc_ids)]

# all semimajor axes
cosmic_a = [i/215.032 for i in relevant_cosmic['sep']]
cmc20_a = relevant_cmc20['a_AU']
cmc10_a = relevant_cmc10['a_AU']
cmc2_a = relevant_cmc2['a_AU']

print('len cosmic', len(cosmic_a))
print('len cmc rv 20', len(cmc20_a))
print('len cmc rv 10', len(cmc10_a))
print('len cmc rv 2', len(cmc2_a))

plt.hist(cosmic_a, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='COSMIC', histtype='step')
plt.hist(cmc20_a, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='CMC rv20', histtype='step')
plt.hist(cmc10_a, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='CMC rv10', histtype='step')
plt.hist(cmc2_a, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='CMC rv2', histtype='step')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlabel('Semimajor Axis [AU]')
plt.ylabel('Number of binaries')
plt.savefig('nonescaped_as.png')
plt.clf()

# all kstars
#cosmic_kstar1 = relevant_cosmic['kstar_1']
#cosmic_kstar2 = relevant_cosmic['kstar_2']
#cmc20_kstar1 = relevant_cmc20['bin_startype0']
#cmc20_kstar2 = relevant_cmc20['bin_startype1']
#cmc10_kstar1 = relevant_cmc10['bin_startype0']
#cmc10_kstar2 = relevant_cmc20['bin_startype1']
#cmc2_kstar1 = relevant_cmc2['bin_startype0']
#cmc2_kstar2 = relevant_cmc2['bin_startype1']
#plt.hist(cosmic_kstar1, label='COSMIC kstar1', histtype='step')
#plt.hist(cosmic_kstar2, label='COSMIC kstar2', histtype='step')
#plt.hist(cmc20_kstar1, label='CMC rv20 kstar1', histtype='step')
#plt.hist(cmc20_kstar2, label='CMC rv20 kstar2', histtype='step')
#plt.hist(cmc10_kstar1, label='CMC rv10 kstar1', histtype='step')
#plt.hist(cmc10_kstar2, label='CMC rv10 kstar2', histtype='step')
#plt.hist(cmc2_kstar1, label='CMC rv2 kstar1', histtype='step')
#plt.hist(cmc2_kstar2, label='CMC rv2 kstar2', histtype='step')
#plt.savefig('nonescaped_kstars.png')

# print counts
print('COSMIC')
print_counts('COSMIC', relevant_cosmic)
print('CMC rv 20')
print_counts('CMC', relevant_cmc20)
print('CMC rv 10')
print_counts('CMC', relevant_cmc10) 
print('CMC rv 2')
print_counts('CMC', relevant_cmc2)

# plot binaries with at least one one mass > 5 and their semimajor axis
#cosmic_mg5 = relevant_cosmic[(relevant_cosmic['kstar_1'] == 14) | (relevant_cosmic['kstar_2'] == 14)]
#print(cosmic_mg5)
