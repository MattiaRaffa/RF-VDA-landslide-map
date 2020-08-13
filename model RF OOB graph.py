from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

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
clf = RandomForestClassifier(verbose=True, oob_score=True, warm_start=True)
#print('RandomForestClassifier', clf.get_params())

error_rate = {}

# Range of `n_estimators` values to explore.
min_estimators = 10
max_estimators = 500

for i in range(min_estimators, max_estimators + 1):
    clf.set_params(n_estimators = i)
    clf.fit(x_train, y_train)

    # Record the OOB error for each `n_estimators=i` setting.
    oob_error = 1 - clf.oob_score_
    error_rate[i] = oob_error

for data_dict in error_rate.values():
   plt.plot(list(error_rate.keys()), list(error_rate.values()))

plt.xlim(min_estimators, max_estimators)
plt.xlabel("n_estimators")
plt.ylabel("OOB error rate")
plt.show()
