import csv
import os, sys
import numpy as np


rootdir = '/Users/Mattia/PycharmProjects/gdal/files'
listfile = []

for root, dirs, files in os.walk(rootdir):
    for name in files:
        listfile.append(root + '/' + name)

listswefile = []

with open('file2.csv', mode='w') as csv_file:
    coll = ['year', 'month', 'day', 'SWE0', 'SWE1', 'SWE2', 'SWE3']
    writer = csv.DictWriter(csv_file, fieldnames=coll)
    writer.writeheader()

# leggo il CSV
with open('/Users/Mattia/Desktop/SWE_VDA/2002-2018c.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        fid = str(row[1])
        year = str(row[6])
        month = str(row[5])
        day = row[4]
        collX = int(row[11])
        rowY = int(row[12])
        print(year + '_' + month.zfill(2) + '_' + day.zfill(2))

        # creo lista con i file dei mesi
        for root, dirs, files in os.walk(rootdir):
            for name in files:
                if name.startswith((str(year + '_' + month.zfill(2)))):
                    listswefile.append(root + '/' + name)
        # continua solo se la lista è piena
        if len(listswefile) > 0:
            print('file del mese')
            print(listswefile)
            # trovo quale delle settimane e' piu' vicina
            n = 0
            fileday = []
            for i in listswefile:
                resto = int((listswefile[n][49:51].strip('0'))) - int(day.strip('0'))
                #print((listswefile[n][42:44].strip('0')) + '%' + day.strip('0'))
                fileday.append(np.absolute(resto))
                n += 1
            print(fileday)
            pos = fileday.index(min(fileday))
            print(pos)
            print(listswefile[pos])

            # cerco nella lista il file nominato e richiamo i 3 file precedenti
            # if listswefile[pos] in listfile:
            fileSWE0 = (listfile.index(listswefile[pos]))
            fileSWE1 = fileSWE0 - 1
            fileSWE2 = fileSWE0 - 2
            fileSWE3 = fileSWE0 - 3

            # reset lista dei mesi
            listswefile = []

            # estrarre valori row-col
            SWE0 = np.loadtxt(listfile[fileSWE0], skiprows=6)
            SWE1 = np.loadtxt(listfile[fileSWE1], skiprows=6)
            SWE2 = np.loadtxt(listfile[fileSWE2], skiprows=6)
            SWE3 = np.loadtxt(listfile[fileSWE3], skiprows=6)

            # scriverli in un csv
            with open('file2.csv', mode='a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=coll)
                writer.writerow({'fid': fid,
                                 'month': month,
                                 'day': day,
                                 'SWE0': SWE0[rowY, collX],
                                 'SWE1': SWE1[rowY, collX],
                                 'SWE2': SWE2[rowY, collX],
                                 'SWE3': SWE3[rowY, collX]})