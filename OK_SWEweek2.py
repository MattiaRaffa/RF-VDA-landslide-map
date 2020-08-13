import numpy as np
import os, sys

rootdir = '/Users/Mattia/Desktop/SWE_VDA/SWE_GOLD'
print(os.listdir(rootdir))
listfile = []

for root, dirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith(("SWE_sca.asc")):
            listfile.append(root + '/' + name)

print(listfile)

header ="""\
ncols   177
nrows    114
XLLCORNER 329181.84817857
YLLCORNER 5036669.44714769
CELLSIZE 500
NODATA_VALUE None"""

n=0
for i in listfile:
    grid2 = np.loadtxt(listfile[n+1], skiprows=6)
    grid1 = np.loadtxt(listfile[n], skiprows=6)
    #grid2[grid2 < 9999] = np.nan
    #sub_results = (grid2 > -999)-grid1
    subm = int(listfile[n+1][49:51]) - int(listfile[n][49:51])
    if subm <= 1:                           #do not create file with big month jump
        grid2[grid2 == -9999] = None      #none value set (nan QGIS not recognised)
        sub_results = grid2 - grid1
        np.savetxt(listfile[n+1][44:54] +'.asc', sub_results, header=header, fmt="%1.2f", comments='')
    n += 1

#https: // pythontic.com / numpy / ndarray / subtract
#http://geospatialpython.com/2013/12/python-and-elevation-data-ascii-grid.html
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
#https://www.w3resource.com



