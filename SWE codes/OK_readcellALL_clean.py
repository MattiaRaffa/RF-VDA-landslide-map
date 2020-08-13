import csv
import os, sys
import numpy as np

rootdir = '/Users/Mattia/PycharmProjects/gdal/cleanfile'

listswefile = []

for root, dirs, files in os.walk(rootdir):          # creo lista con i file dei mesi
    for name in files:
        if name.endswith((".asc")):
            listswefile.append(root + '/' + name)

IdList=['year', 'month', 'day']                                     #
with open('/Users/Mattia/Desktop/SWE_VDA/2002-2018c.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        Id = row[1]
        IdList.append(Id)

with open('fileALL_clean.csv', mode='w') as csv_file:     # creo csv ALL
    writer = csv.DictWriter(csv_file, fieldnames=IdList)
    writer.writeheader()

for i in listswefile:
    SWE = np.loadtxt(i, skiprows=6)

    data = [i[45:49], i[50:52], i[53:55]]

    with open('/Users/Mattia/Desktop/SWE_VDA/2002-2018c.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            collX = int(float(row[11]))
            rowY = int(float(row[12]))
            newdatarow = SWE[rowY, collX]
            data.append(newdatarow)

    datarow = dict(zip(IdList, data))

    with open('fileALL_clean.csv', mode='a', newline='') as csvALL_file:
        writer = csv.DictWriter(csvALL_file, fieldnames=datarow)
        writer.writerow(datarow)

    data = []

