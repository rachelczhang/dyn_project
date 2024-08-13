import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

cosmic_data = pd.read_hdf('field/bcm.h5', 'bcm')
#cmc15_present = pd.read_hdf('dynamics/rv1.5/kingres1.window.snapshots.h5', key='137(t=13.700091Gyr)')
cmc20_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700022Gyr)')
cmc20_escape = pd.read_hdf('dynamics/rv2.0_modified/bcm.h5', 'bcm')
#cmc60_present = pd.read_hdf('dynamics/rv6.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700103Gyr)')
#cmc80_present = pd.read_hdf('dynamics/rv8.0/king.window.snapshots.h5', key='137(t=13.700134Gyr)')
cmc100_present = pd.read_hdf('dynamics/rv10.0_modified/king.window.snapshots.h5', key='137(t=13.700056Gyr)')
cmc100_escape = pd.read_hdf('dynamics/rv10.0_modified/bcm.h5', 'bcm')
cmc200_present = pd.read_hdf('dynamics/rv20_modified/king.window.snapshots.h5', key='137(t=13.700347Gyr)')
cmc200_escape = pd.read_hdf('dynamics/rv20_modified/bcm.h5', 'bcm')

cmc20_esc_pres = cmc20_escape[cmc20_escape['tphys'] != 0.000000]
cmc100_esc_pres = cmc100_escape[cmc100_escape['tphys'] != 0.000000]
cmc200_esc_pres = cmc200_escape[cmc200_escape['tphys'] != 0.000000]
cosmic_present = cosmic_data[cosmic_data['tphys'] == 13700.0]

cmc20_esc_init = cmc20_escape[cmc20_escape['tphys'] == 0.000000]
cmc100_esc_init = cmc100_escape[cmc100_escape['tphys'] == 0.000000]
cmc200_esc_init = cmc200_escape[cmc200_escape['tphys'] == 0.000000]
cosmic_init = cosmic_data[cosmic_data['tphys'] == 0.000000]

def plot_initial_sep(a, b, c, d):
	m1a = []
	for i in range(len(a['sep'])):
		if round(a['sep'].iloc[i]) != -1:
			m1a.append(a['mass_1'][i])
	#a1 = [i for i in a['sep'] if round(i) != -1]
	#plt.hist(a1, bins=np.linspace(0, 300, 100), label='CMC rv2', histtype='step')
	plt.hist(m1a, bins=np.linspace(0, 300, 100), label='CMC rv2', histtype='step')
	m1b = []
	for i in range(len(b['sep'])):
		if round(b['sep'].iloc[i]) != -1:
			m1b.append(b['mass_1'][i])
	#b1 = [i for i in b['sep'] if round(i) != -1]
	#plt.hist(b1, bins=np.linspace(0, 300, 100), label='CMC rv10', histtype='step')
	plt.hist(m1b, bins=np.linspace(0, 300, 100), label='CMC rv10', histtype='step')
	m1c = []
	for i in range(len(c['sep'])):
		if round(c['sep'].iloc[i]) != -1:
			m1c.append(c['mass_1'][i])
	#c1 = [i for i in c['sep'] if round(i) != -1]
	#plt.hist(c1, bins=np.linspace(0, 300, 100), label='CMC rv20', histtype='step')
	plt.hist(m1c, bins=np.linspace(0, 300, 100), label='CMC rv20', histtype='step')
	m1d = []
	for i in range(len(d['sep'])):
		if round(d['sep'].iloc[i]) != -1:
			m1d.append(d['mass_1'][i])
	#d1 = [i for i in d['sep'] if round(i) != -1]
	#plt.hist(d1, bins=np.linspace(0, 300, 100), label='COSMIC', histtype='step')
	plt.hist(m1d, bins=np.linspace(0, 300, 100), label='COSMIC', histtype='step')
	plt.legend()
	plt.yscale('log')
	plt.xlim(0, 300)
	plt.savefig('escapedinitialmasses.png')
plot_initial_sep(cmc20_esc_init, cmc100_esc_init, cmc200_esc_init, cosmic_init)

