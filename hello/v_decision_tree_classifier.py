import numpy as np
from sklearn import datasets
from sklearn import tree

# http://datahref.com/archives/169
iris = datasets.load_iris()

# data对应了样本的4个特征，150行4列
print(iris.data.shape)

# 显示样本特征的前5行
print(iris.data[:5])

# target对应了样本的类别（目标属性），150行1列
print(iris.target.shape)
# 显示所有样本的目标属性
print(iris.target)

test_idx = [0, 50, 100]

# training data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# testing data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)
# ground truth label of test data
print(test_target)
# the prediction of decision tree
print(clf.predict(test_data))
