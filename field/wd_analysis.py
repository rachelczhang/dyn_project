import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import csv 

bcm_data = pd.read_hdf('bcm.h5', 'bcm')
bpp_data = pd.read_hdf('bpp.h5', 'bpp')

def counts(startype):
	ind_dict = {}
	binaries_ind_dict = {}
	diff_bin_ind_dict = {}
	for i in np.unique(bpp_data.index.values):
		# initializing dict 1
		ind_dict[i] = 0
		binaries_ind_dict[i] = 0
		diff_bin_ind_dict[i] = 0
	# dict 2 time: sum of dict 1
	count_dict = {0:0}
	binaries_count_dict = {0:0}
	diff_bin_count_dict = {0:0}
	# filter for all the data with desired kstar and all times after it
	bpp_filter = bpp_data[(bpp_data['kstar_1'] == startype) | (bpp_data['kstar_2'] == startype)]
	for i in np.unique(bpp_filter.index.values):
		if len(bpp_filter.loc[i].index) == 1:
			time = bpp_filter.loc[i]['tphys']
		elif len(bpp_filter.loc[i].index) == 44:
			time = bpp_filter.loc[i]['tphys'] 
		else:
			time = bpp_filter.loc[i].iloc[-1]['tphys']
		bpp_filter = pd.concat([bpp_filter, bpp_data.loc[i][(bpp_data.loc[i]['tphys'] > time)]])
	# sort t values
	bpp_data_sort = bpp_filter.sort_values('tphys')
	# for each t value with a kstar change, check if:
	for t in np.unique(bpp_data_sort['tphys']):
		data_row = bpp_data_sort[(bpp_data_sort['tphys']==t)]
		for i in np.unique(data_row.index.values):
			# an ID goes from 0 kstars of startype to 1 or 2 
			if ind_dict[i] == 0 and len(data_row.loc[i].index) != 1 and len(data_row.loc[i].index) != 44:
				if data_row.loc[i].iloc[-1]['kstar_1'] == startype or data_row.loc[i].iloc[-1]['kstar_2'] == startype:
					if data_row.loc[i].iloc[-1]['kstar_1'] == startype and data_row.loc[i].iloc[-1]['kstar_2'] == startype:
						ind_dict[i] += 2
					else:
						ind_dict[i] += 1
						# if 0-->1, add 1 to diff binary count
						if data_row.loc[i].iloc[-1]['kstar_1'] != 15.0 and data_row.loc[i].iloc[-1]['kstar_2'] != 15.0:
							diff_bin_ind_dict[i] += 1
					# in both cases, if either kstar is not 15, add 1 to binary count
					if data_row.loc[i].iloc[-1]['kstar_1'] != 15.0 and data_row.loc[i].iloc[-1]['kstar_2'] != 15.0:
						binaries_ind_dict[i] += 1 
			elif ind_dict[i] == 0 and (len(data_row.loc[i].index) == 1 or len(data_row.loc[i].index) == 44):
				if data_row.loc[i]['kstar_1'] == startype or data_row.loc[i]['kstar_2'] == startype:
					if data_row.loc[i]['kstar_1'] == startype and data_row.loc[i]['kstar_2'] == startype:
						ind_dict[i] += 2
					else:
						ind_dict[i] += 1
						# if 0-->1, add 1 to diff binary count
						if data_row.loc[i]['kstar_1'] != 15.0 and data_row.loc[i]['kstar_2'] != 15.0:
							diff_bin_ind_dict[i] += 1
					# in both cases, if either kstar is not 15, add 1 to binary count
					if data_row.loc[i]['kstar_1'] != 15.0 and data_row.loc[i]['kstar_2'] != 15.0:
						binaries_ind_dict[i] += 1
			# an ID goes from 1 kstar of startype to 0 or 2
			elif ind_dict[i] == 1 and len(data_row.loc[i].index) != 1 and len(data_row.loc[i].index) != 44:
				# if 1-->0, subtract 1 to binary count
				# in both cases, subtract 1 to diff binary count
				if data_row.loc[i].iloc[-1]['kstar_1'] != startype and data_row.loc[i].iloc[-1]['kstar_2'] != startype:
					ind_dict[i] -= 1
					binaries_ind_dict[i] -= 1
					diff_bin_ind_dict[i] -= 1
				elif data_row.loc[i].iloc[-1]['kstar_1'] == startype and data_row.loc[i].iloc[-1]['kstar_2'] == startype:
					ind_dict[i] += 1
					diff_bin_ind_dict[i] -= 1
			elif ind_dict[i] == 1 and (len(data_row.loc[i].index) == 1 or len(data_row.loc[i].index) == 44):
				if data_row.loc[i]['kstar_1'] != startype and data_row.loc[i]['kstar_2'] != startype:
					ind_dict[i] -= 1
					binaries_ind_dict[i] -= 1
					diff_bin_ind_dict[i] -= 1
				elif data_row.loc[i]['kstar_1'] == startype and data_row.loc[i]['kstar_2'] == startype:
					ind_dict[i] += 1
					diff_bin_ind_dict[i] -= 1
			# an ID goes from 2 kstars of startype to 0 or 1
			elif ind_dict[i] == 2 and len(data_row.loc[i].index) != 1 and len(data_row.loc[i].index) != 44:
				if data_row.loc[i].iloc[-1]['kstar_1'] != startype or data_row.loc[i].iloc[-1]['kstar_2'] != startype:
					# if 2-->0, subtract 1 to binary count
					if data_row.loc[i].iloc[-1]['kstar_1'] != startype and data_row.loc[i].iloc[-1]['kstar_2'] != startype:
						ind_dict[i] -= 2
						binaries_ind_dict[i] -= 1
					else:
						# if 2-->1 and other kstar is 15, subtract 1 to binary count
						# if 2-->1 and other kstar is not 15, add 1 to diff binary count 
						ind_dict[i] -= 1
						if data_row.loc[i].iloc[-1]['kstar_1'] == 15.0 or data_row.loc[i].iloc[-1]['kstar_2'] == 15.0:
							binaries_ind_dict[i] -= 1
						else:
							diff_bin_ind_dict[i] += 1
			elif ind_dict[i] == 2 and (len(data_row.loc[i].index) == 1 or len(data_row.loc[i].index) == 44):
				if data_row.loc[i]['kstar_1'] != startype or data_row.loc[i]['kstar_2'] != startype:
					if data_row.loc[i]['kstar_1'] != startype and data_row.loc[i]['kstar_2'] != startype:
						ind_dict[i] -= 2
						binaries_ind_dict[i] -= 1
					else:
						ind_dict[i] -= 1
						if data_row.loc[i]['kstar_1'] == 15.0 or data_row.loc[i]['kstar_2'] == 15.0:
							binaries_ind_dict[i] -= 1
						else:
							diff_bin_ind_dict[i] += 1
		# update count dictionary 
		count_dict[t] = sum(ind_dict.values())
		binaries_count_dict[t] = sum(binaries_ind_dict.values())
		diff_bin_count_dict[t] = sum(diff_bin_ind_dict.values())
	return count_dict, binaries_count_dict, diff_bin_count_dict

