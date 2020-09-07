from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
import gdal
import numpy as np

estimators = 100
cpu_cores = 4

print('Start loading data...')
df = pd.read_csv('/Users/Mattia/Desktop/v3 model/train Y10 v3 filled B.csv', index_col=False)
print(df.head())

############
OHE = OneHotEncoder(sparse=False)
OHE.fit(df[['LANDre4', 'GEOre3']])
OH_encoded = OHE.transform(df[['LANDre4', 'GEOre3']])
feature_names = OHE.get_feature_names(['LANDre4', 'GEOre3'])

df2 = pd.concat([df.select_dtypes(exclude='object'),
               pd.DataFrame(OH_encoded, columns=feature_names).astype(int)], axis=1)

print(feature_names)
print(df2)
###############

#print(df.columns[1:11])
print('Data has been loaded!\n')

X = df2[[
    #ASPECT,
    'DEM 2',
    #'GEOre3',
    #'LANDre4',
    'SLOPE',
    #'SWEmean',
    'SWEmin',
    'eventi sci',
    'sogliaplu'
    #'sumSWEabs',
    #'sumSWEpos'
]]


y = df2['Y']
x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=20, train_size=0.8)

print('Shape of x,y train=>', x_train.shape)
print('Shape of x,y test=>', x_test.shape, '\n')

print('Start training the model...')
clf = RandomForestClassifier(n_estimators=estimators, verbose=True, n_jobs=cpu_cores, oob_score=True)
print('RandomForestClassifier', clf.get_params())
clf.fit(x_train, y_train)
print('Model created!\n')

print('Calculating...')

# Evaluating on Training set
pred_train = clf.predict(x_train)
print('Training Set F1-Score=>', f1_score(y_train, pred_train).round(3), '\n')

# Evaluating on Test set
pred_test = clf.predict(x_test)
print('Testing Set F1-Score=>', f1_score(y_test, pred_test).round(3), '\n')

print('Final OOB error:')
print((1 - clf.oob_score_).round(3), '\n')

print('Best importance:')
print(sorted(list(zip(clf.feature_importances_.round(2), x_train)), reverse=True), '\n')


print('Calculating...')
pred_test = clf.predict(X)

print('\n')
print('Test accuracy:')
print(accuracy_score(y, pred_test).round(2), '\n')


################
print('Start loading raster arrays...')
#
rasternames = ["/Users/Mattia/Desktop/v3 model/variables 100.tif"]
#"/Volumes/Extreme SSD/variables 2.tif"
#"/Users/Mattia/Desktop/variables500.tif"

v1 = gdal.Open(rasternames[0])

col = v1.RasterXSize
rows = v1.RasterYSize
nelem = col * rows
driver = v1.GetDriver()
print(col, ' x ', rows, ' pixels')
print(v1.RasterCount, ' bands')

val = dict()
for i in range(1, v1.RasterCount+1):
    val['val' + str(i)] = v1.GetRasterBand(i).ReadAsArray().flatten()
    val.get('val' + str(i))[np.isnan(val.get('val' + str(i)))] = 0
    #val.get('val' + str(i))[val.get('val' + str(i)) == 429957] = 0
    
DATA = np.stack(list(val.values()), axis=1)


#v1val = v1.GetRasterBand(1).ReadAsArray().flatten() #ASPECT
v2val = v1.GetRasterBand(2).ReadAsArray().flatten() #DEM
#v3val = v1.GetRasterBand(3).ReadAsArray().flatten() #GEO
#v4val = v1.GetRasterBand(4).ReadAsArray().flatten() #LAND
v5val = v1.GetRasterBand(5).ReadAsArray().flatten() #SLOPE
#v6val = v1.GetRasterBand(6).ReadAsArray().flatten() #SWEmean
v7val = v1.GetRasterBand(7).ReadAsArray().flatten() #SWEmin
v8val = v1.GetRasterBand(8).ReadAsArray().flatten() #eventi
v9val = v1.GetRasterBand(9).ReadAsArray().flatten() #soglia
#v10val = v1.GetRasterBand(10).ReadAsArray().flatten() #sumSWE abs
#v11val = v1.GetRasterBand(11).ReadAsArray().flatten() #sumSWE
#v1.GetRasterBand(4).GetNoDataValue()


#v1val[v1val==-9999] = None
v2val[v2val==0] = 0
#v3val[v3val==0] = 0
#v4val[v4val==-0] = 0
v5val[v5val==0] = 0
#v6val[v6val==0] = None
v7val[v7val==-9999] = 0
v8val[v8val==0] = 0
v9val[v9val==-9999] = 0
#v10val[v10val==-9999] = None
#v11val[v11val==-9999] = 0
#plt.imshow(v5val)

DATA = np.stack((#v1val.flatten(),
                 v2val.flatten(),
                 #v3val.flatten(),
                 #v4val.flatten(),
                 v5val.flatten(),
                 #v6val.flatten(),
                 v7val.flatten(),
                 v8val.flatten(),
                 v9val.flatten()), axis=1)
                 #v10val.flatten(),
                 #v11val.flatten(),


print('Data has been loaded!\n')

print('Start prediction...')
result = clf.predict(DATA)
resultproba = clf.predict_proba(DATA)
print('Prediction ended!\n')

"""
for i in range(len(DATA)):
    if result[i]>0:
        print("%s ==> %s | %s" % (DATA[i], result[i], resultproba[i][1]))

"""
print('Plotting...')
plt.hist(result, bins=30, histtype='bar', ec='black', color='b')

plt.imshow((resultproba[:, 1]).reshape((rows, col))), plt.colorbar()
plt.show()


print('Writing TIF...')
# write_result

pca1 = driver.Create("RFproba1" + ".tif", col, rows, 1, gdal.GDT_Float32)

# Write metadata
pca1.SetGeoTransform(v1.GetGeoTransform())
pca1.SetProjection(v1.GetProjection())

pca1dataarray = (resultproba[:, 1])
pca1dataarray[pca1dataarray == None] = -9999

pca1.GetRasterBand(1).WriteArray(pca1dataarray.reshape(rows, col))
pca1.GetRasterBand(1).SetNoDataValue(-9999)

pca1 = None
del pca1
print('DONE!')

"""
#print first 10 trees:
fig, axes = plt.subplots(nrows=1, ncols=10, figsize=(20, 5), dpi=900)
for index in range(0, 10):
    tree.plot_tree(clf.estimators_[index],
                   feature_names=['sumSWEabs', 'SWEmin', 'SLOPE', 'DEM 2', 'ASPECT', 'land cover', 'GEO'],
                   class_names=('1', '0'),
                   filled=True,
                   rounded=True,
                   proportion=True,
                   ax=axes[index])

    axes[index].set_title('Estimator: ' + str(index), fontsize=10)
fig.savefig('rf_5trees.png')
"""
