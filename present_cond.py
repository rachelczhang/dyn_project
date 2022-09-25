import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

cosmic_data = pd.read_hdf('field/bcm.h5', 'bcm')
cmc15_present = pd.read_hdf('dynamics/rv1.5/kingres1.window.snapshots.h5', key='137(t=13.700091Gyr)')
cmc20_present = pd.read_hdf('dynamics/rv2.0/kingres1.window.snapshots.h5', key='137(t=13.700097Gyr)')
cmc60_present = pd.read_hdf('dynamics/rv6.0/king.window.snapshots.h5', key='137(t=13.700118Gyr)')
cmc80_present = pd.read_hdf('dynamics/rv8.0/king.window.snapshots.h5', key='137(t=13.700134Gyr)')
cosmic_present = cosmic_data[cosmic_data['tphys'] == 13700.0]

def count(cond, data):
	cond_count = len(data[cond].index)
	return cond_count

def cmc_hist(param):
	cmc = [i for i in param if i != -100.0]
	n, bins, patches = plt.hist(cmc, bins=np.logspace(np.log10(0.0001), np.log10(1000), 200))
	binscent = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
	return binscent, n

def rsol_au(rsol):
	au = rsol*1/215
	return au

def get_masses(m0, m1, primary=True):
	masses = []
	for i in range(len(m0)):
		if m0[i] >= m1[i]:
			if primary==True:
				masses.append(m0[i])
			else:
				masses.append(m1[i])
		elif m1[i] > m0[i]:
			if primary == True:
				masses.append(m1[i])
			else:
				masses.append(m0[i])
	n, bins, patches = plt.hist(masses, bins=np.logspace(np.log10(0.05), np.log10(100), 200))
	binscent = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
	return binscent, n	

def plot_property(param, cosmicname, cmcname, unit, primary=True, extra=None):
	cosmic = [i for i in cosmic_present[cosmicname] if round(i) != -1]
	if cosmicname == 'sep':
		cosmic = [rsol_au(i) for i in cosmic]
	n, bins, patches = plt.hist(cosmic, bins=np.logspace(np.log10(0.005), np.log10(100), 200))
	binscent = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
	if extra != None:
		if primary==True:
			binscent15, n15 = get_masses(cmc15_present[cmcname], cmc15_present[extra])
			binscent20, n20 = get_masses(cmc20_present[cmcname], cmc20_present[extra])
			binscent60, n60 = get_masses(cmc60_present[cmcname], cmc60_present[extra])
			binscent80, n80 = get_masses(cmc80_present[cmcname], cmc80_present[extra])
		else:
			binscent15, n15 = get_masses(cmc15_present[cmcname], cmc15_present[extra], primary=False)
			binscent20, n20 = get_masses(cmc20_present[cmcname], cmc20_present[extra], primary=False)
			binscent60, n60 = get_masses(cmc60_present[cmcname], cmc60_present[extra], primary=False)
			binscent80, n80 = get_masses(cmc80_present[cmcname], cmc80_present[extra], primary=False)
	else:
		binscent15, n15 = cmc_hist(cmc15_present[cmcname])
		binscent20, n20 = cmc_hist(cmc20_present[cmcname])
		binscent60, n60 = cmc_hist(cmc60_present[cmcname])
		binscent80, n80 = cmc_hist(cmc80_present[cmcname])
	plt.close()
	plt.plot(binscent, n, label='COSMIC')
	plt.plot(binscent15, n15, label='CMC rv1.5')
	plt.plot(binscent20, n20, label='CMC rv2.0')
	plt.plot(binscent60, n60, label='CMC rv6.0')
	plt.plot(binscent80, n80, label='CMC rv8.0')
	plt.xlabel(param + ' ' + unit)
	plt.yscale('log')
	plt.xscale('log')
	plt.legend()
	plt.title(param + ' of all binaries at present day')
	plt.savefig(param + '.png')
	return

def print_counts(name, data):
	if name=='COSMIC':
		print(name+' Total # systems: ', count((data['kstar_1'] <= 15.0) & (data['kstar_1'] >= 0.0), data))
		print(name+' Total # single systems: ', count((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0), data))
		print(name+' Total # binary systems: ', count((data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0), data))
		print(name+' Total # binaries with BHs: ', count(((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0), data))
		print(name+' Total # BH-BHs: ', count((data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0), data))
		print(name+' Total # binaries with NSs: ', count(((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0), data))
		print(name+' Total # NS-NSs: ', count((data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0), data))
		print(name+' Total # WD-WDs: ', count(((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)), data))
		print(name+' Total # MS-MSs: ', count(((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)), data))
		print(name+' Total # WD-MS: ', count((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))), data))	
		#print(name+' Total # blue stragglers: ', count((data['evol_type'] == 14.0)))
	if 'CMC' in name:
		print(name+' Total # systems: ', count(((data['startype'] >= 0.0) & (data['startype'] <= 15.0)) | ((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0)), data))
		print(name+' Total # single systems: ', count((data['startype'] >= 0.0) & (data['startype'] <= 15.0), data))
		print(name+' Total # binary systems: ', count((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0), data))
		print(name+' Total # binaries with BHs: ', count((data['bin_startype0'] == 14.0) | (data['bin_startype1'] == 14.0), data))
		print(name+' Total # BH-BHs: ', count((data['bin_startype0'] == 14.0) & (data['bin_startype1'] == 14.0), data))
		print(name+' Total # binaries with NSs: ', count(((data['bin_startype0'] == 14.0) & (data['bin_startype1'] < 14.0)) | ((data['bin_startype0'] < 14.0) & (data['bin_startype1'] == 14.0)), data))
		print(name+' Total # NS-NSs: ', count((data['bin_startype0'] == 13.0) & (data['bin_startype1'] == 13.0), data))
		print(name+' Total # WD-WDs: ', count(((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0)), data))
		print(name+' Total # MS-MS: ', count(((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0)), data))
		print(name+' Total # WD-MS: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0))) | (((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))

#print_counts('COSMIC', cosmic_present)
#print_counts('CMC rv1.5', cmc15_present)
#print_counts('CMC rv2.0', cmc20_present)
#print_counts('CMC rv6.0', cmc60_present)
#print_counts('CMC rv8.0', cmc80_present)

#plot_property('Eccentricity', 'ecc', 'e', '')
#plot_property('Semimajor Axis', 'sep', 'a_AU', '[AU]')
plot_property('Primary Masses', 'mass_1', 'm0_MSUN', '[M_sol]', primary=True, extra='m1_MSUN')
plot_property('Secondary Masses', 'mass_2', 'm0_MSUN', '[M_sol]', primary=False, extra='m1_MSUN')
