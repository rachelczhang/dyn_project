import pandas as pd 

# reads in data into smaller parts to download locally to study

cmc_init = pd.read_hdf('rv2.0/king.snapshots.h5', key='0(t=0)')

cmc_init.to_hdf('cmc_init.h5', key='cmc_init', mode='w')
