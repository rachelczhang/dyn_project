import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

cosmic_data = pd.read_hdf('../../fieldmetfix/bcm.h5', 'bcm')
cosmic_present = cosmic_data[(cosmic_data['tphys'] >= 13699) & (cosmic_data['tphys'] <= 13701)]

pd.set_option('display.max_rows', 2000)
pd.set_option('display.min_rows', 1000)
pd.set_option('display.max_columns', None)

bcm = pd.read_hdf('bcm_esc.h5', 'bcm')
bpp = pd.read_hdf('bpp_esc.h5', 'bpp')

print('bcm', bcm)
print('bpp', bpp)

bcm = bcm.iloc[1::2, :]
bcm = bcm[bcm['tphys'] > 13600]

def count(cond, data):
	#print(data[cond])
	cond_count = len(data[cond].index)
	return cond_count

def print_counts(data):
	print(' FROM ESCAPED BINARIES: ')
	print(' Total # systems: ', count((data['tphys'] > 13600) & (data['kstar_1'] <= 15.0) & (data['kstar_1'] >= 0.0), data))
	print(' Total # single systems: ', count((data['tphys'] > 13600) & ((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0)), data))
	print(' Total # BH singles: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
	print(' Total # NS singles: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
	print(' Total # WD singles: ', count((data['tphys'] > 13600) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
	print(' Total # MS singles: ', count((data['tphys'] > 13600) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
	print(' Total # other singles: ', count((data['tphys'] > 13600) & (((data['kstar_1'] > 1.0) & (data['kstar_1'] < 10.0) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & (data['kstar_2'] > 1.0)  & (data['kstar_2'] < 10.0))), data))
	print(' Total # binary systems: ', count((data['tphys'] > 13600) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0), data))
	print(' Total # binaries with BHs: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0)), data))
	print(' Total # BH-BHs: ', count((data['tphys'] > 13600) & (data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0), data))
	print(' Total # BH-non BH: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 14.0) & (data['kstar_2'] != 14.0) & (data['kstar_2'] != 15.0)) | ((data['kstar_1'] != 14.0) & (data['kstar_1'] != 15.0)& (data['kstar_2'] == 14.0))), data))
	print(' Total # binaries with NSs: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0)), data))
	print(' Total # NS-NSs: ', count((data['tphys'] > 13600) & (data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0), data))
	print(' Total # NS-non NSs: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 13.0) & (data['kstar_2'] < 13.0)) | ((data['kstar_1'] < 13.0) & (data['kstar_2'] == 13.0))), data))
	print(' Total # WD-WDs: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))), data))
	print(' Total # WD-non WDs: ', count((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] < 10.0)) | ((data['kstar_1'] < 10.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))),data))
	print(' Total # MS-MSs: ', count((data['tphys'] > 13600) & (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))), data))
	print(' Total # WD-MS: ', count((data['tphys'] > 13600) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
	print(' Total non-compact-object binaries: ', count((data['tphys'] > 13600) & (data['kstar_1'] < 10.0) & (data['kstar_2'] < 10.0), data))
	print(' Other objects: ', count((data['tphys'] > 13600) & (~((data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0))) & (~((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0))), data))
	print(' Double massless remnants: ', count((data['tphys'] > 13600) & (data['kstar_1'] == 15.0) & (data['kstar_2'] == 15.0), data))

print_counts(bcm)

cosmic_present['bin_num'] += 1
cosmic_present['corresponding_esc?'] = cosmic_present['bin_num'].isin(list(bcm.index))

cosmic_corr_esc = cosmic_present[cosmic_present['corresponding_esc?'] == True]
print('cosmic corr esc', len(cosmic_corr_esc))
print_counts(cosmic_corr_esc)