#for i in cosmic_present['bin_state']:
#	if i == 1:
#		print('bin state 1')
#	elif i == 2:
#		print('bin state 2')
#print('bin state 1', (cosmic_present['bin_state'] == 1))
#print('bin state 2', (cosmic_present['bin_state'] == 2))

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
			#binscent20, n20 = get_masses(cmc20_present[cmcname], cmc20_present[extra])
			binscent60, n60 = get_masses(cmc60_present[cmcname], cmc60_present[extra])
			#binscent80, n80 = get_masses(cmc80_present[cmcname], cmc80_present[extra])
		else:
			binscent15, n15 = get_masses(cmc15_present[cmcname], cmc15_present[extra], primary=False)
			#binscent20, n20 = get_masses(cmc20_present[cmcname], cmc20_present[extra], primary=False)
			binscent60, n60 = get_masses(cmc60_present[cmcname], cmc60_present[extra], primary=False)
			#binscent80, n80 = get_masses(cmc80_present[cmcname], cmc80_present[extra], primary=False)
	else:
		#binscent15, n15 = cmc_hist(cmc15_present[cmcname])
		binscent20, n20 = cmc_hist(cmc20_present[cmcname])
		#binscent60, n60 = cmc_hist(cmc60_present[cmcname])
		#binscent80, n80 = cmc_hist(cmc80_present[cmcname])
		binscent100, n100 = cmc_hist(cmc100_present[cmcname])
		binscent200, n200 = cmc_hist(cmc200_present[cmcname])
	plt.close()
	plt.plot(binscent, n, label='COSMIC')
	#plt.plot(binscent15, n15, label='CMC rv1.5')
	plt.plot(binscent20, n20, label='CMC rv2')
	#plt.plot(binscent60, n60, label='CMC rv6.0')
	#plt.plot(binscent80, n80, label='CMC rv8.0')
	plt.plot(binscent100, n100, label='CMC rv10')
	plt.plot(binscent200, n200, label='CMC rv20')
	plt.xlabel(param + ' ' + unit)
	plt.yscale('log')
	plt.xscale('log')
	plt.legend()
	plt.title(param + ' of all binaries at present day')
	plt.savefig(param + '.png')
	return

def au_list(cosmic):
	x = [rsol_au(i) for i in cosmic]
	return x

def plot_property_hist(param, cosmicname, cmcname, unit, primary=True, extra=None):
	cosmic = []
	for i in range(len(cosmic_present[cosmicname])):
		if cosmic_present['kstar_1'][i] != 15.0 and cosmic_present['kstar_2'][i] != 15.0 and round(cosmic_present[cosmicname][i]) != -1 and round(cosmic_present[cosmicname][i]) != 0:	
			cosmic.append(cosmic_present[cosmicname][i])
	#cosmic = [i for i in cosmic_present[cosmicname] if (round(i) != -1 and round(i) != 0]
	print('length of cosmic', len(cosmic))
	if cosmicname == 'sep':
		cosmic = au_list(cosmic)
		#cosmic = [rsol_au(i) for i in cosmic]
	if cosmicname == 'sep':
		bins = np.logspace(np.log10(10**(-3)), np.log10(2*10**4), 50)
	elif cosmicname == 'ecc':
		bins = np.linspace(0, 1, 50)
	elif cosmicname == 'mass_1':
		bins = np.linspace(0, 500, 50)
	plt.hist(cosmic, bins=bins, label='COSMIC', histtype='step')
	#if extra != None:
		# get list of primaries and secondaries masses
	#	cmc20_primary_m, cmc20_secondary_m = get_mass(cmc20_present, cmcname, extra)
		# get escaped primaries and secondaries masses
		# add the two primaries lists and secondaries lists	
		# plot primaries and secondaries 
	#else:
		# run the below
	cmc20 = [i for i in cmc20_present[cmcname] if i != -100.0]
	cmc20_esc = [i for i in cmc20_esc_pres[cosmicname] if round(i) != -1]
	if cosmicname == 'sep':
		cmc20_esc = au_list(cmc20_esc)
	cmc20_comb = cmc20+cmc20_esc
	#plt.hist(cmc20_comb, bins=bins, label='CMC rv2', histtype='step')
	cmc100 = [i for i in cmc100_present[cmcname] if i != -100.0]
	cmc100_esc = [i for i in cmc100_esc_pres[cosmicname] if round(i) != -1]
	if cosmicname == 'sep':
		cmc100_esc = au_list(cmc100_esc)
	cmc100_comb = cmc100+cmc100_esc
	#plt.hist(cmc100_comb, bins=bins, label='CMC rv10', histtype='step')
	cmc200 = [i for i in cmc200_present[cmcname] if i != -100.0]
	cmc200_esc = [i for i in cmc200_esc_pres[cosmicname] if round(i) != -1]
	if cosmicname == 'sep':
		cmc200_esc = au_list(cmc200_esc)
	cmc200_comb = cmc200+cmc200_esc
	plt.hist(cmc200_comb, bins=bins, label='CMC rv20', histtype='step')
	plt.hist(cmc100_comb, bins=bins, label='CMC rv10', histtype='step')
	plt.hist(cmc20_comb, bins=bins, label='CMC rv2', histtype='step')
	plt.xlabel(param + ' ' + unit)
	plt.title(param + ' of all binaries at present day')
	if cosmicname == 'sep':
		plt.xscale('log')
		plt.yscale('log')
	plt.legend()
	plt.savefig('present_' + param + '.png')	

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