def count_specific_bins(startype, startype2):
	ind_dict = {}
	for i in np.unique(bpp_data.index.values):
		ind_dict[i] = 0
	count_dict = {0:0}
	# filter for binaries with type condition and all the time after that 
	bpp_filter = bpp_data[((bpp_data['kstar_1'] == startype) & (bpp_data['kstar_2'] == startype2)) \
		| ((bpp_data['kstar_1'] == startype2) & (bpp_data['kstar_2'] == startype))]
	for i in np.unique(bpp_filter.index.values):
		if len(bpp_filter.loc[i].index) == 1:
			time = bpp_filter.loc[i]['tphys']
		elif len(bpp_filter.loc[i].index) == 44:
			time = bpp_filter.loc[i]['tphys'] 
		else:
			time = bpp_filter.loc[i].iloc[-1]['tphys']
		bpp_filter = pd.concat([bpp_filter, bpp_data.loc[i][(bpp_data.loc[i]['tphys'] > time)]])
	bpp_data_sort = bpp_filter.sort_values('tphys')
	for t in bpp_data_sort['tphys']:	
		data_row = bpp_data_sort[(bpp_data_sort['tphys']==t)]
		for i in data_row.index.values:
			# starting at 0: condition has to be met to go to 1
			if ind_dict[i] == 0:
				if len(data_row.loc[i].index) == 44:
					if (data_row.loc[i]['kstar_1'] == startype and data_row.loc[i]['kstar_2'] == startype2) or \
						(data_row.loc[i]['kstar_2'] == startype and data_row.loc[i]['kstar_1'] == startype2):
						ind_dict[i] += 1
				else:
					if (data_row.loc[i].iloc[-1]['kstar_1'] == startype and data_row.loc[i].iloc[-1]['kstar_2'] == startype2) or \
						(data_row.loc[i].iloc[-1]['kstar_2'] == startype and data_row.loc[i].iloc[-1]['kstar_1'] == startype2):
						ind_dict[i] += 1
			# starting at 1: condition has to be not met to go to 0
			if ind_dict[i] == 1:
				if len(data_row.loc[i].index) == 44:
					if not((data_row.loc[i]['kstar_1'] == startype and data_row.loc[i]['kstar_2'] == startype2) or \
						(data_row.loc[i]['kstar_2'] == startype and data_row.loc[i]['kstar_1'] == startype2)):
						ind_dict[i] -= 1
				else:
					if not((data_row.loc[i].iloc[-1]['kstar_1'] == startype and data_row.loc[i].iloc[-1]['kstar_2'] == startype2) or \
						(data_row.loc[i].iloc[-1]['kstar_2'] == startype and data_row.loc[i].iloc[-1]['kstar_1'] == startype2)):
						ind_dict[i] -= 1
		count_dict[t] = sum(ind_dict.values())
	return count_dict 

