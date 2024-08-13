import pandas as pd
import h5py
import matplotlib.pyplot as plt
import numpy as np
import cmc_parser as cp
import constants 

# extract desired columns from rv1.5 king.hdf5, current king.hdf5 file, and original rv2.0
cmc15_bin = pd.read_hdf('../rv1.5/king.hdf5', key='CLUS_BINARY_DATA', mode='r')
cmc15_obj = pd.read_hdf('../rv1.5/king.hdf5', key='CLUS_OBJ_DATA', mode='r')

cmc_mod_bin = pd.read_hdf('king.hdf5', key='CLUS_BINARY_DATA', mode='r+')
cmc_mod_obj = pd.read_hdf('king.hdf5', key='CLUS_OBJ_DATA', mode='r+')

#print('before', cmc_mod_bin)
orig_bin = pd.read_hdf('../rvinf/king.hdf5', key='CLUS_BINARY_DATA', mode='r')
orig_obj = pd.read_hdf('../rvinf/king.hdf5', key='CLUS_OBJ_DATA', mode='r')

# take rv1.5 columns, convert to physical units using conv.sh in rv1.5, then convert to code units using conv.sh in rv2.0
rv15_conv = cp.conversion_file('../rv1.5/king.conv.sh') # get rv1.5 conversion file
rv20mod_conv = cp.conversion_file('../rvinf/king.conv.sh')

print(rv15_conv)
for i in range(len(cmc15_bin.a.values)):
	if i != 0:
		cmc_mod_bin.index.values[i] = cmc15_bin.index.values[i]
		cmc_mod_bin.id1.values[i] = cmc15_bin.id1.values[i]
		cmc_mod_bin.k1.values[i] = cmc15_bin.k1.values[i]		
		cmc_mod_bin.m1.values[i] = cmc15_bin.m1.values[i]*rv15_conv.mass_msun/rv20mod_conv.mass_msun
		cmc_mod_bin.Reff1.values[i] = cmc15_bin.Reff1.values[i]*rv15_conv.length_cgs/rv20mod_conv.length_cgs
		cmc_mod_bin.id2.values[i] = cmc15_bin.id2.values[i]
		cmc_mod_bin.k2.values[i] = cmc15_bin.k2.values[i]
		cmc_mod_bin.m2.values[i] = cmc15_bin.m2.values[i]*rv15_conv.mass_msun/rv20mod_conv.mass_msun
		cmc_mod_bin.Reff2.values[i] = cmc15_bin.Reff2.values[i]*rv15_conv.length_cgs/rv20mod_conv.length_cgs
		cmc_mod_bin.a.values[i] = cmc15_bin.a.values[i]*rv15_conv.length_cgs/rv20mod_conv.length_cgs
		cmc_mod_bin.e.values[i] = cmc15_bin.e.values[i]
		cmc_mod_obj.id.values[i] = cmc15_obj.id.values[i]
		cmc_mod_obj.k.values[i] = cmc15_obj.k.values[i]
		cmc_mod_obj.m.values[i] = cmc15_obj.m.values[i]*rv15_conv.mass_msun/rv20mod_conv.mass_msun
		cmc_mod_obj.Reff.values[i] = cmc15_obj.Reff.values[i]*rv15_conv.length_cgs/rv20mod_conv.length_cgs
		cmc_mod_obj.binind.values[i] = cmc15_obj.binind.values[i]

#cmc15_bin.a = [rv15_conv.length_cgs/rv20mod_conv.length_cgs*i for i in cmc15_bin.a.values] # convert rv1.5 to physical units, then convert back to rv2.0 code units
#cmc_mod_bin.a[1:].where(cmc_mod_bin.a[1:] == cmc15_bin.a[1:], cmc15_bin.a[1:], inplace=True) # replace king.hdf5 columns with the scaled rv1.5 columns

#save back to king.hdf5 
cmc_mod_bin.to_hdf('king.hdf5', key='CLUS_BINARY_DATA', mode='w')
cmc_mod_obj.to_hdf('king.hdf5', key='CLUS_OBJ_DATA', mode='a')

vg = 220 #km/s
rg = 8000 #pc
rv = 20 #pc
m_c = sum(cmc_mod_obj.m)*rv20mod_conv.mass_msun
print('m_c', m_c)
r_tidal = (constants.G * m_c * constants.Msun / 2. / (vg*constants.km)**2.)**(1./3.) * (rg*constants.PC)**(2./3.) / constants.PC

with h5py.File('king.hdf5', "a") as f:
	f["CLUS_OBJ_DATA/block0_values"].attrs["EXTNAME"] = "CLUS_OBJ_DATA"
	f["CLUS_OBJ_DATA/block0_values"].attrs["NOBJ"] = int(len(cmc_mod_obj)) - 2
	f["CLUS_OBJ_DATA/block0_values"].attrs["NBINARY"] = (int(len(cmc_mod_bin)) - 1)
	f["CLUS_OBJ_DATA/block0_values"].attrs["MCLUS"] = m_c
	f["CLUS_OBJ_DATA/block0_values"].attrs["RVIR"] = rv
	f["CLUS_OBJ_DATA/block0_values"].attrs["RTID"] = r_tidal/rv
	f["CLUS_OBJ_DATA/block0_values"].attrs["Z"] = 0.00017
print('G', constants.G)
print('mc', m_c)
print('vg', vg)
print('rg', rg)
print('rtidal', r_tidal)
print('r tidal code', r_tidal/rv)

print('altered', cmc_mod_bin.a)
check_mod_bin = pd.read_hdf('king.hdf5', key='CLUS_BINARY_DATA', mode='r')
print('rv1.5', cmc15_bin.a)
print('rv20 mod', check_mod_bin.a)

