import pandas as pd 
import h5py
import matplotlib.pyplot as plt 
import numpy as np 
import cmc_parser as cp 

# try method of converting hdf5 file into DF
#cmc_mod_bin = pd.DataFrame(np.array(h5py.File('king.hdf5')['CLUS_BINARY_DATA']))

# extract desired columns from rv1.5 king.hdf5
cmc15_bin = pd.read_hdf('../rv1.5/king.hdf5', key='CLUS_BINARY_DATA', mode='r')
cmc15_obj = pd.read_hdf('../rv1.5/king.hdf5', key='CLUS_OBJ_DATA', mode='r')

#cmc_mod_bin = pd.read_hdf('king.hdf5', key='CLUS_BINARY_DATA', mode='r+')
#cmc_mod_obj = pd.read_hdf('king.hdf5', key='CLUS_OBJ_DATA', mode='r+')

orig_bin = pd.read_hdf('../rv2.0/king.hdf5', key='CLUS_BINARY_DATA', mode='r')
orig_obj = pd.read_hdf('../rv2.0/king.hdf5', key='CLUS_OBJ_DATA', mode='r')

# try new method to just assign values, not create a dataset

#cmc_mod = h5py.File('king.hdf5', 'r+')
#cmc_mod_bin = cmc_mod['CLUS_BINARY_DATA']
#for k in cmc_mod_bin.keys():
#	print('k', k)
#print('keys', cmc_mod_bin.keys())
#print('axis0', cmc_mod_bin['axis0'])
#print('axis1', cmc_mod_bin['axis1'])
#print('a', cmc_mod_bin['axis0']['a'])
#print('cmc mod bin', cmc_mod_bin)
#cmc_mod.close()

# replace such columns in each of the other rv's
#cmc_mod_bin['index'][1:] = cmc15_bin['index'][1:]
#cmc_mod_bin['id1'][1:] = cmc15_bin['id1'][1:]
#cmc_mod_bin['k1'][1:] = cmc15_bin['k1'][1:]
#cmc_mod_bin['m1'][1:] = cmc15_bin['m1'][1:]
#cmc_mod_bin['Reff1'][1:] = cmc15_bin['Reff1'][1:]
#cmc_mod_bin['id2'][1:] = cmc15_bin['id2'][1:]
#cmc_mod_bin['k2'][1:] = cmc15_bin['k2'][1:]
#cmc_mod_bin['m2'][1:] = cmc15_bin['m2'][1:]
#cmc_mod_bin['Reff2'][1:] = cmc15_bin['Reff2'][1:]
#print('before', cmc_mod_bin['a'][1:])
#print('want', cmc15_bin['a'][1:])
#cmc_mod_bin['a'][1:] = cmc15_bin['a'][1:]
#print('after', cmc_mod_bin['a'][1:])
#cmc_mod_bin['e'][1:] = cmc15_bin['e'][1:]
#cmc_mod_obj['id'][1:] = cmc15_obj['id'][1:]
#cmc_mod_obj['k'][1:] = cmc15_obj['k'][1:]
#cmc_mod_obj['m'][1:] = cmc15_obj['m'][1:]
#cmc_mod_obj['Reff'][1:] = cmc15_obj['Reff'][1:]
#cmc_mod_obj['binind'][1:] = cmc15_obj['binind'][1:]

#cmc_mod_bin.replace(to_replace=cmc_mod_bin.index, value=cmc15_bin.index)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.id1, value=cmc15_bin.id1)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.k1, value=cmc15_bin.k1)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.m1, value=cmc15_bin.m1)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.Reff1, value=cmc15_bin.Reff1)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.id2, value=cmc15_bin.id2)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.k2, value=cmc15_bin.k2)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.m2, value=cmc15_bin.m2)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.Reff2, value=cmc15_bin.Reff2)
#print('a', cmc_mod_bin.a.values)
print('rv1.5', cmc15_bin['a'])
#print(cmc_mod_bin.a[1:] == cmc15_bin.a[1:])
#cmc_mod_bin.a[0:].where(cmc_mod_bin.a[0:] == cmc15_bin.a[0:], cmc15_bin.a[0:], inplace=True)

#d = {}
#for i in range(len(cmc_mod_bin.a.values[0:10])):
#	d[cmc_mod_bin.a.values[i]] = cmc15_bin.a.values[i]
#print('d', d)	
#cmc_mod_bin.replace(to_replace=d, value=None, inplace=True)
#cmc_mod_bin.replace(to_replace=cmc_mod_bin.e, value=cmc15_bin.e)
#cmc_mod_obj.replace(to_replace=cmc_mod_obj.id, value=cmc15_obj.id)
#cmc_mod_obj.replace(to_replace=cmc_mod_obj.k, value=cmc15_obj.k)
#cmc_mod_obj.replace(to_replace=cmc_mod_obj.m, value=cmc15_obj.m)
#cmc_mod_obj.replace(to_replace=cmc_mod_obj.Reff, value=cmc15_obj.Reff)
#cmc_mod_obj.replace(to_replace=cmc_mod_obj.binind, value=cmc15_obj.binind)

