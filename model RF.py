from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from collections import OrderedDict

estimators = 500
cpu_cores = 4

print('Start loading data...')
df = pd.read_csv('/Users/Mattia/Desktop/Y10totB.csv', index_col=False)
print(df.head())
#print(df.columns[1:11])
print('Data has been loaded!\n')

X = df[['sumSWEabs', 'SWEmin', 'SLOPE', 'DEM 2', 'ASPECT', 'land cover', 'GEO']]
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

print('OOB error:')
print((1 - clf.oob_score_).round(3), '\n')

print('Best importance:')
print(sorted(list(zip(clf.feature_importances_.round(2), x_train)), reverse=True), '\n')


""""
print('Calculating...')
pred_test = clf.predict(X)

print('\n')
print('Test accuracy:')
print(accuracy_score(y, pred_test).round(2), '\n')

#print first 10 trees:
fig, axes = plt.subplots(nrows=1, ncols=10, figsize=(20, 5), dpi=900)
for index in range(0, 10):
    tree.plot_tree(clf.estimators_[index],
                   feature_names=['sumSWEabs', 'slope', 'mergeVDA', 'aspect', 'SWEmin'],
                   class_names=('1', '0'),
                   filled=True,
                   rounded=True,
                   proportion=True,
                   ax=axes[index])

    axes[index].set_title('Estimator: ' + str(index), fontsize=10)
fig.savefig('rf_5trees.png')

"""