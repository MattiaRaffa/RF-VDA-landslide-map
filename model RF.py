from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt

estimators = 5000
cpu_cores = 4

print('Start loading data...')
df = pd.read_csv('/Users/Mattia/Desktop/Y10.csv', index_col=False)
print(df.head())
#print(df.columns[1:11])
print('Data has been loaded!\n')

X = df[['sumSWEpos', 'sumSWEabs', 'slope', 'northness', 'mergeVDA', 'aspect', 'SWEmin', 'SWEmax', 'SWEmean']]
y = df['Y']
#x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=20, train_size=0.8)


print('Start training the model...')
clf = RandomForestClassifier(n_estimators=estimators, verbose=True, n_jobs=cpu_cores, oob_score=True, warm_start=True)
print('RandomForestClassifier', clf.get_params())
clf.fit(X, y)
print('Model created!\n')

print('Calculating...')
pred_test = clf.predict(X)

print('\n')
print('Test accuracy:')
print(accuracy_score(y, pred_test).round(2), '\n')

print('Best importance scores:')
print(sorted(list(zip(clf.feature_importances_.round(2), X)), reverse=True))
