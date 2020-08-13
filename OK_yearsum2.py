import numpy as np
import os, sys

head ="""\
ncols   177
nrows    114
XLLCORNER 329181.84817857
YLLCORNER 5036669.44714769
CELLSIZE 500
NODATA_VALUE -9999"""

rootdir = '/Users/Mattia/PycharmProjects/gdal/GOLD clean'

listyearfile = []
y = 2002

for y in range(2002, 2020):
    listyearfile = []

    dirfix = str(y) + '-' + str(y + 1) + '.asc'     #create file zero to sum
    ReadTxtFile = open("zero.txt", "r")
    txtContent = ReadTxtFile.read();
    f = open(dirfix, "w+")
    f.write(txtContent)
    f.close()

    for m in range(11, 13):     #just for 11-13 month
        for root, dirs, files in os.walk(rootdir):
            for name in files:
                if name.startswith(str(y) + '_' + str(m)):
                    listyearfile.append(name)

    for m2 in range(1, 6):      #just for 1-6 month
        for root, dirs, files in os.walk(rootdir):
            for name2 in files:
                if name2.startswith(str(y+1) + '_' + str(m2).zfill(2)):
                    listyearfile.append(name2)

    print(listyearfile)

    for i in listyearfile:
        dir = rootdir + '/' + i

        grid = np.loadtxt(dir, skiprows=6)
        grid[grid == -9999] = np.nan

        yearfile = np.loadtxt(dirfix, skiprows=6)       #iterative sum on "zero" file
        sub_results = grid + yearfile

        sub_results[np.isnan(sub_results)] = -9999

        np.savetxt(dirfix, sub_results, header=head, fmt="%1.2f", comments='')

    y += 1