# Script that lets you go through each snapshot file and extract desired binary information
import pandas as pd 
import h5py 
import numpy as np 
import csv

def snapshot_list(h5file):
	""" 
	return all keys in a run, in key format and in number format
	"""
	f = h5py.File(h5file, 'r')
	keys = f.keys()
	snapno_of_window = [key.split('(')[0] for key in keys]
	age = [key.split('=')[1].split('G')[0] for key in keys]
	snapshot_keys_ordered_by_age = np.array(['%s(t=%sGyr)'%(s,a) for (a,s) in sorted(zip(age,snapno_of_window))],dtype='str')
	snapshot_ages_Myr = np.array(list(map(float,sorted(age)))) * 1e3
	f.close()
	return (snapshot_keys_ordered_by_age, snapshot_ages_Myr)

def extract_properties(h5file, bin_type, key=None):
	""" 
	return the desired properties of a binary type, bin_type, of a specific snapshot
	defaults to latest snapshot if no key is input. returns time stamp, properties. 
	"""
	if key == None:
		key = snapshot_list(h5file)[0][-1]
	age = key.split('=')[1].split('G')[0]
	t = float(age) * 1e3
	snap = pd.read_hdf(h5file,key=key)
	sing_wds = snap[(snap['startype'] == bin_type)]
	total_singles = len(sing_wds.index)
	bins_wds = snap[(snap['bin_startype0'] == bin_type) | (snap['bin_startype1'] == bin_type)]
	total_binaries = len(bins_wds.index)
	wd_wds = snap[(snap['bin_startype0'] == bin_type) & (snap['bin_startype1'] == bin_type)]
	total_wdwd = len(wd_wds.index)
	total = total_singles + total_binaries + total_wdwd
	total_diff_bins = total_binaries-total_wdwd
	wd_ms = snap[((snap['bin_startype0'] == bin_type) & (snap['bin_startype1'] == 0.0)) | \
		((snap['bin_startype0'] == 0.0) & (snap['bin_startype1'] == bin_type)) | \
		((snap['bin_startype0'] == bin_type) & (snap['bin_startype1'] == 1.0)) | \
                ((snap['bin_startype0'] == 1.0) & (snap['bin_startype1'] == bin_type))]
	total_wd_ms = len(wd_ms.index)
	return t, total, total_singles, total_binaries, total_wdwd, total_diff_bins, total_wd_ms

def combine_dict(h5file, bin_type):
	"""
	returns the dictionaries of all times corresponding to properties from the snapshot files
	"""
	total_dict = {}
	singles_dict = {}
	bin_dict = {}
	wdwd_dict = {}
	diff_bins_dict = {}
	wd_ms_dict = {}
	keys = snapshot_list(h5file)[0]
	for k in keys:
		t, total, total_singles, total_binaries, total_wdwd, total_diff_bins, total_wd_ms = extract_properties(h5file, bin_type, key=k)
		total_dict[t] = total
		singles_dict[t] = total_singles
		bin_dict[t] = total_binaries
		wdwd_dict[t] = total_wdwd
		diff_bins_dict[t] = total_diff_bins
		wd_ms_dict[t] = total_wd_ms
	return total_dict, singles_dict, bin_dict, wdwd_dict, diff_bins_dict, wd_ms_dict
		

def writerow(dic, filename):
	w = csv.writer(open(filename, 'w'))
	for k, v in dic.items():
		w.writerow([k, v])
	return 
		
def save_data(h5file, bin_type):
	"""
	save dictionary into a file named filename
	"""
	total_dict, singles_dict, bin_dict, wdwd_dict, diff_bins_dict, wd_ms_dict = combine_dict(h5file, bin_type)
	writerow(total_dict, 'wdtotal.csv')
	writerow(singles_dict, 'wdsingles.csv')
	writerow(bin_dict, 'wdbinaries.csv')
	writerow(wdwd_dict, 'wdwdbinaries.csv')
	writerow(diff_bins_dict, 'wd-nonwdbinaries.csv')
	writerow(wd_ms_dict, 'wdmsbinaries.csv')
	return

save_data('king.window.snapshots.h5', 10.0)
