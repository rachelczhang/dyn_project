import numpy as np
import pandas as pd
import cmc_parser as cp
import math 

data = np.genfromtxt('king.esc.dat')
data2 = np.genfromtxt('kingres1.esc.dat')
rv20mod_conv = cp.conversion_file('king.conv.sh')

def count(cond, data):
	#print(data[cond])
	cond_count = len(data[cond].index)
	return cond_count

id0 = []
id1 = []
kstar0 = []
kstar1 = []

for i in range(len(data)):
	if i != 0:
		if math.isnan(data[i,22]):
			id0.append(int(data[i,13]))
			id1.append(-1)
			kstar0.append(data[i,21])
			kstar1.append(-1)
		else:
			id0.append(int(data[i, 17]))
			id1.append(int(data[i, 18]))
			kstar0.append(data[i,22])
			kstar1.append(data[i,23])

for i in range(len(data2)):
	if math.isnan(data2[i,22]):
		id0.append(int(data2[i,13]))
		id1.append(-1)
		kstar0.append(data2[i,21])
		kstar1.append(-1)
	else:
		id0.append(int(data2[i, 17]))
		id1.append(int(data2[i, 18]))
		kstar0.append(data2[i,22])
		kstar1.append(data2[i,23])

escapers = pd.DataFrame(list(zip(id0, id1, kstar0, kstar1)), columns=['id0', 'id1', 'kstar0', 'kstar1'])
print('escapers', escapers)

binary_escapers = escapers[escapers['id1'] != -1]
single_escapers = escapers[escapers['id1'] == -1]
print('binary escapers', binary_escapers)
print('single escapers', single_escapers)


print('BINARY ESCAPERS')
print(' Total # binaries with BHs: ', count((binary_escapers['kstar0'] == 14.0) | (binary_escapers['kstar1'] == 14.0), binary_escapers))
print(' Total # BH-BHs: ', count((binary_escapers['kstar0'] == 14.0) & (binary_escapers['kstar1'] == 14.0), binary_escapers))
print(' Total # binaries with NSs: ', count(((binary_escapers['kstar0'] == 13.0) & (binary_escapers['kstar1'] < 14.0) & (binary_escapers['kstar1'] >= 0.0)) | ((binary_escapers['kstar0'] < 14.0) & (binary_escapers['kstar0'] >= 0.0) & (binary_escapers['kstar1'] == 13.0)), binary_escapers))
print(' Total # NS-NSs: ', count((binary_escapers['kstar0'] == 13.0) & (binary_escapers['kstar1'] == 13.0), binary_escapers))
print(' Total # WD-WDs: ', count(((binary_escapers['kstar0'] == 10.0) | (binary_escapers['kstar0'] == 11.0) | (binary_escapers['kstar0'] == 12.0)) & ((binary_escapers['kstar1'] == 10.0) | (binary_escapers['kstar1'] == 11.0) | (binary_escapers['kstar1'] == 12.0)), binary_escapers))
print(' Total # WD-non WDs: ', count((((binary_escapers['kstar0'] == 10.0) | (binary_escapers['kstar0'] == 11.0) | (binary_escapers['kstar0'] == 12.0)) & (binary_escapers['kstar1'] < 10.0)) | ((binary_escapers['kstar0'] < 10.0) & ((binary_escapers['kstar1'] == 10.0) | (binary_escapers['kstar1'] == 11.0) | (binary_escapers['kstar1'] == 12.0))), binary_escapers))
print(' Total non-compact-object binaries: ', count((binary_escapers['kstar0'] < 10.0) & (binary_escapers['kstar0'] >= 0.0) & (binary_escapers['kstar1'] >= 0.0) & (binary_escapers['kstar1'] < 10.0), binary_escapers))
print(' Total # MS-MS: ', count(((binary_escapers['kstar0'] == 0.0) | (binary_escapers['kstar0'] == 1.0)) & ((binary_escapers['kstar1'] == 0.0) | (binary_escapers['kstar1'] == 1.0)), binary_escapers))
print(' Total # WD-MS: ', count((((binary_escapers['kstar0'] == 10.0) | (binary_escapers['kstar0'] == 11.0) | (binary_escapers['kstar0'] == 12.0)) & ((binary_escapers['kstar1'] == 0.0) | (binary_escapers['kstar1'] == 1.0))) | (((binary_escapers['kstar0'] == 0.0) | (binary_escapers['kstar0'] == 1.0)) & ((binary_escapers['kstar1'] == 10.0) | (binary_escapers['kstar1'] == 11.0) | (binary_escapers['kstar1'] == 12.0))), binary_escapers))
print(' Double massless remnants: ', count((binary_escapers['kstar0'] == 15.0) & (binary_escapers['kstar1'] == 15.0), binary_escapers))

print('SINGLE ESCAPERS')
print(' Total # single systems: ', count((single_escapers['kstar0'] >= 0.0) & (single_escapers['kstar0'] <= 15.0), single_escapers))
print(' Total # BH singles: ', count((single_escapers['kstar0'] == 14.0), single_escapers))
print(' Total # NS singles: ', count((single_escapers['kstar0'] == 13.0), single_escapers))
print(' Total # WD singles: ', count(((single_escapers['kstar0'] == 10.0) | (single_escapers['kstar0'] == 11.0) | (single_escapers['kstar0'] == 12.0)), single_escapers))
print(' Total # MS singles: ', count(((single_escapers['kstar0'] == 0.0) | (single_escapers['kstar0'] == 1.0)), single_escapers))
print(' Total # other singles: ', count((single_escapers['kstar0'] > 1.0) & (single_escapers['kstar0'] < 10.0), single_escapers))