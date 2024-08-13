import numpy as np
import gzip
from re import findall
import cmc_parser as cp
import matplotlib.pyplot as plt

CC_conv = cp.conversion_file('/projects/b1091/CMC_Grid_March2019/rundir/rv0.5/rg20/z0.002/8e5/initial.conv.sh')
CC_init_snap = '/projects/b1091/CMC_Grid_March2019/rundir/rv0.5/rg20/z0.002/8e5/initial.snap0000.dat.gz'
CC_final_snap = '/projects/b1091/CMC_Grid_March2019/rundir/rv0.5/rg20/z0.002/8e5/initial.snap0513.dat.gz'
nonCC_conv = cp.conversion_file('/projects/b1091/CMC_Grid_March2019/rundir/rv2/rg20/z0.002/8e5/initial.conv.sh')
nonCC_init_snap = '/projects/b1091/CMC_Grid_March2019/rundir/rv2/rg20/z0.002/8e5/initial.snap0000.dat.gz'
nonCC_final_snap = '/projects/b1091/CMC_Grid_March2019/rundir/rv2/rg20/z0.002/8e5/initial.snap0305.dat.gz'

def get_time(filepath):      
        # Returns the cluster's age for a given snapshot
        with gzip.open(filepath,'r') as f: contents = f.readline()
        if not findall(b'\d+[\.]?\d*',contents):        # Returns time = 0 for snapshot files without a time header
                print('snapshot empty'); return float(0)
        else: return float(findall(b'\d+[\.]?\d*',contents)[0])

def get_ids_a_from_snapshot(snapfile):
        ids_a = {}
        with gzip.open(snapfile, 'r') as fsnap:
                next(fsnap); next(fsnap)
                for line in fsnap:
                        data=line.split()
                        if float(data[8]) > 0.3 and float(data[9]) > 0.3 and int(data[10]) > 0 and int(data[11]) > 0 and float(data[17]) < 2 and float(data[18]) < 2:
                                ids_a[(int(data[10]), int(data[11]))] = float(data[12])
        return ids_a

def find_preserved_cmc_ids(init_ids, final_ids):
        preserved_init = {}
        preserved_fin = {}
        for key_id in final_ids:
                if key_id in init_ids and final_ids[key_id] != -100.0:
                        preserved_init[key_id] = init_ids[key_id]
                        preserved_fin[key_id] = final_ids[key_id]
        return preserved_init, preserved_fin

plt.rcParams['font.serif'] = ['Computer Modern', 'Times New Roman']
plt.rcParams['font.family'] = ['serif', 'STIXGeneral']
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams.update({'font.size': 18})

# core-collapsed cluster        
print(get_time(CC_final_snap)*CC_conv.time_myr)                
CC_init_ids = get_ids_a_from_snapshot(CC_init_snap)
print('len init', len(CC_init_ids))
CC_final_ids = get_ids_a_from_snapshot(CC_final_snap)
print('len final', len(CC_final_ids))
CC_preserved_init, CC_preserved_fin = find_preserved_cmc_ids(CC_init_ids, CC_final_ids)
print('len preserved init', len(CC_preserved_init))
print('len preserved final', len(CC_preserved_fin)) 
plt.hist(CC_preserved_init.values(), bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='Initial',  histtype='step')
plt.hist(CC_preserved_fin.values(), bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='Final',  histtype='step')
plt.title('Example core-collapsed cluster')
plt.xscale('log')
plt.yscale('log')
plt.legend(fontsize=18)
plt.xlabel('Semimajor Axis [AU]')
plt.ylabel('Number of MS binaries')
plt.savefig('catalogCC.png')
plt.clf()

# non core-collapsed cluster
print(get_time(nonCC_final_snap)*nonCC_conv.time_myr)
nonCC_init_ids = get_ids_a_from_snapshot(nonCC_init_snap)
print('len init', len(nonCC_init_ids))
nonCC_final_ids = get_ids_a_from_snapshot(nonCC_final_snap)
print('len final', len(nonCC_final_ids))
nonCC_preserved_init, nonCC_preserved_fin = find_preserved_cmc_ids(nonCC_init_ids, nonCC_final_ids)
print('len preserved init', len(nonCC_preserved_init))
print('len preserved final', len(nonCC_preserved_fin))
plt.title('Example non-core-collapsed cluster')
plt.hist(nonCC_preserved_init.values(), bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='Initial',  histtype='step')
plt.hist(nonCC_preserved_fin.values(), bins=np.logspace(np.log10(0.001), np.log10(20), 100), label='Final',  histtype='step')
plt.xscale('log')
plt.yscale('log')
#plt.xticks([0.001, 0.01, 0.1, 1, 10], [r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$', r'$10^{1}$'], fontsize=22, fontname='STIXGeneral')
plt.legend(fontsize=16)
plt.xlabel('Semimajor Axis [AU]')
plt.ylabel('Number of MS binaries')
plt.savefig('catalognonCC.png')
