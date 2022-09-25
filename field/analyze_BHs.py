import numpy as np 
import matplotlib.pyplot as plt 

bpp = open('bpp.txt', 'r')
bpp_data = []
for i in bpp.readlines(): 
	x = i.split(' ')
	bpp_data.append(x)
print('bpp data', bpp_data)
#bpp_filt = bpp[['tphys', 'kstar_1', 'kstar_2', 'evol_type']]

#print(bpp_filt)
