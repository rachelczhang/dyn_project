import pandas as pd

# read t=0 snapshot file from different rv's 
def read_snap(rv):
        snap = pd.read_hdf('../dynamics/rv%s/king.snapshots.h5' % (rv,), key='0(t=0)')
        return snap
snap = read_snap(2.0)
for i in range(len(snap['m0_MSUN'])):
	if snap['m0_MSUN'][i] < 138.98 and snap['m0_MSUN'][i] > 138.96:
		print(snap['m0_MSUN'][i], snap['m1_MSUN'][i], snap['a_AU'][i])
