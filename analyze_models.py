import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import itertools as it
from enum import Enum

pd.set_option('display.max_rows', 4000)
pd.set_option('display.min_rows', 2000)
pd.set_option('display.max_columns', None)
 
cosmic_data = pd.read_hdf('/projects/b1091/rczhang/testCMCtoymodel/testbselog/cosmicrunonrv2modinit/bcm.h5', 'bcm')
bpp = pd.read_hdf('/projects/b1091/rczhang/testCMCtoymodel/testbselog/cosmicrunonrv2modinit/bpp.h5', 'bpp')
#cosmic_data = pd.read_hdf('fieldmettimefix/bcm.h5', 'bcm')
#bpp = pd.read_hdf('fieldmettimefix/bpp.h5', 'bpp')

# cosmic_init = cosmic_data[cosmic_data['tphys'] == 0.000000]
cosmic_present = cosmic_data[(cosmic_data['tphys'] >= 13800)]
cmc2_init = pd.read_hdf('dynamics/rv2.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
# cmc2_mid = pd.read_hdf('dynamics/rv2.0_modified/king.window.snapshots.h5', key='39(t=3.9000198Gyr)')
# cmc2_mid = pd.read_hdf('dynamics/rv2.0_modified/kingres1.window.snapshots.h5', key='125(t=12.50001Gyr)')
cmc2_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.snapshots.h5', key='738(t=2.8795097)')
#cmc6_init = pd.read_hdf('dynamics/rv6.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
#cmc6_present = pd.read_hdf('dynamics/rv6.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700103Gyr)')
#cmc10_init = pd.read_hdf('dynamics/rv10.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
#cmc10_present = pd.read_hdf('dynamics/rv10.0_modified/king.window.snapshots.h5', key='137(t=13.700056Gyr)')
#cmc20_init = pd.read_hdf('dynamics/rv20_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
#cmc20_present = pd.read_hdf('dynamics/rv20_modified/king.window.snapshots.h5', key='137(t=13.700347Gyr)') 
cosmicrv2_esc = pd.read_hdf('dynamics/rv2.0_modified/bcm_esc.h5', 'bcm')
cosmicrv2_escpres = cosmicrv2_esc[(cosmicrv2_esc['tphys'] >= 13800)]
#cosmicrv6_esc = pd.read_hdf('dynamics/rv6.0_modified/bcm_esc.h5', 'bcm')
#cosmicrv6_escpres = cosmicrv6_esc[(cosmicrv6_esc['tphys'] >= 13800)]
#cosmicrv10_esc = pd.read_hdf('dynamics/rv10.0_modified/bcm_esc.h5', 'bcm')
#cosmicrv10_escpres = cosmicrv10_esc[(cosmicrv10_esc['tphys'] >= 13800)]
#cosmicrv20_esc = pd.read_hdf('dynamics/rv20_modified/bcm_esc.h5', 'bcm')
#cosmicrv20_escpres = cosmicrv20_esc[(cosmicrv20_esc['tphys'] >= 13800)]

nanerrors = bpp[np.isnan(bpp['rad_2'])]
print('nanerrors', nanerrors)

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

def get_semergedisrupt_ids_list(fil):
    id1merge = []
    id2merge = []
    idrmerge = []
    id1dis = []
    id2dis = []
    kstar1merge = []
    kstar2merge = []
    with open(fil, 'r') as f:
        if 'kingres1' not in fil:
            next(f)
        for line in f:
            x = line.split(' ')
            if x[1] != 'disruptboth':
                    delimiters = ["=", "(", ")", "\n"]
                    for delimiter in delimiters:
                        x[2] = " ".join(x[2].split(delimiter))
                        x[3] = " ".join(x[3].split(delimiter))
                    result = x[3].split()
                    result1 = x[2].split()
                    id1merge.append(int(result[1]))
                    id2merge.append(int(result[5]))
                    idrmerge.append(int(result1[1]))
                    delimiters2 = ["=", "\n"]
                    for delim in delimiters2:
                            x[6] = " ".join(x[6].split(delim))
                            x[7] = " ".join(x[7].split(delim))
                    result2 = x[6].split()
                    result3 = x[7].split()
                    kstar1merge.append(int(result2[1]))
                    kstar2merge.append(int(result3[1]))
            else:
                    delimiters = ["=", "(", ")"]
                    for delimiter in delimiters:
                            x[2] = " ".join(x[2].split(delimiter))
                            x[3] = " ".join(x[3].split(delimiter))
                    result1 = x[2].split()
                    result2 = x[3].split()
                    id1dis.append(int(result1[1]))
                    id2dis.append(int(result2[1]))
    f.close()
    print('mergedis IDs lengths', 'id1merge', len(id1merge), 'id2merge', len(id2merge))
    return id1merge, id2merge, idrmerge, id1dis, id2dis, kstar1merge, kstar2merge

# def merge_two_dicts(dict1, dict2):
#     merged = {}
#     for d in [dict1, dict2]:
#         for key, value in d.items():
#             if key not in merged:
#                 merged[key] = value
#             else:
#                 merged[key].extend(value)
#     return merged

def read_semergedisrupt_file(file_path, secondfile):
    f = file_path+'king.semergedisrupt.log'
    id1merge, id2merge, idrmerge, id1dis, id2dis, kstar1merge, kstar2merge = get_semergedisrupt_ids_list(f)
    if secondfile:
        g = file_path+'kingres1.semergedisrupt.log'
        id1merge1, id2merge1, idrmerge1, id1dis1, id2dis1, kstar1merge1, kstar2merge1 = get_semergedisrupt_ids_list(g)
        id1merge.extend(id1merge1)
        id2merge.extend(id2merge1)
        idrmerge.extend(idrmerge1)
        id1dis.extend(id1dis1)
        id2dis.extend(id2dis1)
        kstar1merge.extend(kstar1merge1)
        kstar2merge.extend(kstar2merge1)
        # kstarmerge = merge_two_dicts(kstarmergedict, kstarmergedict1)
    return id1merge, id2merge, idrmerge, id1dis, id2dis, kstar1merge, kstar2merge

def get_esc_ids(fil):
    id1 = []
    id2 = []
    id0 = []
    with open(fil, 'r') as f:
        if 'kingres1' not in fil:
            next(f)
        for line in f:
            x = line.split(' ')
            id1.append(int(x[17]))
            id2.append(int(x[18]))
            id0.append(int(x[13]))
    f.close()
    print('escapers IDs lengths', 'id1', len(id1), 'id2', len(id2), 'id0', len(id0))
    return id1, id2, id0

def read_escape_file(file_path, secondfile):
    f = file_path+'king.esc.dat'
    id1, id2, id0 = get_esc_ids(f)
    if secondfile:
        g = file_path+'kingres1.esc.dat'
        id11, id21, id01 = get_esc_ids(g)
        id1.extend(id11)
        id2.extend(id21)
        id0.extend(id01)
    return id1, id2, id0 

def count(cond, data):
	cond_count = len(data[cond].index)
	return cond_count

def print_counts_cmc(data):
    print('Total # systems: ', count((data['startype'] >= 0.0) | (data['bin_startype0'] >= 0.0) | (data['bin_startype1'] >= 0.0), data))
    #print('Total # systems: ', count(((data['startype'] >= 0.0) & (data['startype'] <= 15.0)) | ((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0)), data))
    print('Total # single systems: ', count((data['startype'] >= 0.0) & (data['startype'] <= 15.0), data))
    print('Total # BH singles: ', count((data['startype'] == 14.0), data))
    print('Total # NS singles: ', count((data['startype'] == 13.0), data))
    print('Total # WD singles: ', count(((data['startype'] == 10.0) | (data['startype'] == 11.0) | (data['startype'] == 12.0)), data))
    print('Total # MS singles: ', count(((data['startype'] == 0.0) | (data['startype'] == 1.0)), data))
    print('Total # other singles: ', count((data['startype'] > 1.0) & (data['startype'] < 10.0), data))
    print('Total # binary systems: ', count((data['bin_startype0'] < 15.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 15.0), data))
    #print('Total # binary systems: ', count((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0), data))
    print('Total # binaries with BHs: ', count((data['bin_startype0'] == 14.0) | (data['bin_startype1'] == 14.0), data))
    print('Total # BH-BHs: ', count((data['bin_startype0'] == 14.0) & (data['bin_startype1'] == 14.0), data))
    print('Total # binaries with NSs: ', count(((data['bin_startype0'] == 13.0) & (data['bin_startype1'] < 14.0) & (data['bin_startype1'] >= 0.0)) | ((data['bin_startype0'] < 14.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] == 13.0)), data))
    print('Total # NS-NSs: ', count((data['bin_startype0'] == 13.0) & (data['bin_startype1'] == 13.0), data))
    print('Total # WD-WDs: ', count(((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0)), data))
    print('Total # WD-non WDs: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & (data['bin_startype1'] < 10.0)) | ((data['bin_startype0'] < 10.0) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
    print('Total non-compact-object binaries: ', count((data['bin_startype0'] < 10.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 10.0), data))
    print('Total # MS-MS: ', count(((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0)), data))
    print('Total # WD-MS: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0))) | (((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
    print('Total 15-15s: ', count((data['bin_startype0'] == 15.0) & (data['bin_startype1'] == 15.0), data))

def print_counts_cosmic(data):
    print(' Total # systems: ', count((data['tphys'] > 0), data))
    print(' Total # single systems: ', count((data['tphys'] > 0) & ((data['kstar_1'] == 15.0) ^ (data['kstar_2'] == 15.0)), data))
    print(' Total # BH singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 14.0))|((data['kstar_1'] == 14.0) & (data['kstar_2'] == 15.0))), data))
    print(' Total # NS singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] == 13.0))|((data['kstar_1'] == 13.0) & (data['kstar_2'] == 15.0))), data))
    print(' Total # WD singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))), data))
    print(' Total # MS singles: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & (data['kstar_2'] == 15.0)) | ((data['kstar_1'] == 15.0) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0)))), data))
    print(' Total # other singles: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 15.0) & (data['kstar_2'] < 10.0) & (data['kstar_2'] > 1.0))|((data['kstar_2'] == 15.0) & (data['kstar_1'] < 10.0) & (data['kstar_1'] > 1.0))), data))
    print(' Total # binary systems: ', count((data['tphys'] > 0) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] != -1.000000), data))
    print(' Total # binaries with BHs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 14.0) | (data['kstar_2'] == 14.0)) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0)) & (data['sep'] != -1.000000), data))
    print(' Total # BH-BHs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 14.0) & (data['kstar_2'] == 14.0) & (data['sep'] != -1.000000), data))
    print(' Total # BH-non BH: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 14.0) & (data['kstar_2'] != 14.0) & (data['kstar_2'] != 15.0)) | ((data['kstar_1'] != 14.0) & (data['kstar_1'] != 15.0)& (data['kstar_2'] == 14.0))) & (data['sep'] != -1.000000), data))
    print(' Total # binaries with NSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 13.0) | (data['kstar_2'] == 13.0)) & (data['kstar_1'] < 14.0) & (data['kstar_2'] < 14.0)) & (data['sep'] != -1.000000), data))
    print(' Total # NS-NSs: ', count((data['tphys'] > 0) & (data['kstar_1'] == 13.0) & (data['kstar_2'] == 13.0) & (data['sep'] != -1.000000), data))
    print(' Total # NS-non NSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 13.0) & (data['kstar_2'] < 13.0)) | ((data['kstar_1'] < 13.0) & (data['kstar_2'] == 13.0))) & (data['sep'] != -1.000000), data))
    print(' Total # WD-WDs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))) & (data['sep'] != -1.000000), data))
    print(' Total # WD-non WDs: ', count((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & (data['kstar_2'] < 10.0)) | ((data['kstar_1'] < 10.0) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0))) & (data['sep'] != -1.000000),data))        
    print(' Total # WD-MS: ', count((data['tphys'] > 0) & ((((data['kstar_1'] == 10.0) | (data['kstar_1'] == 11.0) | (data['kstar_1'] == 12.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) | (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 10.0) | (data['kstar_2'] == 11.0) | (data['kstar_2'] == 12.0)))) & (data['sep'] != -1.000000), data))	 
    print(' Total # MS-MSs: ', count((data['tphys'] > 0) & (((data['kstar_1'] == 0.0) | (data['kstar_1'] == 1.0)) & ((data['kstar_2'] == 0.0) | (data['kstar_2'] == 1.0))) & (data['sep'] != -1.000000), data))
    print(' Total non-compact-object binaries: ', count((data['tphys'] > 0) & (data['kstar_1'] < 10.0) & (data['kstar_2'] < 10.0) & (data['sep'] != -1.000000), data))        
    print(' Double massless remnants: ', count((data['tphys'] > 0) & (data['kstar_1'] == 15.0) & (data['kstar_2'] == 15.0), data))
    print(' Total # 2 singles: ', count((data['tphys'] > 0) & (data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] == -1.000000), data))

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

def get_info_of_corr_COSMIC_binaries(CMC_binaries, COSMIC_binaries, binnum):
    corr_cosmic = find_corresponding_COSMIC_binaries(CMC_binaries, COSMIC_binaries, binnum=binnum)
    print('corr cosmic')
    print_counts_cosmic(corr_cosmic)
    cosmic_prim_bin = corr_cosmic[(corr_cosmic['bin_state'] == 0) & (corr_cosmic['kstar_1'] != 15.0) & (corr_cosmic['kstar_2'] != 15.0)]
    print('primordial binaries count: ', len(cosmic_prim_bin))
    cosmic_prim_bin_small_orbp = cosmic_prim_bin[cosmic_prim_bin['porb'] < 0.1]
    print('COSMIC small orbp primordial binaries')
    print_counts_cosmic(cosmic_prim_bin_small_orbp)
    print(cosmic_prim_bin_small_orbp[cosmic_prim_bin_small_orbp['kstar_2'] == 15.0])
    cosmic_prim_bin_massless = cosmic_prim_bin[(cosmic_prim_bin['kstar_1'] == 15.0) & (cosmic_prim_bin['kstar_2'] == 15.0)]
    print('len', len(cosmic_prim_bin_massless))
    print_counts_cosmic(cosmic_prim_bin)
    cosmic_merge = corr_cosmic[corr_cosmic['bin_state'] == 1]
    print('merged count: ', len(cosmic_merge))
    cosmic_merge_massless = cosmic_merge[(cosmic_merge['kstar_1'] == 15.0) & (cosmic_merge['kstar_2'] == 15.0)]
    print('len', len(cosmic_merge_massless))
    print_counts_cosmic(cosmic_merge)
    BBHmergers = cosmic_merge[(cosmic_merge['merger_type'] == '1414')]
    print('COSMIC BBH mergers count', len(BBHmergers))
    cosmic_dis = corr_cosmic[corr_cosmic['bin_state'] == 2]
    print('disrupted count: ', len(cosmic_dis))
    cosmic_dis_massless = cosmic_dis[(cosmic_dis['kstar_1'] == 15.0) & (cosmic_dis['kstar_2'] == 15.0)]
    print('len', len(cosmic_dis_massless))
    print_counts_cosmic(cosmic_dis)
    return cosmic_prim_bin['porb']

def a_to_p(a, m1, m2):
    mtot = m1+m2 # in solar masses
    period=(a**3/mtot)**(1/2) ##in years
    period=period*365 ##in days
    return period

def analyze(cmcinit, fewbody_ids, merged_ids, id1merge, id2merge, idrmerge, disrupted_ids, rvnum, cmcpresent, cmcescids, cmcescid1, cmcescid2, cosmicesc, kstar1merge, kstar2merge):#, cmcmid):
    # check whether every binary in cluster at initial snapshot was called in FewBody
    cmcinit['runinfewbody'] = cmcinit['id'].isin(fewbody_ids) | cmcinit['id0'].isin(fewbody_ids) | cmcinit['id1'].isin(fewbody_ids)
    runinfewbody = cmcinit[cmcinit['runinfewbody'] == True]
    ################################ CALLED IN FEWBODY ##################################
    # if called by FewBody, what are present day stats? How many went through mergers/disruptions dynamically? How many escaped?
    print('rv' + rvnum + 'in fewbody init', len(runinfewbody))

    ############################# NOT CALLED IN FEWBODY ################################
    ########## PRIMORDIAL BINARIES ############
    # get initial snapshot unperturbed binaries
    nofewbody = cmcinit[cmcinit['runinfewbody'] == False]
    print('rv' + rvnum + 'no fewbody init', len(nofewbody))
    # count # of in-cluster primordial binaries by checking for present-day snapshot binaries with ID0 = initial snapshot ID0 and ID1 = initial snapshot ID1 
    nofewbody_ids = nofewbody.filter(['id0', 'id1'])
    cmcpresent_ids = cmcpresent.filter(['id0', 'id1'])
    print('len nofewbody ids', len(nofewbody_ids))
    print('len cmcpresent ids', len(cmcpresent_ids))
    primordial_binaries = pd.merge(cmcpresent_ids.reset_index(), nofewbody_ids, how='inner').set_index('index')
    print('len primordial binaries', len(primordial_binaries))
    # count # of escaped primordial binaries at t=escaped that have matching ID0 and ID1
    cmcescids_df = pd.DataFrame({'id0': cmcescid1, 'id1': cmcescid2})
    escaped_primordial_binaries = pd.merge(nofewbody_ids.reset_index(), cmcescids_df, how='inner').set_index('index')
    print('len escaped primordial binaries', len(escaped_primordial_binaries))
    #### also check if there are any primordial binaries with id0 and id1 swap 
    nofewbody_ids['id0_swap'] = nofewbody_ids['id0'].copy()
    nofewbody_ids['id1_swap'] = nofewbody_ids['id1'].copy()
    cmcpresent_ids['id0_swap'] = cmcpresent_ids['id1'].copy()
    cmcpresent_ids['id1_swap'] = cmcpresent_ids['id0'].copy()
    nofewbody_ids_swap = nofewbody_ids.filter(['id0_swap', 'id1_swap'])
    cmcpresent_ids_swap = cmcpresent_ids.filter(['id0_swap', 'id1_swap'])
    primordial_binaries_swap = pd.merge(cmcpresent_ids_swap.reset_index(), nofewbody_ids_swap, how='inner').set_index('index')
    print('len primordial binaries swap', len(primordial_binaries_swap))
    cmcescids_df_escaped = pd.DataFrame({'id0_swap': cmcescid2, 'id1_swap': cmcescid1})
    escaped_primordial_binaries_swap = pd.merge(nofewbody_ids_swap.reset_index(), cmcescids_df_escaped, how='inner').set_index('index')
    print('len primordial brinaries swap escaped', len(escaped_primordial_binaries_swap))
    

    ############ MERGED BINARIES #################
    # check which initial snapshot IDs were in the semergedisrupt file
    merged_file = pd.DataFrame({'id0': id1merge, 'id1': id2merge, 'idr': idrmerge, 'kstar1': kstar1merge, 'kstar2': kstar2merge})
    merged_final = merged_file.merge(nofewbody_ids.reset_index(), how='right', on=['id0', 'id1']).dropna().set_index('index')
    merged_final['idr'] = merged_final['idr'].astype(int)
    print('merged no fewbody', len(merged_final))
    # single remnant ID is either ID0 or ID1 which is already not called in FewBody, so IDr is also not called in FewBody
    # check how many of these remnants are in the present snapshot vs. escaped
    merged_final['incluster'] = merged_final['idr'].isin(list(cmcpresent['id'])) 
    merged_final_incluster = merged_final[merged_final['incluster'] == True]
    print('merged nofewbody incluster', len(merged_final_incluster))
    merged_final['escaped'] = merged_final['idr'].isin(cmcescids)
    merged_final_escaped = merged_final[merged_final['escaped'] == True]
    print('merged nofewbody escaped', len(merged_final_escaped))
    merged_final_neither = merged_final[(merged_final['incluster'] == False) & (merged_final['escaped'] == False)]
    print('merged nofewbody neither', len(merged_final_neither))
    ## count BBH mergers
    bbh_incluster = merged_final[(merged_final['incluster'] == True) & (merged_final['kstar1'] == 14) & (merged_final['kstar2'] == 14)]
    print('len bbh mergers in cluster: ', len(bbh_incluster))
    print(bbh_incluster)
    bbh_escaped = merged_final[(merged_final['escaped'] == True) & (merged_final['kstar1'] == 14) & (merged_final['kstar2'] == 14)]
    print('len bbh mergers escaped: ', len(bbh_escaped))
    print(bbh_escaped)
    escaped_cosmicevol_nofewbody = find_corresponding_COSMIC_binaries(nofewbody, cosmicesc, binnum = True)
    bbh_escaped_cosmicevol = escaped_cosmicevol_nofewbody[(escaped_cosmicevol_nofewbody['bin_state'] == 1) & (escaped_cosmicevol_nofewbody['merger_type'] == '1414')]
    print('len bbh mergers escaped and run through cosmic: ', len(bbh_escaped_cosmicevol))
    print(bbh_escaped_cosmicevol)

    ############### DISRUPTED BINARIES #####################
    # check which initial snapshot IDs were in disrupted IDs from semergedisrupt file
    nofewbody['disrupted'] = nofewbody['id'].isin(disrupted_ids) | nofewbody['id0'].isin(disrupted_ids) | nofewbody['id1'].isin(disrupted_ids)
    disrupted = nofewbody[nofewbody['disrupted'] == True]
    print('rv' + rvnum + ' disrupted', len(disrupted))
    # check if disrupted binary is in cluster vs. escaped
    disrupted['incluster'] = disrupted['id'].isin(list(cmcpresent['id'])) #| disrupted['id1'].isin(list(cmcpresent['id']))
    disrupted_incluster = disrupted[disrupted['incluster'] == True]
    print('len disrupted no fewbody incluster', len(disrupted_incluster))
    disrupted['escaped'] = disrupted['id'].isin(cmcescids)
    disrupted_escaped = disrupted[disrupted['escaped'] == True]
    print('len disrupted no fewbody escaped', len(disrupted_escaped))

    ################# UNKNOWN UNPERTURBED BINARIES #######################
    nofewbody['unknown'] = ~nofewbody['id0'].isin(list(escaped_primordial_binaries['id0'])) & ~nofewbody['id0'].isin(list(primordial_binaries['id0'])) & ~nofewbody['id0'].isin(list(merged_final['idr']))  \
    & ~nofewbody['id0'].isin(list(disrupted['id0'])) & ~nofewbody['id1'].isin(list(merged_final['idr']))
    unknown = nofewbody[nofewbody['unknown'] == True]
    # print('unknown IDs', unknown['id0'])
    print('len unknown before considering soft binaries', len(unknown))

    unknown['soft_binary_cluster'] = unknown['id'].isin(list(cmcpresent['id']))
    soft_binary_cluster = unknown[unknown['soft_binary_cluster'] == True]
    print('len soft binaries in cluster', len(soft_binary_cluster))

    unknown['soft_binary_escaped'] = unknown['id'].isin(cmcescids)
    soft_binary_escaped = unknown[unknown['soft_binary_escaped'] == True]
    print('len soft binaries escaped', len(soft_binary_escaped))        

    unknown_now = unknown[(unknown['soft_binary_cluster'] == False) & (unknown['soft_binary_escaped'] == False)]
    print('len unknown', len(unknown_now))
    print('unknown IDs', unknown_now['id0'])

    ############## STATS OF ESCAPERS IN COSMIC #######################
    escaped_cosmicevol_nofewbody_prim_bin = escaped_cosmicevol_nofewbody[(escaped_cosmicevol_nofewbody['bin_state'] == 0) & (escaped_cosmicevol_nofewbody['kstar_1'] != 15.0) & (escaped_cosmicevol_nofewbody['kstar_2'] != 15.0)]
    print('escapers run through COSMIC primordial binaries count: ', len(escaped_cosmicevol_nofewbody_prim_bin))
    escaped_cosmicevol_nofewbody_prim_bin_massless = escaped_cosmicevol_nofewbody_prim_bin[(escaped_cosmicevol_nofewbody_prim_bin['kstar_1'] == 15.0) & (escaped_cosmicevol_nofewbody_prim_bin['kstar_2'] == 15.0)]
    print('len', len(escaped_cosmicevol_nofewbody_prim_bin_massless))
    escaped_cosmicevol_nofewbody_merge = escaped_cosmicevol_nofewbody[escaped_cosmicevol_nofewbody['bin_state'] == 1]
    print('escapers run through COSMIC mergers count: ', len(escaped_cosmicevol_nofewbody_merge))
    escaped_cosmicevol_nofewbody_merge_massless = escaped_cosmicevol_nofewbody_merge[(escaped_cosmicevol_nofewbody_merge['kstar_1'] == 15.0) & (escaped_cosmicevol_nofewbody_merge['kstar_2'] == 15.0)]
    print('len', len(escaped_cosmicevol_nofewbody_merge_massless))
    escaped_cosmicevol_nofewbody_dis = escaped_cosmicevol_nofewbody[escaped_cosmicevol_nofewbody['bin_state'] == 2]
    print('escapers run through COSMIC disruptions count: ', len(escaped_cosmicevol_nofewbody_dis))
    escaped_cosmicevol_nofewbody_dis_massless = escaped_cosmicevol_nofewbody_dis[(escaped_cosmicevol_nofewbody_dis['kstar_1'] == 15.0) & (escaped_cosmicevol_nofewbody_dis['kstar_2'] == 15.0)]
    print('len', len(escaped_cosmicevol_nofewbody_dis_massless))

    ##### orbital periods, component masses, eccentricities of the primordial binaries #####
    cmcpresent['primordial_binaries_in_cluster'] = cmcpresent['id0'].isin(list(primordial_binaries['id0']))
    primordial_binaries_in_cluster = cmcpresent[cmcpresent['primordial_binaries_in_cluster'] == True]
    primordial_binaries_in_cluster['orb_p'] = (primordial_binaries_in_cluster['a_AU']**3/(primordial_binaries_in_cluster['m0_MSUN']+primordial_binaries_in_cluster['m1_MSUN']))**(1/2)*365
    primordial_binaries_in_cluster_small_orbp = primordial_binaries_in_cluster[primordial_binaries_in_cluster['orb_p']<0.1]
    print('small orbp in cluster')
    # print(primordial_binaries_in_cluster_small_orbp.filter(['id', 'bin_startype0', 'bin_startype1']))
    print_counts_cmc(primordial_binaries_in_cluster_small_orbp)
    escaped_cosmicevol_nofewbody_prim_bin_small_orbp = escaped_cosmicevol_nofewbody_prim_bin[escaped_cosmicevol_nofewbody_prim_bin['porb']<0.1]
    print('small orbp escaped')
    print_counts_cosmic(escaped_cosmicevol_nofewbody_prim_bin_small_orbp)
    # cosmicesc['primordial_binaries_escaped'] = cosmicesc['bin_num'].isin(list(escaped_cosmicevol_nofewbody_prim_bin['id0']))
    # primordial_binaries_esc = cosmicesc[cosmicesc['primordial_binaries_escaped'] == True]
    # print('porb', primordial_binaries_esc['porb'])

    # print('unknown ex present', cmcpresent.loc[cmcpresent['id'] == 1626432])
    # print('unknown ex mid', cmcmid.loc[cmcmid['id'] == 1626432])
    # print('unknown ex init', cmcinit.loc[cmcinit['id'] == 999994])
    # print('unknown COSMIC ID')
    # print(bpp.loc[bpp['bin_num'] == 968077])
    # print(bpp.loc[bpp['bin_num'] == 844982])


    ############## CORRESPONDING COSMIC BINARIES #####################
    print('nofewbody COSMIC binaries')
    cosmic_porb = get_info_of_corr_COSMIC_binaries(nofewbody, cosmic_present, binnum=False)
    print('COSMIC binary ID: 758434')
    print(bpp.loc[bpp['bin_num'] == 758434])
    print('check init')
    print(cmcinit.loc[cmcinit['id'] == 758435])
    # print('all COSMIC binaries')
    # get_info_of_corr_COSMIC_binaries(cmcinit, cosmic_present, binnum=False)
    # print('fewbody COSMIC binaries')
    # get_info_of_corr_COSMIC_binaries(runinfewbody, cosmic_present, binnum=False)

    return len(runinfewbody), primordial_binaries_in_cluster['orb_p'], escaped_cosmicevol_nofewbody_prim_bin['porb'], cosmic_porb
    
def plot_perturb_pie(len_perturbed, rvnum):
    # labels = 'Perturbed', 'Unperturbed'
    len_unperturb = 10**6 - len_perturbed
    sizes = [len_perturbed/10**4, len_unperturb/10**4]
    fig, ax = plt.subplots(layout="constrained")
    ax.pie(sizes, colors=['red', 'blue'], textprops={'fontsize': 12})
    # fig.suptitle('Virial radius: ' + rvnum + ' pc', fontsize=20)
    fig.savefig('unperturbedpiechartrv' + rvnum + '.png')
    plt.clf()

def plot_properties(incluster, esc, cosmic, name, units):
    cmc = list(incluster)+list(esc)
    # incluster.hist(bins=np.logspace(np.log10(min(incluster)),np.log10(max(incluster)), 50), histtype='step', linestyle='solid', color='blue', label='In cluster')
    # esc.hist(bins=np.logspace(np.log10(min(esc)),np.log10(max(esc)), 50),  histtype='step', linestyle='dashed', color='blue', label='Escaped')
    plt.hist(cmc, bins=np.logspace(np.log10(min(cosmic)),np.log10(max(cosmic)), 50), histtype='step', linestyle='solid', color='blue', label='CMC')
    cosmic.hist(bins=np.logspace(np.log10(min(cosmic)),np.log10(max(cosmic)), 50), histtype='step', linestyle='solid', color='orange', label='COSMIC')
    plt.title(name)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(name + units)
    plt.ylabel('Number of binaries')
    plt.legend()
    plt.savefig(name+'.png')
    plt.clf()

if __name__ == '__main__':
    file_path = sys.argv[1]
    if '2.0' in file_path:
        cmcinit = cmc2_init 
        rvnum = '2'
        cmcpresent = cmc2_present
        secondfile = True
        cosmicpresesc = cosmicrv2_escpres
        # cmcmid = cmc2_mid
    elif '6.0' in file_path:
        cmcinit = cmc6_init
        rvnum = '6'
        cmcpresent = cmc6_present
        secondfile = True
        cosmicpresesc = cosmicrv6_escpres
    elif '10.0' in file_path:
        cmcinit = cmc10_init
        rvnum = '10'
        cmcpresent = cmc10_present
        secondfile = False 
        cosmicpresesc = cosmicrv10_escpres
    elif '20' in file_path:
        cmcinit = cmc20_init
        rvnum = '20'
        cmcpresent = cmc20_present
        secondfile = False
        cosmicpresesc = cosmicrv20_escpres
    fewbody_ids = read_binint_ids(file_path, secondfile)
    id1merge, id2merge, idrmerge, id1dis, id2dis, kstar1merge, kstar2merge = read_semergedisrupt_file(file_path, secondfile)
    merged_ids = id1merge+id2merge
    disrupted_ids = id1dis+id2dis
    cmcescid1, cmcescid2, cmcescid0 = read_escape_file(file_path, secondfile)
    cmcescids = cmcescid1+cmcescid2+cmcescid0 
    len_perturbed, incluster_porb, esc_porb, cosmic_porb = analyze(cmcinit, fewbody_ids, merged_ids, id1merge, id2merge, idrmerge, disrupted_ids, rvnum, cmcpresent, cmcescids, cmcescid1, cmcescid2, cosmicpresesc, kstar1merge, kstar2merge)#, cmcmid)
    plot_perturb_pie(len_perturbed, rvnum)
    plot_properties(incluster_porb, esc_porb, cosmic_porb, 'OrbitalPeriod', '[days]')
