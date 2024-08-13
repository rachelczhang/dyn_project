import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from tqdm import tqdm

cmcinf = pd.read_hdf('dynamics/rvinf_modified/king.window.snapshots.h5', key='51(t=5.1004359Gyr)')
cmcinf_esc = pd.read_hdf('dynamics/rvinf_modified/bcm.h5', 'bcm')
cmcinf_esc_sing = pd.read_hdf('dynamics/rvinf_modified/bcm_singles.h5', 'bcm')
 
def count(cond, data):
        cond_count = len(data[cond].index)
        return cond_count

def print_cmc_counts(data):
                print(' Total # systems: ', count((data['startype'] >= 0.0) | (data['bin_startype0'] >= 0.0) | (data['bin_startype1'] >= 0.0), data))
                #print(name+' Total # systems: ', count(((data['startype'] >= 0.0) & (data['startype'] <= 15.0)) | ((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0)), data))
                print(' Total # single systems: ', count((data['startype'] >= 0.0) & (data['startype'] <= 15.0), data))
                print(' Total # BH singles: ', count((data['startype'] == 14.0), data))
                print(' Total # NS singles: ', count((data['startype'] == 13.0), data))
                print(' Total # WD singles: ', count(((data['startype'] == 10.0) | (data['startype'] == 11.0) | (data['startype'] == 12.0)), data))
                print(' Total # MS singles: ', count(((data['startype'] == 0.0) | (data['startype'] == 1.0)), data))
                print(' Total # other singles: ', count((data['startype'] > 1.0) & (data['startype'] < 10.0), data))
                print(' Total # binary systems: ', count((data['bin_startype0'] < 15.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 15.0), data))
                #print(name+' Total # binary systems: ', count((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0), data))
                print(' Total # binaries with BHs: ', count((data['bin_startype0'] == 14.0) | (data['bin_startype1'] == 14.0), data))	
                print(' Total # BH-BHs: ', count((data['bin_startype0'] == 14.0) & (data['bin_startype1'] == 14.0), data))
                print(' Total # binaries with NSs: ', count(((data['bin_startype0'] == 13.0) & (data['bin_startype1'] < 14.0) & (data['bin_startype1'] >= 0.0)) | ((data['bin_startype0'] < 14.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] == 13.0)), data))
                print(' Total # NS-NSs: ', count((data['bin_startype0'] == 13.0) & (data['bin_startype1'] == 13.0), data))
                print(' Total # WD-WDs: ', count(((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0)), data))
                print(' Total # WD-non WDs: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & (data['bin_startype1'] < 10.0)) | ((data['bin_startype0'] < 10.0) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
                print(' Total non-compact-object binaries: ', count((data['bin_startype0'] < 10.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 10.0), data))
                print(' Total # MS-MS: ', count(((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0)), data))
                print(' Total # WD-MS: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0))) | (((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
                print(' Total 15-15s: ', count((data['bin_startype0'] == 15.0) & (data['bin_startype1'] == 15.0), data))

def escaped_counts(data):
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

def escaped_singles_counts(data):
        print(' FROM ESCAPED SINGLES: ')
        print(' Total # systems: ', count(data['tphys'] > 0, data))
        print(' Total # BH singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
        print(' Total # NS singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
        print(' Total # WD singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
        print(' Total # MS singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
        print(' Total # other singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] > 1.0) & (data['kstar_1'] < 10.0) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & (data['kstar_2'] > 1.0)  & (data['kstar_2'] < 10.0))), data))

#print_cmc_counts(cmcinf)
#escaped_counts(cmcinf_esc)
escaped_singles_counts(cmcinf_esc_sing)
