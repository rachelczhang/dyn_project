import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 4000)
pd.set_option('display.min_rows', 2000)
pd.set_option('display.max_columns', None)
 
cosmic_data = pd.read_hdf('fieldmetfix/bcm.h5', 'bcm')
bpp = pd.read_hdf('fieldmetfix/bpp.h5', 'bpp')
cosmic_init = cosmic_data[cosmic_data['tphys'] == 0.000000]
cosmic_present = cosmic_data[(cosmic_data['tphys'] >= 13699) & (cosmic_data['tphys'] <= 13701)]
cmc20_init = pd.read_hdf('dynamics/rv2.0_modified/king.window.snapshots.h5', key='0(t=0Gyr)')
cmc20_present = pd.read_hdf('dynamics/rv2.0_modified/kingres1.window.snapshots.h5', key='137(t=13.700022Gyr)')

# testing below shows that COSMIC ID is always 1 below CMC ID
# ind = -1
#print(cosmic_data.loc[ind]['mass_1'])
#print(cosmic_data.loc[ind]['mass_2'])
#print(cmc20_init)
#print (cmc20_present['id'])
#print(cmc20_init['id'])
#print(cmc20_init.loc[ind]['id'])
#print(cmc20_init.loc[ind]['m0_MSUN'])
#print(cmc20_init.loc[ind]['m1_MSUN'])
#print("cosmic")
#print(cosmic_init.filter(items=["mass_1", "mass_2", "kstar_1", "kstar_2"]))
#print("cmc")
#print(cmc20_init.filter(items=["m0_MSUN", "m1_MSUN", "bin_startype0", "bin_startype1", "id"]))
#print(cmc20_init.index)

def map_CMC_to_COSMIC_id(CMC_id):
        # maps the CMC to COSMIC IDs
        return CMC_id - 1

def map_COSMIC_to_CMC_id(COSMIC_id):
        return COSMIC_id + 1

def find_preserved_cmc_ids():
        cmc20_init_ids = {k: True for k in cmc20_init['id']}
        cmc20_present_ids = {k: True for k in cmc20_present['id']}
        preserved = {}
        new = {}
        for _, cmc_info in cmc20_present.iterrows():
                k = cmc_info['id']
                cosmic_i = k - 1
                i = int(cosmic_i)
                if (i not in cosmic_present.index):
                        continue
                cosmic_info = cosmic_present.loc[i]
                if (k in cmc20_init_ids):
                # filtered more than just the preserved binaries 
                # if (k in cmc20_init_ids) and cmc_info['a_AU'] > 0 and cosmic_info['sep'] > 0: 
                        preserved[k] = True
        for k in cmc20_present_ids:
                if (k not in cmc20_init_ids):
                        new[k] = True
        return preserved, new

def check_id_matches(cmc_preserved):
        error_count = 0 
        preserved_cmc_info = cmc20_init.loc[cmc20_init['id'].isin(cmc_preserved)]
        for _, cmc_info in preserved_cmc_info.iterrows():
                cmc_id = cmc_info['id']
                error = False
                cosmic_id = int(map_CMC_to_COSMIC_id(cmc_id))
                # cosmic_id = int(cmc_id - 1)
                cosmic_info = cosmic_init.iloc[cosmic_id]
                cosmic_fields = ["mass_1", "mass_2"]
                cmc_fields = ["m0_MSUN", "m1_MSUN"]
                for i in range(len(cosmic_fields)):
                        if (abs(cosmic_info[cosmic_fields[i]] - cmc_info[cmc_fields[i]]) > 0.1):
                               error = True 
                if (error):
                        error_count += 1
        print ("ERROR COUNT", error_count)
                
# def mass_bins(data, cmc=True):
#         less_1_ids = []
#         less_1 = []
#         between_1_5_ids = []
#         between_1_5 = []
#         greater_5_ids = []
#         greater_5 = []
#         for key, row in data.iterrows():
#                 if cmc==True:
#                         if row['m0_MSUN'] <= 1 and row['m1_MSUN'] <= 1:
#                                 less_1.append(row['a_AU'])
#                                 less_1_ids.append(row['id'])
#                         elif (row['m0_MSUN'] <= 5 and row['m0_MSUN'] > 1 and row['m1_MSUN'] <= 5) \
#                                 or (row['m1_MSUN'] <= 5 and row['m1_MSUN'] > 1 and row['m0_MSUN'] <= 5):
#                                 between_1_5.append(row['a_AU'])
#                                 between_1_5_ids.append(row['id'])
#                         else:
#                                 greater_5.append(row['a_AU'])
#                                 greater_5_ids.append(row['id'])
#                 else:
#                         if row['mass_1'] <= 1 and row['mass_2'] <= 1:
#                                 less_1.append(row['sep']/215.032)
#                                 #print('row', row)
#                                 less_1_ids.append(row.name)
#                         elif (row['mass_1'] <= 5 and row['mass_1'] > 1 and row['mass_2'] <= 5) \
#                                 or (row['mass_2'] <= 5 and row['mass_2'] > 1 and row['mass_1'] <= 5):
#                                 between_1_5.append(row['sep']/215.032)
#                                 between_1_5_ids.append(row.name)
#                         else:
#                                 greater_5.append(row['sep']/215.032)
#                                 greater_5_ids.append(row.name)
#         return less_1_ids, less_1, between_1_5_ids, between_1_5, greater_5_ids, greater_5

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

def present_cosmic_counts(data):
        # count1 = count((data['kstar_1'] != 15.0) & (data['kstar_2'] != 15.0) & (data['sep'] == -1.000000), data)
        # print(' Total # systems: ', count((data['tphys'] > 0), data)+count1)
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