def get_present_stats(startype, startype2 = None):
	bcm_filter = bcm_data[((bcm_data['kstar_1'] == startype) | (bcm_data['kstar_2'] == startype)) & (bcm_data['tphys'] == 13700.0)]
	total = 0
	singles = 0
	binaries = 0
	same_bin = 0
	diff_bin = 0
	if startype2 != None:
		specific_bin = [0]*len(startype2)
	for i in bcm_filter.index.values:
		if bcm_filter.loc[i]['kstar_1'] == startype and bcm_filter.loc[i]['kstar_2'] == startype:
			total += 2
			binaries += 1
			same_bin += 1
		else:
			total += 1
			if bcm_filter.loc[i]['kstar_1'] == 15.0 or bcm_filter.loc[i]['kstar_2'] == 15.0:
				singles += 1
			elif bcm_filter.loc[i]['kstar_1'] != 15.0 and bcm_filter.loc[i]['kstar_2'] != 15.0:
				binaries += 1
				diff_bin += 1
				if startype2 != None:
					for j in range(len(startype2)):
						if bcm_filter.loc[i]['kstar_1'] == startype2[j] or bcm_filter.loc[i]['kstar_2'] == startype2[j]:
							specific_bin[j] += 1
	return total, singles, binaries, same_bin, diff_bin, specific_bin

def writerow(dic, filename):
	w = csv.writer(open(filename, 'w'))
	for k, v in dic.items():
		w.writerow([k, v])
	return

def save_data(count, bin_count, diff_bin_count, single, wdwd, wdms, wdms2):
	"""
	save dictionary into a file named filename
	"""
	writerow(count, 'hewdtotal.csv')
	writerow(single, 'hewdsingles.csv')
	writerow(bin_count, 'hewdbins.csv')
	writerow(wdwd, 'hewdwd.csv')
	writerow(diff_bin_count, 'hewd-nonwd.csv')
	writerow(wdms, 'hewdms.csv')
	writerow(wdms2, 'hewdms2.csv')
	return

######### WD ANALYSIS #########
count_dict, binaries_count_dict, diff_bin_count_dict = counts(10.0)
print('count dict', count_dict)
print('binaries count dict', binaries_count_dict)
print('diff bin count dict', diff_bin_count_dict)
singleWD_count = count_specific_bins(10.0, 15.0)
print('single WDs', singleWD_count)
WDWD_count = count_specific_bins(10.0, 10.0)
print('WDWD count', WDWD_count)
WDMS_count = count_specific_bins(10.0, 0.0)
print('WDMS count', WDMS_count)
WDMS_count2 = count_specific_bins(10.0, 1.0)
print('WDMS count2', WDMS_count2)
save_data(count_dict, binaries_count_dict, diff_bin_count_dict, singleWD_count, WDWD_count, WDMS_count, WDMS_count2)
