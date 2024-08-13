import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

bcm = pd.read_hdf('bcm.h5', 'bcm')
bpp = pd.read_hdf('bpp.h5', 'bpp')

bcm_singles = pd.read_hdf('bcm_singles.h5', 'bcm')
bpp_singles = pd.read_hdf('bpp_singles.h5', 'bpp')

def count(cond, data):
	#print(data[cond])
	cond_count = len(data[cond].index)
	return cond_count

def print_singles_counts(data):
	print(' FROM ESCAPED SINGLES: ')
	print(' Total # systems: ', count(data['tphys'] > 0, data))
	print(' Total # BH singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
	print(' Total # NS singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
	print(' Total # WD singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
	print(' Total # MS singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
	print(' Total # other singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] > 1.0) & (data['kstar_1'] < 10.0) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & (data['kstar_2'] > 1.0)  & (data['kstar_2'] < 10.0))), data))

def print_counts(data):
	print(' FROM ESCAPED BINARIES: ')
	print(' Total # systems: ', count((data['tphys'] > 0) & (data['kstar_1'] <= 15.0) & (data['kstar_1'] >= 0.0), data))
	print(' Total # single systems: ', count((data['tphys'] > 0) & ((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0)), data))
	print(' Total # BH singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
	print(' Total # NS singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
	print(' Total # WD singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
	print(' Total # MS singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
	print(' Total # other singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] > 1.0) & (data['kstar_1'] < 10.0) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & (data['kstar_2'] > 1.0)  & (data['kstar_2'] < 10.0))), data))
	print(' Total # binary systems: ', count((data['tphys'] > 0) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0), data))
	print(' Total # binaries with BHs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0)), data))
	print(' Total # BH-BHs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0), data))
	print(' Total # BH-non BH: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 14.0) & (data['kstar_2'] != 14.0) & (data['kstar_2'] != 15.0)) | ((data['kstar_1'] != 14.0) & (data['kstar_1'] != 15.0)& (data['kstar_2'] == 14.0))), data))
	print(' Total # binaries with NSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0)), data))
	print(' Total # NS-NSs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0), data))
	print(' Total # NS-non NSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 13.0) & (data['kstar_2'] < 13.0)) | ((data['kstar_1'] < 13.0) & (data['kstar_2'] == 13.0))), data))
	print(' Total # WD-WDs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))), data))
	print(' Total # WD-non WDs: ', count((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] < 10.0)) | ((data['kstar_1'] < 10.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))),data))
	print(' Total # MS-MSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))), data))
	print(' Total # WD-MS: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
	print(' Total non-compact-object binaries: ', count((data['tphys'] > 0) & (data['kstar_1'] < 10.0) & (data['kstar_2'] < 10.0), data))
	print(' Other objects: ', count((data['tphys'] > 0) & (~((data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0))) & (~((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0))), data))
	print(' Double massless remnants: ', count((data['tphys'] > 0) & (data['kstar_1'] == 15.0) & (data['kstar_2'] == 15.0), data))
		

def fix_print_counts(data):
        # FROM ESCAPED BINARIES
        count1 = count((data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] == -1.000000), data)
        print(' Total # systems: ', count((data['tphys'] > 0), data)+count1)
        print(' Total # single systems: ', count((data['tphys'] > 0) & ((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0)), data))
        print(' Total # BH singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
        print(' Total # NS singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
        print(' Total # WD singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
        print(' Total # MS singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
        print(' Total # binary systems: ', count((data['tphys'] > 0) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] != -1.000000), data))
        print(' Total # binaries with BHs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0)) & (data['sep'] != -1.000000), data))
        print(' Total # BH-BHs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0) & (data['sep'] != -1.000000), data))
        print(' Total # binaries with NSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0)) & (data['sep'] != -1.000000), data))
        print(' Total # NS-NSs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0) & (data['sep'] != -1.000000), data))
        print(' Total # WD-WDs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))) & (data['sep'] != -1.000000), data))
        print(' Total # MS-MSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) & (data['sep'] != -1.000000), data))
        print(' Total # WD-MS: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))) & (data['sep'] != -1.000000), data))	
	
#print_counts(bcm)
fix_print_counts(bcm)
#print_singles_counts(bcm_singles)
