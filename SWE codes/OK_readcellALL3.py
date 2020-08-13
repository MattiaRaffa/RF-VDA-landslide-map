import csv
import os, sys
import numpy as np

rootdir = '/Users/Mattia/PycharmProjects/gdal/weekfile'

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

with open('fileALL.csv', mode='w') as csv_file:     # creo csv ALL
    writer = csv.DictWriter(csv_file, fieldnames=IdList)
    writer.writeheader()

 # ---------------
#if listswefile[49:51]       #eliminare voce dalla lista se contiene il punto

for i in listswefile:
    SWE = np.loadtxt(i, skiprows=6)

    data = [i[44:48], i[49:51], i[52:54]]

    with open('/Users/Mattia/Desktop/SWE_VDA/2002-2018c.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            collX = int(row[11])
            rowY = int(row[12])
            newdatarow = SWE[rowY, collX]
            data.append(newdatarow)

    datarow = dict(zip(IdList, data))

    with open('fileALL.csv', mode='a', newline='') as csvALL_file:
        writer = csv.DictWriter(csvALL_file, fieldnames=datarow)
        writer.writerow(datarow)

    data = []

