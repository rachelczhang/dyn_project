import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

bcm = pd.read_hdf('bcm_esc.h5', 'bcm')
bpp = pd.read_hdf('bpp_esc.h5', 'bpp')

print(bpp)

