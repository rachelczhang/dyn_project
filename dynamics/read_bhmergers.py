import numpy as np
import cmc_parser as cp
import matplotlib.pyplot as plt
import math

class RvData:
        def __init__(self, key):
                self.key = key
                self.bhmasses = []

rv_2 = RvData(2.0)
rv_6 = RvData(6.0)
rv_10 = RvData(10.0)
rv_20 = RvData(20)

rvs = [rv_2, rv_6, rv_10, rv_20]

for r in rvs:
        masses = []
        key = r.key
        bhform = np.genfromtxt('rv%s_modified/king.bhmerger.dat' % key)
        for i in bhform:
                masses.append(i[6])
        if key < 9.0:
                bhform1 = np.genfromtxt('rv%s_modified/kingres1.bhmerger.dat' % key)
                for j in bhform1:
                        masses.append(j[6])
        r.bhmasses = masses

for r in rvs:
        plt.hist(r.bhmasses, bins=np.logspace(np.log10(min(rv_2.bhmasses)), np.log10(max(rv_2.bhmasses)), 50),  histtype='step', label='rv%s' % r.key)

plt.yscale('log')
plt.xscale('log')
plt.xlabel('Merged BH Masses [M_sol]')
plt.legend()
plt.savefig('mergedBHmasses.png')