#cmc_mod_bin.index = cmc15_bin.index
#cmc_mod_bin.id1 = cmc15_bin.id1
#cmc_mod_bin.k1 = cmc15_bin.k1
#cmc_mod_bin.m1 = cmc15_bin.m1
#cmc_mod_bin.Reff1 = cmc15_bin.Reff1
#cmc_mod_bin.id2 = cmc15_bin.id2
#cmc_mod_bin.k2 = cmc15_bin.k2
#cmc_mod_bin.m2 = cmc15_bin.m2
#cmc_mod_bin.Reff2 = cmc15_bin.Reff2
#cmc_mod_bin.a = cmc15_bin.a
#print('change to a', cmc15_bin.a)
#print('want a', cmc_mod_bin.a)
#cmc_mod_bin.e = cmc15_bin.e
#print('want e', cmc_mod_bin.e)

#cmc_mod_obj.id = cmc15_obj.id
#cmc_mod_obj.k = cmc15_obj.k
#cmc_mod_obj.m = cmc15_obj.m
#cmc_mod_obj.Reff = cmc15_obj.Reff
#cmc_mod_obj.binind = cmc15_obj.binind

#cmc_mod_bin.to_hdf('king.hdf5', key='CLUS_BINARY_DATA')
#cmc_mod_obj.to_hdf('king.hdf5', key='CLUS_OBJ_DATA')

#with h5py.File('king.hdf5', "a") as f:
#	f["CLUS_OBJ_DATA/block0_values"].attrs["EXTNAME"] = "CLUS_OBJ_DATA"
#	f["CLUS_OBJ_DATA/block0_values"].attrs["NOBJ"] = int(len(singles)) - 2
#	f["CLUS_OBJ_DATA/block0_values"].attrs["NBINARY"] = (int(len(binaries)) - 1)
#	f["CLUS_OBJ_DATA/block0_values"].attrs["MCLUS"] = Singles.mass_of_cluster
#	f["CLUS_OBJ_DATA/block0_values"].attrs["RVIR"] = virial_radius
#	f["CLUS_OBJ_DATA/block0_values"].attrs["RTID"] = tidal_radius
#	f["CLUS_OBJ_DATA/block0_values"].attrs["Z"] = metallicity
see_mod_bin = pd.read_hdf('king.hdf5', key='CLUS_BINARY_DATA', mode='r')
see_mod_obj = pd.read_hdf('king.hdf5', key='CLUS_OBJ_DATA', mode='r')

print('modified a', see_mod_bin.a)

print('equal?', cmc15_bin.a == see_mod_bin.a)
#print('modified e', see_mod_bin.e)
#print('modified id', see_mod_obj.id)
#plt.hist(see_mod_obj.m, histtype='step', label='modified') 
#plt.hist(orig_obj.m, histtype='step', label='original')
#plt.xscale('log')
#plt.yscale('log')
#plt.legend()
#plt.savefig('mass_dist.png')

#plt.hist(see_mod_obj.r, alpha=0.3, label='modified')
#plt.hist(orig_obj.r, alpha=0.3, label='original')
#plt.legend()
#plt.savefig('rad_dist.png')

rv20mod_conv = cp.conversion_file('king.conv.sh')
see_mod_bin.a = [rv20mod_conv.length_cgs*i/(1.496e13) for i in see_mod_bin.a]
rv20_conv = cp.conversion_file('../rv2.0/king.conv.sh')
orig_bin.a = [rv20_conv.length_cgs*i/(1.496e13) for i in orig_bin.a]
rv15_conv = cp.conversion_file('../rv1.5/king.conv.sh')
cmc15_bin.a = [rv15_conv.length_cgs*i/(1.496e13) for i in cmc15_bin.a]
print('equal?', cmc15_bin.a == see_mod_bin.a)
#check a
plt.hist(see_mod_bin.a, alpha=0.3, label='rv.2.0 mod', bins=np.logspace(np.log10(10**(-9)), np.log10(10**2), 200), histtype='step')
plt.hist(orig_bin.a, alpha=0.3, label='rv 2.0', bins=np.logspace(np.log10(10**(-9)), np.log10(10**2), 200), histtype='step')
plt.hist(cmc15_bin.a, alpha=0.3, label='rv 1.5', bins=np.logspace(np.log10(10**(-9)), np.log10(10**2), 200), histtype='step')
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.savefig('a_dist.png')