def present_cmc_counts(data):
        print(' Total # systems: ', count((data['startype'] >= 0.0) | (data['bin_startype0'] >= 0.0) | (data['bin_startype1'] >= 0.0), data))
        #print(' Total # systems: ', count(((data['startype'] >= 0.0) & (data['startype'] <= 15.0)) | ((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0)), data))
        print(' Total # single systems: ', count((data['startype'] >= 0.0) & (data['startype'] <= 15.0), data))
        print(' Total # BH singles: ', count((data['startype'] == 14.0), data))
        print(' Total # NS singles: ', count((data['startype'] == 13.0), data))
        print(' Total # WD singles: ', count(((data['startype'] == 10.0) | (data['startype'] == 11.0) | (data['startype'] == 12.0)), data))
        print(' Total # MS singles: ', count(((data['startype'] == 0.0) | (data['startype'] == 1.0)), data))
        print(' Total # other singles: ', count((data['startype'] > 1.0) & (data['startype'] < 10.0), data))
        print(' Total # binary systems: ', count((data['bin_startype0'] < 15.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 15.0), data))
        #print(' Total # binary systems: ', count((data['bin_startype0'] >= 0.0) & (data['bin_startype0'] <= 15.0), data))
        print(' Total # binaries with BHs: ', count((data['bin_startype0'] == 14.0) | (data['bin_startype1'] == 14.0), data))
        print(' Total # BH-BHs: ', count((data['bin_startype0'] == 14.0) & (data['bin_startype1'] == 14.0), data))
        print(' Total # binaries with NSs: ', count(((data['bin_startype0'] == 13.0) & (data['bin_startype1'] < 14.0) & (data['bin_startype1'] >= 0.0)) | ((data['bin_startype0'] < 14.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] == 13.0)), data))
        print(' Total # NS-NSs: ', count((data['bin_startype0'] == 13.0) & (data['bin_startype1'] == 13.0), data))
        print(' Total # WD-WDs: ', count(((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0)), data))
        print(' Total # WD-non WDs: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & (data['bin_startype1'] < 10.0)) | ((data['bin_startype0'] < 10.0) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
        print(' Total non-compact-object binaries: ', count((data['bin_startype0'] < 10.0) & (data['bin_startype0'] >= 0.0) & (data['bin_startype1'] >= 0.0) & (data['bin_startype1'] < 10.0), data))
        print(' Total # MS-MS: ', count(((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0)), data))
        print(' Total # WD-MS: ', count((((data['bin_startype0'] == 10.0) | (data['bin_startype0'] == 11.0) | (data['bin_startype0'] == 12.0)) & ((data['bin_startype1'] == 0.0) | (data['bin_startype1'] == 1.0))) | (((data['bin_startype0'] == 0.0) | (data['bin_startype0'] == 1.0)) & ((data['bin_startype1'] == 10.0) | (data['bin_startype1'] == 11.0) | (data['bin_startype1'] == 12.0))), data))
        print(' Double massless remnants: ', count((data['bin_startype0'] == 15.0) & (data['bin_startype1'] == 15.0), data)) 

def get_ids_with_condition(data, cond):
        ids = data[cond].index
        return ids 

def read_collision_file(filename):
        # filename is a string for the file name
        with open('dynamics/rv2.0_modified/'+filename) as f:
                if 'kingres1' not in filename:
                        next(f)
                id1 = []
                id2 = []
                id3 = []
                id4 = []
                for line in f:
                        x = line.split(' ')
                        delimiters = ["=", "(", ")"]
                        for delimiter in delimiters:
                                x[3] = " ".join(x[3].split(delimiter))
                        result = x[3].split()
                        id1.append(int(result[1]))
                        id2.append(int(result[5]))
                        try:
                                id3.append(int(result[9]))
                        except:
                                continue 
                        try:
                                id4.append(int(result[13])) 
                        except:
                                continue
        f.close()
        print('collision IDs lengths', 'id1', len(id1), 'id2', len(id2), 'id3', len(id3), 'id4', len(id4))
        return id1, id2, id3, id4

def read_escape_file(filename):
        id1 = []
        id2 = []
        id0 = []
        with open('dynamics/rv2.0_modified/'+filename) as f:
                if 'kingres1' not in filename:
                        next(f)
                for line in f:
                        x = line.split(' ')
                        id1.append(int(x[17]))
                        id2.append(int(x[18]))
                        id0.append(int(x[13]))
        f.close()
        print('escapers IDs lengths', 'id1', len(id1), 'id2', len(id2), 'id0', len(id0))
        return id1, id2, id0

def read_semergedisrupt_file(filename):
        id1merge = []
        kstar1merge = []
        id2merge = []
        kstar2merge = []
        id1dis = []
        id2dis = []
        with open('dynamics/rv2.0_modified/'+filename) as f:
                if 'kingres1' not in filename:
                        next(f)
                for line in f:
                        x = line.split(' ')
                        if x[1] != 'disruptboth':
                                delimiters = ["=", "(", ")"]
                                for delimiter in delimiters:
                                        x[3] = " ".join(x[3].split(delimiter))
                                result = x[3].split()
                                id1merge.append(int(result[1]))
                                id2merge.append(int(result[5]))
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
        print('mergedis IDs lengths', 'id1merge', len(id1merge), 'id2merge', len(id2merge), 'kstar1', len(kstar1merge), 'kstar2', len(kstar2merge))
        return id1merge, id2merge, id1dis, id2dis, kstar1merge, kstar2merge

def count_ids_in_cosmic_not_cmc(ids_list, cosmic_nonpreserved):
        print('length of union', len(ids_list))
        dict_of_cosmic_ids = {k: True for k in cosmic_nonpreserved['bin_num']}
        in_cosmic = []
        for i in ids_list:
                if i in dict_of_cosmic_ids:
                        in_cosmic.append(i)
        print('length of IDs in COSMIC', len(in_cosmic))
        nonpres = []
        dict_of_cmc_ids = {k: True for k in cmc20_present['id']}
        for m in in_cosmic:
                if m not in dict_of_cmc_ids:
                        nonpres.append(m)
        print('length of nonpres IDs', len(nonpres))

repeat = 2000912
if __name__ == '__main__':
        # # get total lengths 
        # print('cosmic initial length', len(cosmic_init))
        # print ("cosmic present length", len(cosmic_present))
        # print('cmc initial length', len(cmc20_init))
        # print ("cmc present length", len(cmc20_present))

        # # filter out preserved data 
        # preserved1, new1 = find_preserved_cmc_ids()        
        # check_id_matches(preserved1)     
        # preserved_cmc = cmc20_present.loc[cmc20_present['id'].isin(preserved1)]
        # print ("preserved cmc", len(preserved_cmc))
        # # seps_for_preserved_cmc = preserved_cmc['a_AU']
        # # seps_for_preserved_cmc = [i for i in seps_for_preserved_cmc]

        # # cosmic_preserved_ids = map(map_CMC_to_COSMIC_id, preserved1)
        # cosmic_preserved_ids = [map_CMC_to_COSMIC_id(x) for x in preserved1]
        # # preserved_cosmic = cosmic_present[cosmic_present.index.isin(cosmic_preserved_ids)]
        # preserved_cosmic = cosmic_present.filter(items=cosmic_preserved_ids, axis=0)
        # print('preserved cosmic', len(preserved_cosmic))
       
        # # filter out the preserved binaries that start and end as MS
        # preserved_cmc_ms = preserved_cmc[((preserved_cmc['bin_startype0'] == 1.0) | (preserved_cmc['bin_startype0'] == 0.0)) & ((preserved_cmc['bin_startype1'] == 1.0) | (preserved_cmc['bin_startype1'] == 0.0)) & (preserved_cmc['a_AU'] > 0)]
        # print('# of MS CMC', len(preserved_cmc_ms))
        # preserved_cosmic_ms = preserved_cosmic[((preserved_cosmic['kstar_1'] == 1.0) | (preserved_cosmic['kstar_1'] == 0.0)) & ((preserved_cosmic['kstar_2'] == 1.0) | (preserved_cosmic['kstar_2'] == 0.0)) & (preserved_cosmic['sep'] > 0)]
        # print('# of MS COSMIC', len(preserved_cosmic_ms))
        # common_ids = find_common_ids(preserved_cmc_ms['id'], [i+1 for i in preserved_cosmic_ms.index])
        # print('# common ids', len(common_ids))
        # cmc_preserve_final = preserved_cmc_ms.loc[preserved_cmc_ms['id'].isin(common_ids)]
        # cosmic_preserve_final = preserved_cosmic_ms.filter(items=[i-1 for i in common_ids], axis=0)
        # cosmic_in = cosmic_init.filter(items=[i-1 for i in common_ids], axis=0)
        # test = cmc20_init.loc[cmc20_init['id'].isin(common_ids)]
        # print('# of MS CMC', len(cmc_preserve_final))
        # print('# of MS COSMIC', len(cosmic_preserve_final))
        # print('# of init', len(cosmic_in))

        # cosmic_preserve_final_a = [i/215.032 for i in cosmic_preserve_final['sep']]
        # cmc_preserve_final_a = cmc_preserve_final['a_AU']
        # ini_a = [i/215.032 for i in cosmic_in['sep']]
        # #test_a = test['a_AU']

        # # plotting
        # plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
        # plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
        # plt.rcParams['savefig.bbox'] = 'tight'
        # plt.rcParams.update({'font.size': 18})
        # plt.hist(cmc_preserve_final_a, bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='CMC rv2 Final',  histtype='step')
        # plt.hist(cosmic_preserve_final_a, bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='COSMIC Final',  histtype='step')
        # plt.hist(ini_a, bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='Initial',  histtype='step')        
        # #plt.hist(test_a, bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='test',  histtype='step') 
        # plt.xscale('log')
        # #plt.yscale('log')
        # plt.xlabel('Semimajor Axis [AU]')
        # plt.ylabel('Number of MS binaries')
        # plt.legend(fontsize=15)
        # plt.savefig('semimajoraxisMSfixmet.png')
        # plt.clf()
 
        # print('most massive initial binary: ', max(max(test['m0_MSUN']), max(test['m1_MSUN'])))
        # print('most massive final binary: ', max(max(cmc_preserve_final['m0_MSUN']), max(cmc_preserve_final['m1_MSUN'])))
        # print('average mass of initial binaries: ', (sum(test['m0_MSUN']) + sum(test['m1_MSUN']))/(len(test['m0_MSUN'])+len(test['m1_MSUN'])))
        # print('average mass of final binaries: ', (sum(cmc_preserve_final['m0_MSUN']) + sum(cmc_preserve_final['m1_MSUN']))/(len(cmc_preserve_final['m0_MSUN'])+len(cmc_preserve_final['m1_MSUN'])))        
        # print('least massive initial binary: ', min(min(test['m0_MSUN']), min(test['m1_MSUN'])))
        # print('least massive final binary: ', min(min(cmc_preserve_final['m0_MSUN']), min(cmc_preserve_final['m1_MSUN'])))
        
        # # positions of MS binaries
        # test_r = [i*2 for i in test['r']]
        # cmc_r = [i*2 for i in cmc_preserve_final['r']]
        # plt.hist(test_r,  bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, label='Initial', histtype='step')
        # plt.hist(cmc_r, bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, label='Final', histtype='step')
        # plt.axvline(x=0.5942561, c='#1f77b4')
        # plt.axvline(x=2.437094932055888, c='#ff7f0e')
        # plt.legend(loc='upper left')
        # plt.xscale('log')
        # #plt.yscale('log')
        # plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
        # plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
        # plt.rcParams['savefig.bbox'] = 'tight'
        # plt.rcParams.update({'font.size': 18})
        # plt.title('CMC rv2')
        # plt.xlabel('Clustercentric radial position [pc]')
        # plt.ylabel('Fraction of MS binaries')
        # plt.savefig('positionMSfixmet.png')
# UNCOMMENT ABOVE FOR ORIGINAL CODE
        #ids_that_are_in_cmc_but_not_cosmic = [x for x in cosmic_preserved_ids if x not in cosmic_present.index]
        #ids_that_are_in_cmc_but_not_cosmic_cmc_format = [x + 1 for x in ids_that_are_in_cmc_but_not_cosmic]
        #print ("ids that are in cmc but not in cosmic (in cmc ids)", ids_that_are_in_cmc_but_not_cosmic_cmc_format)
        #rows_that_are_in_cmc_but_not_cosmic = preserved_cmc.loc[preserved_cmc['id'].isin(ids_that_are_in_cmc_but_not_cosmic_cmc_format)]
        #print ("rows that are in cmc but not in cosmic (CMC BEGIN)")
        #print (cmc20_init.loc[cmc20_init['id'].isin(ids_that_are_in_cmc_but_not_cosmic_cmc_format)].filter(items=["m0_MSUN", "m1_MSUN", "bin_startype0", "bin_startype1", "id"]))

       # print ("rows that are in cmc but not in cosmic (CMC END)")
       # print (rows_that_are_in_cmc_but_not_cosmic.filter(items=["m0_MSUN", "m1_MSUN", "bin_startype0", "bin_startype1", "id"]))
       # print ("rows that are in CMC but not in cosmic (cosmic start)")
       # print (cosmic_init.filter(items=ids_that_are_in_cmc_but_not_cosmic, axis=0).filter(items=["mass_1", "mass_2", "kstar_1", "kstar_2"]))
       # print ("rows that are in CMC but not in cosmic (cosmic end)")
       # print (cosmic_present.filter(items=ids_that_are_in_cmc_but_not_cosmic, axis=0).filter(items=["mass_1", "mass_2", "kstar_1", "kstar_2"]))
       # print ("preserved cosmic length", len(preserved_cosmic))
       # filtered_preserved_cmc = preserved_cmc.loc[~cmc20_present['id'].isin(ids_that_are_in_cmc_but_not_cosmic_cmc_format)]
       # print('filtered preserved cmc', filtered_preserved_cmc)
       # 


        # get the seps for each mass bin
        # < 1 solar masses, 1 < x < 5 solar masses, > 5 solar masses
        # cmcless_1_ids, cmcless_1, cmcbetween_1_5_ids, cmcbetween_1_5, cmcgreater_5_ids, cmcgreater_5 = mass_bins(filtered_preserved_cmc)
        # cosmicless_1_ids, cosmicless_1, cosmicbetween_1_5_ids, cosmicbetween_1_5, cosmicgreater_5_ids, cosmicgreater_5 = mass_bins(preserved_cosmic, cmc=False)
        # print ("len of > 5 solar mass cosmic", len(cosmicgreater_5))
        # print("len of > 5 solar mass cmc", len(cmcgreater_5))
        # print ("len of 1<x<5 solar mass cosmic", len(cosmicbetween_1_5))
        # print ("len of 1<x<5 solar mass cmc", len(cmcbetween_1_5))
        # print("len of < 1 solar mass cosmic", len(cosmicless_1))
        # print("len of < 1 solar mass cmc", len(cmcless_1))
        # print("Avg sep of 1<x<5 solar mass cosmic", sum(cosmicbetween_1_5)/len(cosmicbetween_1_5))
        # print("Avg sep of 1<x<5 solar mass cmc", sum(cmcbetween_1_5)/len(cmcbetween_1_5))
        # print("Avg sep of <1 solar mass cosmic", sum(cosmicless_1)/len(cosmicless_1))
        # print("Avg sep of <1 solar mass cmc", sum(cmcless_1)/len(cmcless_1))
        # #print("Avg sep of >5 solar mass cosmic", sum(cosmicgreater_5)/len(cosmicgreater_5))
        # #print("Avg sep of >5 solar mass cmc", sum(cmcgreater_5)/len(cmcgreater_5))
        # 
        # # see what CMC binaries are that have IDs in COSMIC that ends up with 1-5 solar masses
        # print('cosmicbetween_1_5_ids', cosmicbetween_1_5_ids)
        # print('cmcbetween_1_5_ids', cmcbetween_1_5_ids)
        # cmc_with_cosmic15 = preserved_cmc.loc[preserved_cmc['id'].isin([i+1 for i in cosmicbetween_1_5_ids])]['a_AU']
        # print('cmc_with_cosmic15', cmc_with_cosmic15)
        # plt.hist(cmc_with_cosmic15, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='CMC rv2 with COSMIC IDs >1 sol mass', histtype='step')
        # plt.hist(cosmicbetween_1_5, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='COSMIC >1 solar mass', histtype = 'step')
        # #plt.hist(cmcbetween_1_5, bins=np.linspace(0, 1, 100), label='CMC rv2 1<x<5 solar mass', histtype='step')
        # #plt.hist(cmcless_1, bins=np.linspace(0, 1, 100), label='CMC rv2 <1 solar mass', histtype='step')
        # #plt.hist(cosmicbetween_1_5, bins=np.linspace(0, 1, 100), label='COSMIC 1<x<5 solar mass', histtype = 'step')
        # #plt.hist(cosmicless_1, bins=np.linspace(0, 1, 100), label='COSMIC <1 solar mass', histtype = 'step')
        # #plt.xlim(0, 1)
        # plt.legend()
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.xlabel('Semimajor Axis [AU]')
        # plt.ylabel('Number of primordial binaries')
        # plt.savefig('btwn15ids.png')
        # plt.clf()

        # # now plot CMC binaries that end up > 1 solar mass and corresponding COSMIC binaries
        # cosmic_with_cmc15 = cosmic_present.filter(items=cmcbetween_1_5_ids, axis=0).filter(items=["sep"])['sep']
        # print('cosmic_with_cmc15', cosmic_with_cmc15)
        # cosmic_with_cmc15 = [i/215.032 for i in cosmic_with_cmc15]
        # plt.hist(cmcbetween_1_5, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='CMC >1 solar mass', histtype='step')
        # plt.hist(cosmic_with_cmc15, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='COSMIC with CMC rv2 IDs >1 sol mass', histtype='step')
        # plt.legend()
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.xlabel('Semimajor Axis [AU]')
        # plt.ylabel('Number of primordial binaries')
        # plt.savefig('btwn15ids2.png')
        # plt.clf()

        # # all binaries that end up with >1 solar masses
        # plt.hist(cmcbetween_1_5, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='CMC rv2 >1 solar mass', histtype='step')
        # plt.hist(cosmicbetween_1_5, bins=np.logspace(np.log10(0.001), np.log10(10), 100), label='COSMIC >1 solar mass', histtype = 'step')
        # plt.legend()
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.xlabel('Semimajor Axis [AU]')
        # plt.ylabel('Number of primordial binaries')
        # plt.savefig('massbinneda.png')
        # plt.clf()

        # # all primordial binaries
        # seps_for_preserved_cmc = filtered_preserved_cmc['a_AU']
        # seps_for_preserved_cmc = [i for i in seps_for_preserved_cmc]
        # seps_for_preserved_cosmic = preserved_cosmic['sep']
        # #seps_for_preserved_cosmic = seps_for_preserved_cosmic/215.032
        # seps_for_preserved_cosmic = [x / 215.032 for x in seps_for_preserved_cosmic]
        # print ("len of cosmic", len(seps_for_preserved_cosmic))
        # print ("len of cmc", len(seps_for_preserved_cmc))

        # print ("Avg sep of cmc", sum(seps_for_preserved_cmc) / len(seps_for_preserved_cmc))
        # print ("Avg sep of cosmic", sum(seps_for_preserved_cosmic) / len(seps_for_preserved_cosmic))
        # 
        # plt.hist(seps_for_preserved_cmc, bins=np.logspace(np.log10(0.0001), np.log10(10), 100), label='CMC rv2',  histtype='step')
        # plt.hist(seps_for_preserved_cosmic, bins=np.logspace(np.log10(0.0001), np.log10(10), 100), label='COSMIC', histtype='step')
        # #plt.xlim(0, 1)
        # plt.legend()
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.xlabel('Semimajor Axis [AU]')
        # plt.ylabel('Number of primordial binaries')
        # plt.savefig('test_seps.png')
        # plt.clf()
        # 
        # mass1_for_preserved_cmc = filtered_preserved_cmc['m0_MSUN']
        # mass2_for_preserved_cmc = filtered_preserved_cmc['m1_MSUN']
        # mass1_for_preserved_cosmic = preserved_cosmic['mass_1']
        # mass2_for_preserved_cosmic = preserved_cosmic['mass_2']
        # plt.hist(mass1_for_preserved_cmc, bins=np.logspace(np.log10(0.001), np.log10(5), 100), label='CMC rv2 mass1', histtype='step')
        # plt.hist(mass2_for_preserved_cmc, bins=np.logspace(np.log10(0.001), np.log10(5), 100), label='CMC rv2 mass2', histtype='step')
        # plt.hist(mass1_for_preserved_cosmic, bins=np.logspace(np.log10(0.001), np.log10(5), 100), label='COSMIC mass1', histtype='step')
        # plt.hist(mass2_for_preserved_cosmic, bins=np.logspace(np.log10(0.001), np.log10(5), 100), label='COSMIC mass2', histtype='step')
        # plt.xlabel('Masses [M_sun]')
        # plt.ylabel('Number of primordial binaries')
        # plt.legend()
        # plt.xscale('log')
        # plt.yscale('log')
        # #plt.xlim(0, 5)
        # plt.savefig('primmasses.png')

        ################ preserved binaries that are not the identical MS stars ########################
        # preserved_cosmic_nonms = preserved_cosmic[~(((preserved_cosmic['kstar_1'] == 1.0) | (preserved_cosmic['kstar_1'] == 0.0)) & ((preserved_cosmic['kstar_2'] == 1.0) | (preserved_cosmic['kstar_2'] == 0.0)) & (preserved_cosmic['sep'] > 0))]
        # preserved_cmc_nonms = preserved_cmc[~(((preserved_cmc['bin_startype0'] == 1.0) | (preserved_cmc['bin_startype0'] == 0.0)) & ((preserved_cmc['bin_startype1'] == 1.0) | (preserved_cmc['bin_startype1'] == 0.0)) & (preserved_cmc['a_AU'] > 0))]
        # # cosmic_common_ids = [map_CMC_to_COSMIC_id(i) for i in common_ids]
        # # preserved_cosmic_nonms =  preserved.cosmic.loc[~preserved_cosmic_nonms.isin(cosmic_common_ids)]
        # # preserved_cmc_nonms = preserved_cmc.loc[~preserved_cmc['id'].isin(common_ids)]
        # print('len COSMIC nonms', len(preserved_cosmic_nonms))
        # present_cosmic_counts(preserved_cosmic_nonms)
        # print('len CMC nonms', len(preserved_cmc_nonms))
        # present_cmc_counts(preserved_cmc_nonms)
        # ####### track a WD single produced in COSMIC and not CMC ########################
        # # find what IDs the WD singles are
        # wdsinglecosmicids = get_ids_with_condition(preserved_cosmic_nonms, (preserved_cosmic_nonms['tphys'] > 0) & ((((preserved_cosmic_nonms['kstar_1'] == 10.0) | (preserved_cosmic_nonms['kstar_1'] == 11.0) | (preserved_cosmic_nonms['kstar_1'] == 12.0)) & (preserved_cosmic_nonms['kstar_2'] == 15.0)) | ((preserved_cosmic_nonms['kstar_1'] == 15.0) & ((preserved_cosmic_nonms['kstar_2'] == 10.0) | (preserved_cosmic_nonms['kstar_2'] == 11.0) | (preserved_cosmic_nonms['kstar_2'] == 12.0)))))
        # print('wd single cosmic ids', wdsinglecosmicids)
        # wdsinglecmcids = [map_COSMIC_to_CMC_id(i) for i in wdsinglecosmicids]
        # # print bpp of 3 of the IDs
        # for ind in wdsinglecosmicids:
        #         print('wd single ind', ind)
        #         print(bpp.loc[ind][['tphys', 'mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'porb', 'ecc', 'evol_type']])
        # # plot where all of these not singles in CMC 
        # cmc_missed_singles = preserved_cmc_nonms.loc[preserved_cmc_nonms['id'].isin(wdsinglecmcids)]
        # cmc_missed_r = [i*2 for i in cmc_missed_singles['r']]
        # plt.hist(cmc_missed_r, bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, histtype='step')
        # plt.axvline(x=2.437094932055888, c='#1f77b4')
        # plt.xscale('log')
        # plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
        # plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
        # plt.rcParams['savefig.bbox'] = 'tight'
        # plt.rcParams.update({'font.size': 18})
        # plt.title('CMC rv2 binaries that did not become singles')
        # plt.xlabel('Clustercentric radial position [pc]')
        # plt.ylabel('Fraction of MS binaries')
        # plt.savefig('rv2positionsofpreservednonMS.png')
        # plt.clf()
        # ####################### track the 15-15s in COSMIC #########################
        # masslesscosmicids = get_ids_with_condition(preserved_cosmic_nonms, (preserved_cosmic_nonms['tphys'] > 0) & (preserved_cosmic_nonms['kstar_1'] == 15.0) & (preserved_cosmic_nonms['kstar_2'] == 15.0))
        # masslesscmcids = [map_COSMIC_to_CMC_id(i) for i in masslesscosmicids]
        # for ind in masslesscosmicids:
        #         print('massless ind', ind)
        #         print(bpp.loc[ind][['tphys', 'mass_1', 'mass_2', 'kstar_1', 'kstar_2', 'sep', 'porb', 'ecc', 'evol_type']])
        # cmc_massless = preserved_cmc_nonms.loc[preserved_cmc_nonms['id'].isin(masslesscmcids)]
        # cmc_massless_r = [i*2 for i in cmc_massless['r']]
        # plt.hist(cmc_massless_r, bins=np.logspace(np.log10(0.05), np.log10(100), 100), cumulative=True, density=True, histtype='step')
        # plt.axvline(x=2.437094932055888, c='#1f77b4')
        # plt.xscale('log')
        # plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
        # plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
        # plt.rcParams['savefig.bbox'] = 'tight'
        # plt.rcParams.update({'font.size': 18})
        # plt.title('CMC rv2 binaries that did not become massless')
        # plt.xlabel('Clustercentric radial position [pc]')
        # plt.ylabel('Fraction of MS binaries')
        # plt.savefig('rv2positionsofpreservednonMSmassless.png')
        # plt.clf()
#        # plot semimajor axis distribution of all the remaining preserved binaries CMC vs. COSMIC and where they are in CMC
#         remainpreservedcosmicids = get_ids_with_condition(preserved_cosmic_nonms, (preserved_cosmic_nonms['tphys'] > 0) & (preserved_cosmic_nonms['kstar_1'] != 15.0) & (preserved_cosmic_nonms['kstar_2'] != 15.0) & (preserved_cosmic_nonms['sep'] != -1.000000))
#         remainpreservedcmcids = [map_COSMIC_to_CMC_id(i) for i in remainpreservedcosmicids]
#         remain_cosmic_a = []
#         for ind in remainpreservedcosmicids:
#                 remain_cosmic_a.append(preserved_cosmic_nonms.loc[ind]['sep']/215.032)
#         remain_cmc = preserved_cmc_nonms.loc[preserved_cmc_nonms['id'].isin(remainpreservedcmcids)]
#         remain_cmc_a = remain_cmc['a_AU']
#         plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
#         plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
#         plt.rcParams['savefig.bbox'] = 'tight'
#         plt.rcParams.update({'font.size': 18})
#         print('len cmc', len(remain_cmc_a))
#         print('len cosmic', len(remain_cosmic_a))
#         plt.hist(remain_cmc_a, bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='CMC rv2 Final',  histtype='step')
#         plt.hist(remain_cosmic_a, bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='COSMIC Final',  histtype='step')
#         plt.xscale('log')
#         plt.xlabel('Semimajor Axis [AU]')
#         plt.ylabel('Number of binaries')
#         plt.legend(fontsize=15)
#         plt.savefig('preservedbinariesnonMS.png')
#         plt.clf()
        ################################### GET COUNTS OF EVERYTHING ################################################################
        ############################### preserved IDs redo ############################################
        # get list of present CMC IDs
        list_of_cmc_ids = list(cmc20_present['id'])
        # list_of_cmc_ids2 = list(cmc20_present['id0'])
        # list_of_cmc_ids3 = list(cmc20_present['id1'])
        # get dataframe of present COSMIC IDs, which comes from bin_num column
        preserved_cosmic = cosmic_present.filter(['tphys', 'bin_num', 'kstar_1', 'kstar_2', 'sep', 'mass_1', 'mass_2', 'bin_state', 'merger_type'])
        # convert the COSMIC ID column to the corresponding CMC IDs
        preserved_cosmic['bin_num'] += 1
        preserved_cosmic['preserved_bool'] = (preserved_cosmic['bin_num'].isin(list_of_cmc_ids)) #| (preserved_cosmic['bin_num'].isin(list_of_cmc_ids2)) | (preserved_cosmic['bin_num'].isin(list_of_cmc_ids3))
        # filter data frame to only have the population of present COSMIC IDs in CMC present day
        preserved_cosmic = preserved_cosmic[preserved_cosmic['preserved_bool'] == True]
        common_ids = list(preserved_cosmic['bin_num'])
        print('len common ids', len(common_ids))
        # get the filtered preserved CMC present day objects
        preserved_cmc = cmc20_present.filter(['id', 'startype', 'bin_startype0', 'bin_startype1', 'a_AU', 'm0_MSUN', 'm1_MSUN', 'm_MSUN', 'r'])
        preserved_cmc['preserved_bool'] = preserved_cmc['id'].isin(common_ids)
        preserved_cmc = preserved_cmc[preserved_cmc['preserved_bool'] == True]
        ###################### MS Binaries only ############################
        preserved_cmc_ms = preserved_cmc[((preserved_cmc['bin_startype0'] == 1.0) | (preserved_cmc['bin_startype0'] == 0.0)) & ((preserved_cmc['bin_startype1'] == 1.0) | (preserved_cmc['bin_startype1'] == 0.0)) & (preserved_cmc['a_AU'] > 0)]
        print('# of MS CMC', len(preserved_cmc_ms))
        preserved_cosmic_ms = preserved_cosmic[((preserved_cosmic['kstar_1'] == 1.0) | (preserved_cosmic['kstar_1'] == 0.0)) & ((preserved_cosmic['kstar_2'] == 1.0) | (preserved_cosmic['kstar_2'] == 0.0)) & (preserved_cosmic['sep'] > 0)]
        print('# of MS COSMIC', len(preserved_cosmic_ms))
        common_ids = find_common_ids(preserved_cmc_ms['id'], preserved_cosmic_ms['bin_num'])
        print('# common ids', len(common_ids))
        cmc_preserve_final = preserved_cmc_ms[preserved_cmc_ms['id'].isin(common_ids)]
        cosmic_preserve_final = preserved_cosmic_ms[preserved_cosmic_ms['bin_num'].isin(common_ids)]
        print('# of MS CMC', len(cmc_preserve_final))
        print('# of MS COSMIC', len(cosmic_preserve_final))
        ###################### Everything else #############################
        preserved_cosmic_nonms = preserved_cosmic[~preserved_cosmic['bin_num'].isin(common_ids)]
        preserved_cmc_nonms = preserved_cmc[~preserved_cmc['id'].isin(common_ids)]
        print('# nonMS CMC', len(preserved_cmc_nonms))
        present_cmc_counts(preserved_cmc_nonms)
        print('# nonMS COSMIC', len(preserved_cosmic_nonms))
        present_cosmic_counts(preserved_cosmic_nonms)
        ###################### nonpreserved IDs in COSMIC present but not in CMC present #############################
        # print('diff', set(cosmic_init.index)-set(cosmic_present.index)) # six binaries only got run to a few hundred Myr--too little to care about rn
        # get dataframe of present COSMIC IDs, which comes from bin_num column
        nonpreserved_ids = cosmic_present.filter(['tphys', 'bin_num', 'kstar_1', 'kstar_2', 'sep', 'mass_1', 'mass_2', 'bin_state', 'merger_type'])
        # convert the COSMIC ID column to the corresponding CMC IDs
        nonpreserved_ids['bin_num'] += 1
        # create a new boolean column that checks whether or not the present day COSMIC IDs exist in present day CMC
        nonpreserved_ids['nonpreserved_bool'] =  ~nonpreserved_ids['bin_num'].isin(list_of_cmc_ids) #| nonpreserved_ids.isin(list_of_cmc_ids2) | nonpreserved_ids.isin(list_of_cmc_ids3)) 
        # get the lists of IDs in CMC affected by collisions or escapers
        id1col, id2col, id3col, id4col = read_collision_file('king.collision.log')
        id11col, id22col, id33col, id44col = read_collision_file('kingres1.collision.log')
        id1esc, id2esc, id0esc = read_escape_file('king.esc.dat')
        id11esc, id22esc, id00esc = read_escape_file('kingres1.esc.dat')
        id1merge, id2merge, id1dis, id2dis, kstar1merge, kstar2merge = read_semergedisrupt_file('king.semergedisrupt.log')
        id11merge, id22merge, id11dis, id22dis, kstar11merge, kstar22merge = read_semergedisrupt_file('kingres1.semergedisrupt.log')

        # METHOD 1
        union_of_ids = list(set().union(id1col, id2col, id3col, id4col, id11col, id22col, id33col, id44col, id1esc, \
        id2esc, id0esc, id11esc, id22esc, id00esc, id1merge, id2merge, id1dis, id2dis, id11merge, id22merge, id11dis, id22dis))
        # union_of_ids = id1col + id2col + id3col + id4col + id11col + id22col + id33col + id44col + id1esc + \
        # id2esc + id0esc + id11esc + id22esc + id00esc + id1merge + id2merge + id1dis + id2dis + id11merge + id22merge + id11dis + id22dis
        union_of_esc = list(set().union(id1esc, id2esc, id0esc, id11esc, id22esc, id00esc))
        union_of_col = list(set().union(id1col, id2col, id3col, id4col, id11col, id22col, id33col, id44col))
        union_of_dis = list(set().union(id1dis, id2dis, id11dis, id22dis))
        union_of_merge = list(set().union(id1merge, id2merge, id11merge, id22merge))
        print('overall')
        count_ids_in_cosmic_not_cmc(union_of_ids, nonpreserved_ids)
        print('escape')
        count_ids_in_cosmic_not_cmc(union_of_esc, nonpreserved_ids)
        print('col')
        count_ids_in_cosmic_not_cmc(union_of_col, nonpreserved_ids)
        print('dis')
        count_ids_in_cosmic_not_cmc(union_of_dis, nonpreserved_ids)
        print('merge')
        count_ids_in_cosmic_not_cmc(union_of_merge, nonpreserved_ids)

        # METHOD 2
        # count the number of present day COSMIC IDs that are not in present day CMC
        overall_count = nonpreserved_ids['nonpreserved_bool'].sum()
        # filter data frame to only have the population of present COSMIC IDs not in CMC present day
        nonpreserved_ids = nonpreserved_ids[nonpreserved_ids['nonpreserved_bool'] == True]
        # check if the above COSMIC IDs that are missing from CMC present day are resulting from collisions or escapers
        nonpreserved_ids['collisions?'] = (nonpreserved_ids['bin_num'].isin(id1col)) | (nonpreserved_ids['bin_num'].isin(id2col)) | \
                (nonpreserved_ids['bin_num'].isin(id11col)) | (nonpreserved_ids['bin_num'].isin(id22col)) | \
                (nonpreserved_ids['bin_num'].isin(id3col)) | (nonpreserved_ids['bin_num'].isin(id4col)) | \
                (nonpreserved_ids['bin_num'].isin(id33col)) | (nonpreserved_ids['bin_num'].isin(id44col))
        collision_count = nonpreserved_ids['collisions?'].sum()
        nonpreserved_ids['escapers?'] = ((nonpreserved_ids['bin_num'].isin(id1esc)) | (nonpreserved_ids['bin_num'].isin(id2esc)) | \
                (nonpreserved_ids['bin_num'].isin(id11esc)) | (nonpreserved_ids['bin_num'].isin(id22esc)) | \
                (nonpreserved_ids['bin_num'].isin(id0esc)) | (nonpreserved_ids['bin_num'].isin(id00esc))) # & (nonpreserved_ids['collisions?'] == False)
        escapers_count = nonpreserved_ids['escapers?'].sum()
        nonpreserved_ids['disrupted?'] = ((nonpreserved_ids['bin_num'].isin(id1dis)) | (nonpreserved_ids['bin_num'].isin(id2dis)) | \
                (nonpreserved_ids['bin_num'].isin(id11dis)) | (nonpreserved_ids['bin_num'].isin(id22dis))) & (nonpreserved_ids['collisions?'] == False) & (nonpreserved_ids['escapers?'] == False)
        disrupted_count = nonpreserved_ids['disrupted?'].sum()
        nonpreserved_ids['merged?'] = ((nonpreserved_ids['bin_num'].isin(id1merge)) | (nonpreserved_ids['bin_num'].isin(id2merge)) | \
                (nonpreserved_ids['bin_num'].isin(id11merge)) | (nonpreserved_ids['bin_num'].isin(id22merge))) & (nonpreserved_ids['collisions?'] == False) & (nonpreserved_ids['escapers?'] == False) & (nonpreserved_ids['collisions?'] == False) & (nonpreserved_ids['disrupted?'] == False)
        merged_count = nonpreserved_ids['merged?'].sum()
        # print all the counts of each condition
        print('overall count', overall_count)
        print('collision count', collision_count)
        print('escapers count', escapers_count)
        print('disrupted count', disrupted_count)
        print('mergers count', merged_count)
        # filter nonpreserved IDs that are not collisions, escapers, disruptions, or mergers and did not end up in CMC present
        nonpreserved_ids['other'] = ~nonpreserved_ids['bin_num'].isin(union_of_ids)
        other_count = nonpreserved_ids['other'].sum()
        print('other count', other_count)
        other_nonpreserved = nonpreserved_ids[nonpreserved_ids['other'] == True]
        print('other nonpreserved IDs', other_nonpreserved['bin_num'])
        # accounting for the IDs that are 0
        zeros_cmc_present = cmc20_present[cmc20_present['id'] == 0]
        print('0 ids', len(zeros_cmc_present))
        list_zeros_id0 = list(zeros_cmc_present['id0'])
        print('id0s', list_zeros_id0)
        list_zeros_id1 = list(zeros_cmc_present['id1'])
        print('id1s', list_zeros_id1)
        other_nonpreserved['foundid'] = (other_nonpreserved['bin_num'].isin(list_zeros_id0)) | (other_nonpreserved['bin_num'].isin(list_zeros_id1))
        foundid_count = other_nonpreserved['foundid'].sum()
        print('found id count', foundid_count)
        # last missing nonpreserved IDs 
        last_ids = other_nonpreserved[other_nonpreserved['foundid'] == False]
        print('example last IDs', last_ids['bin_num'])
        ############################################################################################################################################

        ################################################### ACTUALLY ANALYZE THE DIFFERENT SUBCATEGORIES ##############################################################
      
        ################################### preserved non binary MS stars ###########################################
        ######## look at the BH binaries in COSMIC and not in CMC #################
        # filter correct data
        pres_BH_binaries = preserved_cosmic_nonms[((preserved_cosmic_nonms['kstar_1'] == 14.0) | (preserved_cosmic_nonms['kstar_2'] == 14.0)) & (preserved_cosmic_nonms['kstar_1'] != 15.0) & (preserved_cosmic_nonms['kstar_2'] != 15.0) & (preserved_cosmic_nonms['sep'] != -1.000000)]
        pres_BH_binaries_ids = list(pres_BH_binaries['bin_num'])
        preserved_cmc_nonms['preservedidsnotBHs'] = preserved_cmc_nonms['id'].isin(pres_BH_binaries_ids)
        pres_not_BHs = preserved_cmc_nonms[preserved_cmc_nonms['preservedidsnotBHs'] == True]
        print('pres not BHs', pres_not_BHs)
        merged_not_BHs = pres_not_BHs[(pres_not_BHs['id'].isin(id1merge) | pres_not_BHs['id'].isin(id11merge) | pres_not_BHs['id'].isin(id2merge) | pres_not_BHs['id'].isin(id22merge)) == True]
        disrupted_not_BHs = pres_not_BHs[(pres_not_BHs['id'].isin(id1dis) | pres_not_BHs['id'].isin(id11dis) | pres_not_BHs['id'].isin(id2dis) | pres_not_BHs['id'].isin(id22dis)) == True]
        print('merged not BHs', merged_not_BHs)
        print('disrupted not BHs', disrupted_not_BHs)
        # plot the masses of those COSMIC BHs vs. masses of the corresponding nonBHs in CMC
        cosmic_mass1 = pres_BH_binaries['mass_1']
        cosmic_mass2 = pres_BH_binaries['mass_2']
        cmc_mass = pres_not_BHs['m_MSUN']
        plt.hist(cosmic_mass1, bins=50, histtype='step', color='blue', label='COSMIC mass 1')
        plt.hist(cosmic_mass2, bins=50, histtype='step', color='red', label='COSMIC mass 2')
        plt.hist(cmc_mass, bins=50, histtype='step', color='green', label='CMC mass')
        plt.xlabel('Masses [solar masses]')
        plt.ylabel('Number of objects')
        plt.legend()
        plt.savefig('presbhbinariesmasses.png')
        ######## look at the WD-WDs in COSMIC vs CMC #################
        # compare 15534 CMC WD-WDs with corresponding IDs in COSMIC
        cmc_pres_WD_WD = preserved_cmc_nonms[((preserved_cmc_nonms['bin_startype0'] == 10.0) | (preserved_cmc_nonms['bin_startype0'] == 11.0) | (preserved_cmc_nonms['bin_startype0'] == 12.0)) & ((preserved_cmc_nonms['bin_startype1'] == 10.0) | (preserved_cmc_nonms['bin_startype1'] == 11.0) | (preserved_cmc_nonms['bin_startype1'] == 12.0))]
        cmc_pres_WD_WD_ids = list(cmc_pres_WD_WD['id'])
        preserved_cosmic_nonms['WDWDsinCMC'] = preserved_cosmic_nonms['bin_num'].isin(cmc_pres_WD_WD_ids)
        cosmic_corr_WD_WD = preserved_cosmic_nonms[preserved_cosmic_nonms['WDWDsinCMC'] == True]
        cosmic_remain_bin = cosmic_corr_WD_WD[cosmic_corr_WD_WD['bin_state'] == 0]
        cosmic_corr_merge = cosmic_corr_WD_WD[cosmic_corr_WD_WD['bin_state'] == 1]
        cosmic_corr_dis = cosmic_corr_WD_WD[cosmic_corr_WD_WD['bin_state'] == 2]
        print('cosmic corr', cosmic_corr_WD_WD)
        print('cmc corr', cmc_pres_WD_WD)
        print('cosmic corr bin', len(cosmic_remain_bin))
        print('cosmic corr merge', len(cosmic_corr_merge))
        print('cosmic corr dis', len(cosmic_corr_dis))
        # plot masses of COSMIC vs. CMC 
        cosmic_mass1 = cosmic_corr_WD_WD['mass_1']
        cosmic_mass2 = cosmic_corr_WD_WD['mass_2']
        cmc_mass1 = cmc_pres_WD_WD['m0_MSUN']
        cmc_mass2 = cmc_pres_WD_WD['m1_MSUN']
        # plt.hist(cosmic_mass1, bins=50, histtype='step', color='blue', label='COSMIC mass 1')
        # plt.hist(cosmic_mass2, bins=50, histtype='step', color='red', label='COSMIC mass 2')
        # plt.hist(cmc_mass1, bins=50, histtype='step', color='green', label='CMC mass 1')
        # plt.hist(cmc_mass2, bins=50, histtype='step', color='orange', label='CMC mass 2')
        # plt.xlabel('Masses [solar masses]')
        # plt.ylabel('Number of objects')
        # plt.legend()
        # plt.savefig('presCMCWDWDmasses.png')
        # plt.clf()
        # # plot kstars of COSMIC
        # plt.hist(cosmic_corr_WD_WD['kstar_1'],  bins=20, histtype='step', color='blue', label='COSMIC kstar 1')
        # plt.hist(cosmic_corr_WD_WD['kstar_2'],  bins=20, histtype='step', color='red', label='COSMIC kstar 2')
        # plt.xlabel('kstars')
        # plt.ylabel('Number of objects')
        # plt.legend()
        # plt.savefig('presCMCWDWDkstars.png')
        # plt.clf()
        # # compare 15534 CMC WD-WDs with 1395 COSMIC WD-WDs
        # # masses
        # cosmic_pres_WD_WD = preserved_cosmic_nonms[(((preserved_cosmic_nonms['kstar_1'] == 10.0) | (preserved_cosmic_nonms['kstar_1'] == 11.0) | (preserved_cosmic_nonms['kstar_1'] == 12.0)) & ((preserved_cosmic_nonms['kstar_2'] == 10.0) | (preserved_cosmic_nonms['kstar_2'] == 11.0) | (preserved_cosmic_nonms['kstar_2'] == 12.0))) & (preserved_cosmic_nonms['sep'] != -1.000000)]
        # plt.hist(cmc_pres_WD_WD['m0_MSUN'], bins=20, histtype='step', color='blue', label='CMC mass 1')
        # plt.hist(cmc_pres_WD_WD['m1_MSUN'], bins=20, histtype='step', color='red', label='CMC mass 2')
        # plt.hist(cosmic_pres_WD_WD['mass_1'], bins=20, histtype='step', color='green', label='COSMIC mass 1')
        # plt.hist(cosmic_pres_WD_WD['mass_2'], bins=20, histtype='step', color='orange', label='COSMIC mass 2')
        # plt.xlabel('WD masses [solar masses]')
        # plt.ylabel('Number of objects')
        # plt.legend()
        # plt.savefig('presWDWDsmasses.png')
        # plt.clf()
        # # semimajor axes
        # plt.hist(cmc_pres_WD_WD['a_AU'], bins=np.logspace(np.log10(0.001), np.log10(20), 100), histtype='step', color='blue', label='CMC')
        # plt.hist([i/215.032 for i in cosmic_pres_WD_WD['sep']], bins=np.logspace(np.log10(0.001), np.log10(20), 100), histtype='step', color='red', label='COSMIC')
        # plt.xlabel('Semimajor axes [AU]')
        # plt.ylabel('Number of objects')
        # plt.xscale('log')
        # plt.legend()
        # plt.savefig('presWDWDsa.png')
        # plt.clf()
        # # where are the CMC IDs?
        # plt.hist(cmc_pres_WD_WD['r'], bins=np.logspace(np.log10(0.05), np.log10(30), 100), cumulative=True, density=True, color='blue', histtype='step')
        # plt.xlabel('Clustercentric radial position [pc]')
        # plt.ylabel('Fraction of WD-WDs')
        # plt.axvline(x=2.437, c='blue')
        # plt.savefig('positionWDWDs.png')
        # plt.clf()


        # ########### preserved mergers vs. disruptions CMC vs. COSMIC #################
        # # for COSMIC, filter for all the singles, double massless remnants, 2 singles
        # cosmic_singles_massless = preserved_cosmic_nonms[((preserved_cosmic_nonms['kstar_1'] == 15.0) ^ (preserved_cosmic_nonms['kstar_2'] == 15.0)) | ((preserved_cosmic_nonms['kstar_1'] == 15.0) & (preserved_cosmic_nonms['kstar_2'] == 15.0)) | ((preserved_cosmic_nonms['kstar_1'] != 15.0) & (preserved_cosmic_nonms['kstar_2'] != 15.0) & (preserved_cosmic_nonms['sep'] == -1.000000))]
        # remaining_binary = cosmic_singles_massless[cosmic_singles_massless['bin_state'] == 0]
        # binaries_that_merged = cosmic_singles_massless[cosmic_singles_massless['bin_state'] == 1]
        # binaries_that_disrupted = cosmic_singles_massless[cosmic_singles_massless['bin_state'] == 2]
        # print('cosmic singles massless', cosmic_singles_massless)
        # print('remaining binary', remaining_binary)
        # print('merged', binaries_that_merged)
        # print('disrupted', binaries_that_disrupted)
        # # get types of COSMIC mergers and parse it
        # print('merger type', binaries_that_merged['merger_type'])
        # binaries_that_merged['merger_type'].astype('int')
        # binaries_that_merged['merger_kstar1'] = binaries_that_merged['merger_type'].astype('int') // 100
        # binaries_that_merged['merger_kstar2'] = binaries_that_merged['merger_type'].astype('int') % 100
        # print('binaries that merged', binaries_that_merged)
        # # get counts of BH-BH mergers, BH-NS mergers, BH-WD mergers, BH-noncompact, NS-NS mergers, NS-WD mergers, NS-noncompact, WD-WD, WD-noncompact, noncompact 
        # binaries_that_merged['bhbhmerge'] = binaries_that_merged['merger_kstar1'].isin([14]) & binaries_that_merged['merger_kstar2'].isin([14])
        # bhbhmerge = binaries_that_merged[binaries_that_merged['bhbhmerge'] == True]
        # print('len bhbhmerge', len(bhbhmerge))
        # print('bhbhmerge', bhbhmerge)
        # binaries_that_merged['bhnsmerge'] = (binaries_that_merged['merger_kstar1'].isin([14]) & binaries_that_merged['merger_kstar2'].isin([13])) | (binaries_that_merged['merger_kstar1'].isin([13]) & binaries_that_merged['merger_kstar2'].isin([14])) 
        # bhnsmerge = binaries_that_merged[binaries_that_merged['bhnsmerge'] == True]
        # print('len bhnsmerge', len(bhnsmerge))
        # binaries_that_merged['bhwdmerge'] = (binaries_that_merged['merger_kstar1'].isin([14]) & binaries_that_merged['merger_kstar2'].isin([10, 11, 12])) | (binaries_that_merged['merger_kstar1'].isin([10, 11, 12]) & binaries_that_merged['merger_kstar2'].isin([14]))
        # bhwdmerge = binaries_that_merged[binaries_that_merged['bhwdmerge'] == True]
        # print('len bhwdmerge', len(bhwdmerge))
        # binaries_that_merged['bhnoncompmerge'] = (binaries_that_merged['merger_kstar1'].isin([14]) & binaries_that_merged['merger_kstar2'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) | (binaries_that_merged['merger_kstar1'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & binaries_that_merged['merger_kstar2'].isin([14]))
        # bhnoncompmerge = binaries_that_merged[binaries_that_merged['bhnoncompmerge'] == True]
        # print('len bhnoncompmerge', len(bhnoncompmerge))
        # binaries_that_merged['nsnsmerge'] = binaries_that_merged['merger_kstar1'].isin([13]) & binaries_that_merged['merger_kstar2'].isin([13]) 
        # nsnsmerge = binaries_that_merged[binaries_that_merged['nsnsmerge'] == True]
        # print('len nsnsmerge', len(nsnsmerge))
        # binaries_that_merged['nswdmerge'] = (binaries_that_merged['merger_kstar1'].isin([13]) & binaries_that_merged['merger_kstar2'].isin([10, 11, 12])) | (binaries_that_merged['merger_kstar1'].isin([10, 11, 12]) & binaries_that_merged['merger_kstar2'].isin([13]))
        # nswdmerge = binaries_that_merged[binaries_that_merged['nswdmerge'] == True]
        # print('len nswdmerge', len(nswdmerge))
        # binaries_that_merged['nsnoncompmerge'] = (binaries_that_merged['merger_kstar1'].isin([13]) & binaries_that_merged['merger_kstar2'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) | (binaries_that_merged['merger_kstar1'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & binaries_that_merged['merger_kstar2'].isin([13]))
        # nsnoncompmerge = binaries_that_merged[binaries_that_merged['nsnoncompmerge'] == True]
        # print('len nsnoncompmerge', len(nsnoncompmerge))
        # binaries_that_merged['wdwdmerge'] = binaries_that_merged['merger_kstar1'].isin([10, 11, 12]) & binaries_that_merged['merger_kstar2'].isin([10, 11, 12])
        # wdwdmerge = binaries_that_merged[binaries_that_merged['wdwdmerge'] == True]
        # print('len wdwdmerge', len(wdwdmerge))
        # binaries_that_merged['wdnoncompmerge'] = (binaries_that_merged['merger_kstar1'].isin([10, 11, 12]) & binaries_that_merged['merger_kstar2'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) | (binaries_that_merged['merger_kstar1'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & binaries_that_merged['merger_kstar2'].isin([10, 11, 12]))
        # wdnoncompmerge = binaries_that_merged[binaries_that_merged['wdnoncompmerge'] == True]
        # print('len wdnoncompmerge', len(wdnoncompmerge))
        # binaries_that_merged['noncompnoncompmerge'] = binaries_that_merged['merger_kstar1'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & binaries_that_merged['merger_kstar2'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) 
        # noncompnoncompmerge = binaries_that_merged[binaries_that_merged['noncompnoncompmerge'] == True]
        # print('len noncompnoncompmerge', len(noncompnoncompmerge))

        # # for CMC, filter for all the singles
        # cmc_singles = preserved_cmc_nonms[(preserved_cmc_nonms['startype'] >= 0.0) & (preserved_cmc_nonms['startype'] <= 15.0)]
        # print('cmc singles', len(cmc_singles))
        # # check those IDs in the semergedisrupt.log file and see if they went through disruptboth (disruption) or disrupt1/disrupt2 (merger)
        # merged_cmc_singles = cmc_singles[(cmc_singles['id'].isin(id1merge) | cmc_singles['id'].isin(id11merge) | cmc_singles['id'].isin(id2merge) | cmc_singles['id'].isin(id22merge)) == True]
        # print('length of cmc merged', len(merged_cmc_singles))
        # disrupted_cmc_singles = cmc_singles[cmc_singles['id'].isin(id1dis) | cmc_singles['id'].isin(id11dis) | cmc_singles['id'].isin(id2dis) | cmc_singles['id'].isin(id22dis)]
        # print('length of cmc disrupted', len(disrupted_cmc_singles))
        # collision_cmc_singles = cmc_singles[cmc_singles['id'].isin(id1col) | cmc_singles['id'].isin(id2col) | cmc_singles['id'].isin(id11col) | cmc_singles['id'].isin(id22col) | cmc_singles['id'].isin(id3col) | cmc_singles['id'].isin(id33col) | cmc_singles['id'].isin(id4col) | cmc_singles['id'].isin(id4col)]
        # print('length of cmc collisions', len(collision_cmc_singles))
        # neither_cmc_singles = cmc_singles[~(cmc_singles['id'].isin(id1merge) | cmc_singles['id'].isin(id11merge) | cmc_singles['id'].isin(id2merge) | cmc_singles['id'].isin(id22merge) | cmc_singles['id'].isin(id1dis) | cmc_singles['id'].isin(id11dis) | cmc_singles['id'].isin(id2dis) | cmc_singles['id'].isin(id22dis) | cmc_singles['id'].isin(id1col) \
        # | cmc_singles['id'].isin(id2col) | cmc_singles['id'].isin(id11col) | cmc_singles['id'].isin(id22col) | cmc_singles['id'].isin(id3col) | cmc_singles['id'].isin(id33col) | cmc_singles['id'].isin(id4col) | cmc_singles['id'].isin(id44col))]
        # print('none cmc singles', neither_cmc_singles)
        # print('length of none', len(neither_cmc_singles))

        # # get kstars of the mergers, get counts of BH-BH mergers, BH-NS mergers, BH-WD mergers, BH-noncompact, NS-NS mergers, NS-WD mergers, NS-noncompact, WD-WD, WD-noncompact, noncompact 
        # # create a dictionary mapping ID in all the merged IDs to kstars
        # merged_info = {}
        # for i in range(len(id1merge)):
        #         merged_info[id1merge[i]] = [kstar1merge[i], kstar2merge[i]]
        # for i in range(len(id11merge)):
        #         merged_info[id11merge[i]] = [kstar11merge[i], kstar22merge[i]]
        # for i in range(len(id2merge)):
        #         merged_info[id2merge[i]] = [kstar1merge[i], kstar2merge[i]]
        # for i in range(len(id22merge)):
        #         merged_info[id22merge[i]] = [kstar11merge[i], kstar22merge[i]] 
        # # for each ID in merged_cmc_singles, get the corresponding kstars for the merge
        # merged_cmc_singles['kstarsmerge'] = merged_cmc_singles['id'].map(merged_info)
        # merged_cmc_singles[['kstar1merge', 'kstar2merge']] = pd.DataFrame(merged_cmc_singles.kstarsmerge.tolist(), index=merged_cmc_singles.index)
        # # print('merged cmc singles', merged_cmc_singles)
        # print('len merged cmc singles', len(merged_cmc_singles))
        # # create dataframe with new new kstars
        # merged_cmc_singles['bhbhmerge'] = merged_cmc_singles['kstar1merge'].isin([14]) & merged_cmc_singles['kstar2merge'].isin([14])
        # bhbhmerge = merged_cmc_singles[merged_cmc_singles['bhbhmerge'] == True]
        # print('len bhbhmerge', len(bhbhmerge))
        # merged_cmc_singles['bhnsmerge'] = (merged_cmc_singles['kstar1merge'].isin([14]) & merged_cmc_singles['kstar2merge'].isin([13])) | (merged_cmc_singles['kstar1merge'].isin([13]) & merged_cmc_singles['kstar2merge'].isin([14]))
        # bhnsmerge = merged_cmc_singles[merged_cmc_singles['bhnsmerge'] == True]
        # print('len bhnsmerge', len(bhnsmerge))
        # merged_cmc_singles['bhwdmerge'] = (merged_cmc_singles['kstar1merge'].isin([14]) & merged_cmc_singles['kstar2merge'].isin([10, 11, 12])) | (merged_cmc_singles['kstar1merge'].isin([10, 11, 12]) & merged_cmc_singles['kstar2merge'].isin([14]))
        # bhwdmerge = merged_cmc_singles[merged_cmc_singles['bhwdmerge'] == True]
        # print('len bhwdmerge', len(bhwdmerge))
        # merged_cmc_singles['bhnoncompmerge'] = (merged_cmc_singles['kstar1merge'].isin([14]) & merged_cmc_singles['kstar2merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) | (merged_cmc_singles['kstar1merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & merged_cmc_singles['kstar2merge'].isin([14]))
        # bhnoncompmerge = merged_cmc_singles[merged_cmc_singles['bhnoncompmerge'] == True]
        # print('len bhnoncompmerge', len(bhnoncompmerge))
        # merged_cmc_singles['nsnsmerge'] = merged_cmc_singles['kstar1merge'].isin([13]) & merged_cmc_singles['kstar2merge'].isin([13])
        # nsnsmerge = merged_cmc_singles[merged_cmc_singles['nsnsmerge'] == True]
        # print('len nsnsmerge', len(nsnsmerge))
        # merged_cmc_singles['nswdmerge'] = (merged_cmc_singles['kstar1merge'].isin([10, 11, 12]) & merged_cmc_singles['kstar2merge'].isin([13])) | (merged_cmc_singles['kstar1merge'].isin([13]) & merged_cmc_singles['kstar2merge'].isin([10, 11, 12]))
        # nswdmerge = merged_cmc_singles[merged_cmc_singles['nswdmerge'] == True]
        # print('len nswdmerge', len(nswdmerge))
        # merged_cmc_singles['nsnoncompmerge'] = (merged_cmc_singles['kstar1merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & merged_cmc_singles['kstar2merge'].isin([13])) | (merged_cmc_singles['kstar1merge'].isin([13]) & merged_cmc_singles['kstar2merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        # nsnoncompmerge = merged_cmc_singles[merged_cmc_singles['nsnoncompmerge'] == True]
        # print('len nsnoncompmerge', len(nsnoncompmerge))
        # merged_cmc_singles['wdwdmerge'] = merged_cmc_singles['kstar1merge'].isin([10, 11, 12]) & merged_cmc_singles['kstar2merge'].isin([10, 11, 12])
        # wdwdmerge = merged_cmc_singles[merged_cmc_singles['wdwdmerge'] == True]
        # print('len wdwdmerge', len(wdwdmerge))
        # merged_cmc_singles['wdnoncompmerge'] = (merged_cmc_singles['kstar1merge'].isin([10, 11, 12]) & merged_cmc_singles['kstar2merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) | (merged_cmc_singles['kstar1merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & merged_cmc_singles['kstar2merge'].isin([10, 11, 12]))
        # wdnoncompmerge = merged_cmc_singles[merged_cmc_singles['wdnoncompmerge'] == True]
        # print('len wdnoncompmerge', len(wdnoncompmerge))
        # merged_cmc_singles['noncompnoncompmerge'] = merged_cmc_singles['kstar1merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & merged_cmc_singles['kstar2merge'].isin([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        # noncompnoncompmerge = merged_cmc_singles[merged_cmc_singles['noncompnoncompmerge'] == True]
        # print('len noncompnoncompmerge', len(noncompnoncompmerge))

        # # where are the CMC mergers?
        # plt.hist(merged_cmc_singles['r'], bins=np.logspace(np.log10(0.05), np.log10(30), 100), cumulative=True, density=True, color='blue', histtype='step')
        # plt.xlabel('Clustercentric radial position [pc]')
        # plt.ylabel('Fraction of preserved mergers')
        # plt.axvline(x=2.437, c='blue')
        # plt.savefig('positionpresmergers.png')
        # plt.clf()

        # # where are the CMC disruptions?
        # plt.hist(disrupted_cmc_singles['r'], bins=np.logspace(np.log10(0.05), np.log10(30), 100), cumulative=True, density=True, color='blue', histtype='step')
        # plt.xlabel('Clustercentric radial position [pc]')
        # plt.ylabel('Fraction of preserved disruptions')
        # plt.axvline(x=2.437, c='blue')
        # plt.savefig('positionpresdisrupt.png')
        # plt.clf()

        ############################################# non-preserved escapers ######################################################################
        escapers = nonpreserved_ids[nonpreserved_ids['escapers?'] == True]
        
        
        # ###### look at what kinds of binaries the non-preserved objects are #######
        # # non-preserved COSMIC
        # not_common_ids_init = list(set([i+1 for i in cosmic_init.index])-set(common_ids))
        # print('# not common ids which should be 241294, ok?', len(not_common_ids_init))
        # cosmic_nonpreserved_init = cosmic_init.filter(items=[i-1 for i in not_common_ids_init], axis=0)
        # not_common_ids_present = list(set([i+1 for i in cosmic_present.index])-set(common_ids))
        # cosmic_nonpreserved_present = cosmic_present.filter(items=[i-1 for i in not_common_ids_present], axis=0)
        # print('# not common ids which should be 241200, ok?', len(not_common_ids_present))
        # # non-preserved CMC
        # cmc_nonpreserved_init = cmc20_init.loc[~cmc20_init['id'].isin(common_ids)]
        # cmc_nonpreserved_present = cmc20_present.loc[~cmc20_present['id'].isin(common_ids)]
        # print('non preserved cmc')
        # # see what the present day non preserved stats are
        # # present_cosmic_counts(cosmic_nonpreserved_present)
        # # present_cmc_counts(cmc_nonpreserved_present)
        # ##############################################################################