import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import itertools as it
import corner

cosmic_data = pd.read_hdf('fieldmettimefix/bcm.h5', 'bcm')
cosmic_present = cosmic_data[(cosmic_data['tphys'] >= 13800)]
cmc2_init = pd.read_hdf('dynamics/rv2.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
cmc2_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.snapshots.h5', key='738(t=2.8795097)')
cosmicrv2_esc = pd.read_hdf('dynamics/rv2.0_modified/bcm_esc.h5', 'bcm')
cosmicrv2_escpres = cosmicrv2_esc[(cosmicrv2_esc['tphys'] >= 13800)]

def convert_value(s):
    f = None
    try:
        f = float(s)
        i = int(s)
        return i if i == f else f
    except ValueError:
        if (f):
            return f
        return s
        
def parse_line(s):
    return {key: convert_value(value) for key, value in (item.split("=") for item in s.split(" "))}

def parse_interaction(group):
    interaction = {"input": [], "output": [], "params": []}
    for line in group:
        if (line.startswith("type")):
            interaction = {**interaction, **parse_line(line)}
        if (line.startswith("IS EXCEPTION")):
            is_exception = line.split(": ")[1] == "1\n"
            interaction["is_exception"] = is_exception
        if (line.startswith("input")):
            info = parse_line(line.split(": ")[1])
            interaction["input"].append(info)
        if (line.startswith("output")):
            info = parse_line(line.split(": ")[1])
            interaction["output"].append(info)
        if (line.startswith("params")):
            info = parse_line(line.split(": ")[1])
            interaction["params"].append(info)
    return interaction

def get_fewbody_ids_list(file):
    with open(file, 'r') as f:
        fewbody_ids = []
        for key,group in it.groupby(f,lambda line: line.startswith('******************')):
                if not key: 
                    group = list(group)
                    interaction = parse_interaction(group)
                    for inp in interaction['input']:
                        if inp['type'] == 'binary':
                            fewbody_ids.append(inp['id0'])
                            fewbody_ids.append(inp['id1'])
                        elif inp['type'] == 'single':
                            fewbody_ids.append(inp['id'])
    return fewbody_ids 

def read_binint_ids(file_path, secondfile):
    f = file_path+'king.binint.log'
    fewbody_ids = get_fewbody_ids_list(f)
    if secondfile: 
        g = file_path+'kingres1.binint.log'
        fewbody_ids1 = get_fewbody_ids_list(g)
        fewbody_ids.extend(fewbody_ids1)
    return fewbody_ids

def find_corresponding_COSMIC_binaries(CMC_binaries, COSMIC_binaries, binnum):
    # given a dataframe with CMC binaries, return the corresponding COSMIC binaries for easy comparison between the two
    ## save the CMC binaries IDs
    cmc_ids = list(CMC_binaries['id'])# + list(CMC_binaries['id0']) + list(CMC_binaries['id1'])
    ## change COSMIC ID column to corresponding CMC IDs
    corr_cosmic_data = COSMIC_binaries.filter(['tphys', 'bin_num', 'kstar_1', 'kstar_2', 'sep', 'porb', 'mass_1', 'mass_2', 'bin_state', 'merger_type'])
    if binnum == False:
        corr_cosmic_data['bin_num'] += 1
    ## filter the binaries with COSMIC IDs that are in the CMC binaries IDs
    corr_cosmic_data['corrbin'] = corr_cosmic_data['bin_num'].isin(cmc_ids)
    corr_cosmic = corr_cosmic_data[corr_cosmic_data['corrbin'] == True]
    return corr_cosmic

def howsimilar(cmc, cosmic):
	# this returns the dataframes of binaries that end up with the same, similar, or different evolutions between COSMIC and CMC
	# print('len cmc', len(cmc))
	# print('len cosmic', len(cosmic))
	cmc.set_index('id', drop=False, inplace=True)
	cosmic.set_index('bin_num', drop=False, inplace=True)
	combined = pd.concat([cmc, cosmic], axis=1)
	same_kstar = combined[(combined['bin_startype0'] == combined['kstar_1']) & (combined['bin_startype1'] == combined['kstar_2'])]
	same = same_kstar[(round(same_kstar['m0_MSUN'], 5) == round(same_kstar['mass_1'], 5)) & (round(same_kstar['m1_MSUN'], 5) == round(same_kstar['mass_2'], 5))]
	similar = same_kstar[(round(same_kstar['m0_MSUN'], 5) != round(same_kstar['mass_1'], 5)) | (round(same_kstar['m1_MSUN'], 5) != round(same_kstar['mass_2'], 5))]
	different = combined[(combined['bin_startype0'] != combined['kstar_1']) | (combined['bin_startype1'] != combined['kstar_2'])]
	print('different', different.filter(['bin_startype0', 'bin_startype1', 'm0_MSUN', 'm1_MSUN', 'kstar_1', 'kstar_2', 'mass_1', 'mass_2']))
	print('similar', similar.filter(['bin_startype0', 'bin_startype1', 'm0_MSUN', 'm1_MSUN', 'kstar_1', 'kstar_2', 'mass_1', 'mass_2']))
	print('same', same.filter(['bin_startype0', 'bin_startype1', 'm0_MSUN', 'm1_MSUN', 'kstar_1', 'kstar_2', 'mass_1', 'mass_2']))
	return same, similar, different

def compare(cmcinit, cmcpresent, cosmicpresent, cmcescpres, fewbody_ids):
	cmcinit['runinfewbody'] = cmcinit['id'].isin(fewbody_ids) | cmcinit['id0'].isin(fewbody_ids) | cmcinit['id1'].isin(fewbody_ids)
	nofewbody = cmcinit[cmcinit['runinfewbody'] == False]
	### preserved binaries in cluster ####
	primordial_binaries = cmcpresent.merge(nofewbody[['id0', 'id1']].reset_index(), how='right', on=['id0', 'id1']).dropna().set_index('index')
	corr_nofewbody_primbin = find_corresponding_COSMIC_binaries(primordial_binaries, cosmicpresent, binnum=False)
	primbinsame, primbinsimilar, primbindifferent = howsimilar(primordial_binaries, corr_nofewbody_primbin)
	cmcinit['primbinsame'] = cmcinit['id'].isin(list(primbinsame['id']))
	primbinsame_init = cmcinit[cmcinit['primbinsame'] == True]
	cmcinit['primbinsimilar'] = cmcinit['id'].isin(list(primbinsimilar['id']))
	primbinsimilar_init = cmcinit[cmcinit['primbinsimilar'] == True]
	cmcinit['primbindifferent'] = cmcinit['id'].isin(list(primbindifferent['id']))
	primbindifferent_init = cmcinit[cmcinit['primbindifferent'] == True]

	### preserved binaries escaped ####
	### mergers in cluster ####
	### mergers escaped ####
	### disruptions in cluster ####
	### disruptions escaped ####
	### double massless remnants ####
	return primbinsame_init, primbinsimilar_init, primbindifferent_init

def plot_masses(same, similar, diff):
	same_masses = list(same['m0_MSUN']) + list(same['m1_MSUN'])
	similar_masses = list(similar['m0_MSUN']) + list(similar['m1_MSUN'])
	diff_masses = list(diff['m0_MSUN']) + list(diff['m1_MSUN'])
	plt.hist(same_masses, histtype='step', label='Same')
	plt.hist(similar_masses, histtype='step', label='Similar')
	plt.hist(diff_masses, histtype='step', label='Different')
	plt.xlabel('Component masses [M_sun]')
	plt.yscale('log')
	plt.legend()
	plt.savefig('masses_cmc_vs_cosmic.png')
	plt.clf()

def plot_a(same, similar, diff):
	plt.hist(list(same['a_AU']), histtype='step', label='Same')
	plt.hist(list(similar['a_AU']), histtype='step', label='Similar')
	plt.hist(list(diff['a_AU']), histtype='step', label='Different')
	plt.xlabel('Semimajor axis [AU]')
	plt.yscale('log')
	plt.legend()
	plt.savefig('a_cmc_vs_cosmic.png')
	plt.clf()

def a_to_p(a, m1, m2):
    mtot = m1+m2 # in solar masses
    period=(a**3/mtot)**(1/2) ##in years
    period=period*365 ##in days
    return period

def get_parameters(df):
	period = a_to_p(df['a_AU'], df['m0_MSUN'], df['m1_MSUN'])
	return df['m0_MSUN'], df['m1_MSUN'], period, df['e']

def plot_corner(same, similar, diff):
	m0same, m1same, porbsame, eccsame = get_parameters(same)
	m0similar, m1similar, porbsimilar, eccsimilar = get_parameters(similar)
	m0diff, m1diff, porbdiff, eccdiff = get_parameters(diff)
	m0same = np.log10(m0same)
	m0similar = np.log10(m0similar)
	m0diff = np.log10(m0diff)
	m1same = np.log10(m1same)
	m1similar = np.log10(m1similar)
	m1diff = np.log10(m1diff)
	porbsame = np.log10(porbsame)
	porbsimilar = np.log10(porbsimilar)
	porbdiff = np.log10(porbdiff)
	a = np.array([m0same, m1same, porbsame, eccsame])
	b = np.array([m0similar, m1similar, porbsimilar, eccsimilar])
	c = np.array([m0diff, m1diff, porbdiff, eccdiff])
	samples = a.transpose()
	samples1 = b.transpose()
	samples2 = c.transpose()
	figure = corner.corner(samples, color='black', labels=['m0', 'm1', 'porb', 'ecc'], axes_scale=['linear', 'linear', 'log', 'linear'])
	corner.corner(samples1, fig=figure, color='red', labels=['m0', 'm1', 'porb', 'ecc'], axes_scale=['linear', 'linear', 'log', 'linear'])
	corner.corner(samples2, fig=figure, color='blue', labels=['m0', 'm1', 'porb', 'ecc'], axes_scale=['linear', 'linear', 'log', 'linear'])
	plt.savefig('cornerplot.png')
	plt.clf()

	
if __name__ == '__main__':
	file_path = sys.argv[1]
	cmcinit = cmc2_init 
	rvnum = '2'
	cmcpresent = cmc2_present
	secondfile = True
	cosmicpresesc = cosmicrv2_escpres
	fewbody_ids = read_binint_ids(file_path, secondfile)
	primbinsame, primbinsimilar, primbindifferent = compare(cmcinit, cmcpresent, cosmic_present, cosmicpresesc, fewbody_ids)
	plot_corner(primbinsame, primbinsimilar, primbindifferent)
	# plot_masses(primbinsame, primbinsimilar, primbindifferent)
	# plot_a(primbinsame, primbinsimilar, primbindifferent)

