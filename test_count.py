import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

cosmic_data = pd.read_hdf('field/bcm.h5', 'bcm')
bpp = pd.read_hdf('field/bpp.h5', 'bpp')
cmc20_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700022Gyr)')

def count(cond, data):
        #print('hi', data[cond].index)
        #print('hi2', len(data[cond].index))
        cond_count = len(data[cond].index)
        return cond_count

def print_counts(data):
        print(' Total # systems with two time stamps: ', count((data['tphys'] > 0), data))
        print(' Total # systems with only t = 0: ', count((data['tphys'] == 0), data))
        print(' Total # systems with t>0: ', count((data['tphys'] > 0), data))
        print(' Total # systems: ', count((data['tphys'] > 0) & (data['kstar_1'] <= 15.0) & (data['kstar_1'] >= 0.0), data))
        print(' Total # single systems at t=0: ', count((data['tphys'] <= 1.0) & ((data['kstar_1'] == 15.0) | (data['kstar_2'] == 15.0)), data))
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
def print_property(data, prop):
        for i in range(1000000):
                if len(data.loc[i]) != 2:
                        print(len(data.loc[i]))
                        #print(data.loc[i][prop])
                #print(data.loc[i][(data.loc[i]['tphys'] == 13700.0) & (data.loc[i]['kstar_2'] == 15.0)])
                #if data.loc[i][(data.loc[i]['tphys'] == 13700.0) & (data.loc[i]['kstar_2'] == 15.0)]:
                #        print('single', i)
                #        break

#for line in cosmic_data[(cosmic_data['tphys'] > 0)]:
#        print('line', line)
#        if line[cosmic_data['kstar_1'] != 15.0] and line[cosmic_data['kstar_2'] != 15.0]:
#                pass
#        elif line[cosmic_data['kstar_1'] == 15.0] or line[cosmic_data['kstar_2'] == 15.0]:
#                pass
#        else:
#                print('whatever')
#print(bpp.loc[51946]['evol_type'])
#print(bpp.loc[50918]['evol_type'])
#print('cosmic data', cosmic_data)
#print_property(cosmic_data, 'bin_state')
print_counts(cosmic_data)
