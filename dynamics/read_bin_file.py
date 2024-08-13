import numpy as np
import cmc_parser as cp
import matplotlib.pyplot as plt

class RvData:
        def __init__(self, key):
                self.key = key
                self.timedata = []
                self.binfracdata = []
                

# keys
rv_2 = RvData(2.0)
rv_6 = RvData(6.0)
rv_10 = RvData(10.0)
rv_20 = RvData(20)

rvs = [rv_2, rv_6, rv_10, rv_20]

for r in rvs:
        time = []
        bin_frac = []
        key = r.key
        bin_dat = np.genfromtxt('rv%s_modified/king.bin.dat' % key)
        conv = cp.conversion_file('rv%s_modified/king.conv.sh' % key)
        for i in bin_dat:
                time.append(i[0]*conv.time_myr)
                bin_frac.append(i[11])
        if key < 9.0:
                bin_dat1 = np.genfromtxt('rv%s_modified/kingres1.bin.dat' % key)
                for j in bin_dat1:
                        time.append(j[0]*conv.time_myr)
                        bin_frac.append(j[11])
        r.timedata = time
        r.binfracdata = bin_frac        
        
for r in rvs:
        plt.scatter(r.timedata, r.binfracdata, s=1, label='rv%s' % r.key)
        
plt.xlabel('Time [Myr]')
plt.ylabel('Binary fraction')
plt.legend()
plt.savefig('binfracovertime.png')


