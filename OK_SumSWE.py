import numpy as np
import os, sys

rootdir = '/Users/Mattia/Desktop/SWE_VDA/positive delta'
listfile = []

for root, dirs, files in os.walk(rootdir):
    for name in files:
            listfile.append(root + '/' + name)

print(listfile)

header ="""\
ncols   177
nrows    114
XLLCORNER 329181.84817857
YLLCORNER 5036669.44714769
CELLSIZE 500
NODATA_VALUE 9999"""


n=1
for i in listfile:
    grid2 = np.loadtxt(listfile[n], skiprows=6)
    grid1 = np.absolute(np.loadtxt('/Users/Mattia/PycharmProjects/gdal/sumSWEabs.txt', skiprows=6))
    sub_results = np.absolute(grid2 < 9999) + grid1
    np.savetxt('sumSWEabs' +'.asc', sub_results, header=header, fmt="%1.2f", comments='')
    n += 1