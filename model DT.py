from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
from dtreeviz.trees import dtreeviz

df = pd.read_csv('/Users/Mattia/Desktop/Y10.csv', index_col = False)
print(df)

X = df[['sumSWEpos', 'sumSWEabs', 'slope', 'northness', 'mergeVDA', 'aspect', 'SWEmin', 'SWEmax', 'SWEmean']]
y = df['Y']

# Make a decision tree and train
model = DecisionTreeClassifier(random_state=500)
model.fit(X, y)
print(model)

print('Decision tree has ' + str(model.tree_.node_count) + ' nodes with maximum depth ' + str(model.tree_.max_depth))

print('Model Accuracy: ' + str(model.score(X, y)))


fig = plt.figure(dpi=500)
_= tree.plot_tree(model, filled=True, rounded=True, feature_names=df.columns[1:11],
                  class_names=('1', '0'))

plt.savefig('tree.pdf', format='pdf', bbox_inches="tight")

plt.show()


"""""

viz = dtreeviz(model, X, y, target_name="target", feature_names=['sumSWEpos', 'sumSWEabs', 'slope', 'northness', 'mergeVDA', 'aspect', 'SWEmin', 'SWEmax', 'SWEmean'],
               class_names=y.unique().tolist())

viz.view()
"""""