def additional_singles_COSMIC(data):
	'''
	count the additional singles that are disrupted binaries from COSMIC
	'''
	# BH singles
	count1 = count((((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0)) & (data['sep'] == -1.000000), data)
	print('count 1', count1)
	count2 = count((data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0) & (data['sep'] == -1.000000), data)
	print('count 2', count2)
	print(' Total additional BH singles from disrupted binaries: ', count1+count2)
	# NS singles
	count3 = count((((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0)) & (data['sep'] == -1.000000), data)
	count4 = count((data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0) & (data['sep'] == -1.000000), data)
	print(' Total additional NS singles from disrupted binaries: ', count3+count4)
	# NS singles from BH-NS disruptions
	print(' Additional NS singles from disrupted BH-NSs: ', count((data['sep'] == -1.000000) & (((data['kstar_1'] == 14.0) & (data['kstar_2'] == 13.0)) | ((data['kstar_1'] == 13.0) & (data['kstar_2'] == 14.0))), data))
	# WD singles from BH-WD disruptions
	print(' Additional WD singles from disrupted BH-WDs: ', count((data['sep'] == -1.000000) & (((data['kstar_1'] == 14.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))) | (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 14.0))), data))
	# MS singles from BH-MS disruptions
	print(' Additional MS singles from disrupted BH-MSs: ', count((data['sep'] == -1.000000) & (((data['kstar_1'] == 14.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 14.0))), data))
	# WD singles from NS-WD disruptions
	print(' Additional WD singles from disrupted NS-WDs: ', count((data['sep'] == -1.000000) & (((data['kstar_1'] == 13.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))) | (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 13.0))), data))
	# MS singles from NS-MS disruptions	
	print(' Additional MS singles from disrupted NS-MSs: ', count((data['sep'] == -1.000000) & (((data['kstar_1'] == 13.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 13.0))), data))

#print(cmc20_present['bin_startype0'])

#print(cosmic_present)
#print_counts('COSMIC', cosmic_present)
#additional_singles_COSMIC(cosmic_present)
#print('CMC rv20')
#print_counts('COSMIC', cmc200_esc_pres)
#additional_singles_COSMIC(cmc200_esc_pres)
#print('CMC rv10')
#print_counts('COSMIC', cmc100_esc_pres)
#additional_singles_COSMIC(cmc100_esc_pres)
#print('CMC rv2')
#print_counts('COSMIC', cmc20_esc_pres)
#additional_singles_COSMIC(cmc20_esc_pres)

#print_counts('CMC rv1.5', cmc15_present)
#print_counts('CMC rv2.0', cmc20_present)
#print_counts('CMC rv6.0', cmc60_present)
#print_counts('CMC rv8.0', cmc80_present)
#print_counts('CMC rv10.0', cmc100_present)
#print_counts('CMC rv20', cmc200_present)
#print_counts('CMC rvinf', cmcinf_present)

#plot_property('Eccentricity', 'ecc', 'e', '')
#plot_property_hist('Eccentricity', 'ecc', 'e', '')
#plot_property_hist('Semimajor Axis', 'sep', 'a_AU', '[AU]')
#plot_property_hist('Primary Masses', 'mass_1', 'm0_MSUN','[M_sol]', primary=True, extra='m1_MSUN')
#plot_property('Primary Masses', 'mass_1', 'm0_MSUN', '[M_sol]', primary=True, extra='m1_MSUN')
#plot_property('Secondary Masses', 'mass_2', 'm0_MSUN', '[M_sol]', primary=False, extra='m1_MSUN')
