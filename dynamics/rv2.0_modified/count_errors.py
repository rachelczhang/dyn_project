import numpy as np

data = np.genfromtxt('king.esc.dat')

kstar1s = []
kstar2s = []
mass1s = []
mass2s = []

for i in range(len(data)):
        kstar1s.append(data[i,22])
        kstar2s.append(data[i,23])
        mass1s.append(data[i,15])
        mass2s.append(data[i,16])

print('total: ', len(kstar1s))
count = 0
for s in range(len(kstar1s)):
        if (kstar1s[s] > 1 and kstar1s[s] < 10) or (kstar2s[s] > 1 and kstar2s[s] < 10):
                count += 1
print('non compact object/MS: ', count)     

count1 = 0
for m in range(len(mass1s)):
        if mass1s[m] >= 8 or mass2s[m] >= 8:
                count1 += 1
print('higher masses', count1)
