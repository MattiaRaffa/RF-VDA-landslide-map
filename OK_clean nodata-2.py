import os, sys
import numpy as np

head ="""\
ncols   177
nrows    114
XLLCORNER 329181.84817857
YLLCORNER 5036669.44714769
CELLSIZE 500
NODATA_VALUE -9999"""

rootdir = '/Users/Mattia/PycharmProjects/gdal/cleanfile'
listfile = []

for root, dirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith((".asc")):
            listfile.append(root + '/' + name)

for i in listfile:
    grid1 = np.loadtxt(i, skiprows=6)

    grid1[grid1 < -100] = np.nan
    grid1[np.isnan(grid1)] = 9999
    grid1[grid1 < 0] = 0
    grid1[grid1 == 9999] = np.nan
    grid1[np.isnan(grid1)] = -9999
    np.savetxt(str((i)[45:55]) +'-positive.asc', grid1, header=head, fmt="%1.2f", comments='')