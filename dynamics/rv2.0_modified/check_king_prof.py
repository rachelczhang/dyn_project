# read snapshot files at t = 0 for the rv2.0 and rv2.0_modified versions of king.hdf5 
cmc_20 = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0/king.snapshots.h5', key='0(t=0)')
cmc_20_mod = pd.read_hdf('/projects/b1095/rczhang/dyn_proj/dynamics/rv2.0_modified/king.snapshots.h5', key='0(t=0)')
# plot radius from the center of galaxy  vs. density plot to see if both versions match
r = cmc_20['r']
r_mod = cmc_20_mod['r']

plt.hist(r, bins=np.logspace(np.log10(10**(-3)), np.log10(10**7), 50), label='original', histtype='step')
plt.hist(r_mod, bins=np.logspace(np.log10(10**(-3)), np.log10(10**7), 50), label='modified', histtype='step')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.savefig('kingproifle.png')

