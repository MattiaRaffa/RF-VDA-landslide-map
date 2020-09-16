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

#estimators = 100
cpu_cores = 4

print('Start loading data...')
df = pd.read_csv('/Volumes/Extreme SSD/model 3 I/points Y10.csv', index_col=False)
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
    #'LANDre4_1',
    #'LANDre4_2',
    #'LANDre4_3',
    #'LANDre4_4',
    #'GEOre3_1',
    #'GEOre3_2',
    #'GEOre3_3',
    'curvatura',
    'esposizion',
    'flow_acc',
    'pendenza',
    'quote',
    'soglia_plu'
]]


y = df2['Y']
x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=20, train_size=0.8)

print('Shape of x,y train=>', x_train.shape)
print('Shape of x,y test=>', x_test.shape, '\n')

print('Start training the model...')
clf = RandomForestClassifier(verbose=True, n_jobs=cpu_cores, oob_score=True, warm_start=True)
print('RandomForestClassifier', clf.get_params())
print('Model created!\n')

#################
error_rate = {}

# Range of `n_estimators` values to explore.
min_estimators = 1
max_estimators = 250

for i in range(min_estimators, max_estimators + 1):
    clf.set_params(n_estimators=i)
    clf.fit(x_train, y_train)

    # Record the OOB error for each `n_estimators=i` setting.
    oob_error = 1 - clf.oob_score_
    error_rate[i] = oob_error

plt.plot(list(error_rate.keys()), list(error_rate.values()), color='#0c343d')

SMA = pd.Series(list(error_rate.values())).ewm(span=14, adjust=False).mean()
plt.plot(SMA, label='SMA', color='#bf9000', linestyle="--")

plt.xlim(min_estimators, max_estimators)
plt.xlabel("n_estimators")
plt.ylabel("OOB error rate")
plt.grid(True)
plt.show()
################

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
rasternames = ["/Volumes/Extreme SSD/model 3 I/variables I.tif"]

v1 = gdal.Open(rasternames[0])

col = v1.RasterXSize
rows = v1.RasterYSize
nelem = col * rows
driver = v1.GetDriver()
print(col, ' x ', rows, ' pixels')
print(v1.RasterCount, ' bands')


v1val = v1.GetRasterBand(1).ReadAsArray().flatten() #curvatura
v2val = v1.GetRasterBand(2).ReadAsArray().flatten() #esposizion
v3val = v1.GetRasterBand(3).ReadAsArray().flatten() #flow_acc
v4val = v1.GetRasterBand(4).ReadAsArray().flatten() #pendenza
v5val = v1.GetRasterBand(5).ReadAsArray().flatten() #quote
v6val = v1.GetRasterBand(6).ReadAsArray().flatten() #soglia_plu
#v7val = v1.GetRasterBand(7).ReadAsArray().flatten() #GEO
#v8val = v1.GetRasterBand(8).ReadAsArray().flatten() #LAND
#v1.GetRasterBand(4).GetNoDataValue()


v1val[v1val==-9999] = 0
v2val[v2val==0] = 0
v3val[v3val==0] = 0
v4val[v4val==-0] = 0
v5val[v5val==0] = 0
v6val[v6val==0] = 0
#v7val[v7val==-9999] = 0
#v8val[v8val==0] = 0
#plt.imshow(v5val)

DATA = np.stack((v1val.flatten(),
                 v2val.flatten(),
                 v3val.flatten(),
                 v4val.flatten(),
                 v5val.flatten(),
                 v6val.flatten()), axis=1)
                 #v7val.flatten(),
                 #v8val.flatten(), axis=1)

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