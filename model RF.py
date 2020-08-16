from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.impute import SimpleImputer
import gdal
import numpy as np

estimators = 500
cpu_cores = 4

print('Start loading data...')
df = pd.read_csv('/Users/Mattia/Desktop/Y10totB.csv', index_col=False)
print(df.head())
#print(df.columns[1:11])
print('Data has been loaded!\n')

X = df[['ASPECT', 'DEM 2', 'GEO', 'SLOPE', 'land cover', 'sumSWEabs', 'sumSWEpos']]
y = df['Y']
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
rasternames = ["/Users/Mattia/Desktop/variables500.tif"]
#'ASPECT',
#'DEM 2'
#'GEO'
#'SLOPE'
#land
#sumSWEabs
#sumSWEpos

v1 = gdal.Open(rasternames[0])

col = v1.RasterXSize
rows = v1.RasterYSize
nelem = col * rows
driver = v1.GetDriver()
print(col, ' x ', rows, ' pixels')
print(v1.RasterCount, ' bands')

val = dict()
for i in range(1, v1.RasterCount+1):
    val['val' + str(i)] = v1.GetRasterBand(i).ReadAsArray().flatten().round(2)
    val.get('val' + str(i))[np.isnan(val.get('val' + str(i)))] = 0
    #val.get('val' + str(i))[val.get('val' + str(i)) == 429957] = 0

DATA = np.stack(list(val.values()), axis=1)
print(DATA)

print('Data has been loaded!\n')

print('Start prediction...')
result = clf.predict(DATA)
resultproba = clf.predict_proba(DATA)
print('Prediction ended!\n')

for i in range(len(DATA)):
    if result[i]>0:
        print("%s ==> %s | %s" % (DATA[i], result[i], resultproba[i][1]))


plt.hist(result, bins=30, histtype='bar', ec='black', color='b')

plt.imshow((resultproba[:, 1]).reshape((rows, col))), plt.colorbar()
plt.show()

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
"""""
