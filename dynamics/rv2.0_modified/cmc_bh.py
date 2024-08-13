import numpy as np 
import matplotlib.pyplot as plt 
from time_conversion import read_units

unit_conversions = read_units('king')

# read king.bh.dat files; there's 2 bc simulation restart
bh_dat = np.loadtxt('king.bh.dat', unpack=True)
print('bh dat', bh_dat)
bh_dat2 = np.loadtxt('kingres1.bh.dat', unpack=True)
print('bh_dat2', bh_dat2)
time_myr = [i*unit_conversions[0][-3] for i in bh_dat[1]]
time_myr2 = [i*unit_conversions[0][-3] for i in bh_dat2[1]]

i = 0
while time_myr2[i] <= time_myr[-1]:
	i += 1
time_myr2 = time_myr2[i:]

print('Number of BHs at present day', bh_dat2[2][-1])
print('Number of single BHs at present day', bh_dat2[3][-1])
print('Number of binary BHs at present day', bh_dat2[4][-1])
print('Number of BH-BH binaries at present day', bh_dat2[5][-1])
print('Number of BH-non BH binaries at present day', bh_dat2[6][-1])
print('Number of BH-NS binaries at present day', bh_dat2[7][-1])
print('Number of BH-WD binaries at present day', bh_dat2[8][-1])
print('Number of stars w/ MSstars/giants at present day', bh_dat2[9][-1])
print('Number of BH-MS binaries at present day', bh_dat2[10][-1])
print('Number of BH-giant binaries at present day', bh_dat2[11][-1])
print('Fraction of binaries containing BH over systems containing BH at present day', bh_dat2[12][-1])


# plot number of BHs over time
plt.plot(time_myr, bh_dat[2], 'crimson')
plt.plot(time_myr2, bh_dat2[2][i:], 'crimson')
plt.xscale('log')
plt.title('CMCrv2 total number of BHs over time')
plt.xlabel('Time [Myr]')
plt.savefig('CMCrv2_BHs_over_time.png')

#plt.plot(time_myr, bh_dat[3], 'crimson')
#plt.plot(time_myr2, bh_dat2[3][i:], 'crimson')
#plt.title('Total number of single BHs over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[4], 'crimson')
#plt.plot(time_myr2, bh_dat2[4][i:], 'crimson')
#plt.title('Total number of binary BHs over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[5], 'crimson')
#plt.plot(time_myr2, bh_dat2[5][i:], 'crimson')
#plt.title('Total number of BH-BH binaries over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[6], 'crimson')
#plt.plot(time_myr2, bh_dat2[6][i:], 'crimson')
#plt.title('Total number of BH-non BH binaries over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[7], 'crimson')
#plt.plot(time_myr2, bh_dat2[7][i:], 'crimson')
#plt.title('Total number of BH-NS binaries over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[8], 'crimson')
#plt.plot(time_myr2, bh_dat2[8][i:], 'crimson')
#plt.title('Total number of BH-WD binaries over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[9], 'crimson')
#plt.plot(time_myr2, bh_dat2[9][i:], 'crimson')
#plt.title('Total number of stars with MS stars/giants over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[10], 'crimson')
#plt.plot(time_myr2, bh_dat2[10][i:], 'crimson')
#plt.title('Total number of BH-MS binaries over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[11], 'crimson')
#plt.plot(time_myr2, bh_dat2[11][i:], 'crimson')
#plt.title('Total number of BH-giant binaries over time')
#plt.xlabel('Time [Myr]')
#plt.show()

#plt.plot(time_myr, bh_dat[12], 'crimson')
#plt.plot(time_myr2, bh_dat2[12][i:], 'crimson')
#plt.title('Fraction of binaries containing BH over systems containing BH')
#plt.xlabel('Time [Myr]')
#plt.show()
