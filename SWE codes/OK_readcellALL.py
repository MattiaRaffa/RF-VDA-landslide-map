import csv
import os, sys
import numpy as np


rootdir = '/Users/Mattia/PycharmProjects/gdal/weekfile'
listswefile = []
# creo lista con i file dei mesi
for root, dirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith((".asc")):
            listswefile.append(root + '/' + name)

with open('fileALL.csv', mode='w') as csv_file:
    coll = ['year', 'month', 'day']
    writer = csv.DictWriter(csv_file, fieldnames=coll)
    writer.writeheader()

for i in listswefile:
    with open('fileALL.csv', mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=coll)
        writer.writerow({'year': i[44:48],
                         'month': i[49:51],
                         'day': i[52:54]})

n = 0
# leggo il CSV
with open('/Users/Mattia/Desktop/SWE_VDA/2002-2018c.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        Id = row[1]
        collX = int(row[11])
        rowY = int(row[12])

        for i in listswefile:
            # estrarre valori row-col
            SWE = np.loadtxt(i, skiprows=6)

            v = open('fileALL.csv')
            r = csv.reader(v)
            row0 = next(r)
            row0.append(Id)
            for item in r:
                item.append(SWE[rowY, collX])

            n += 1