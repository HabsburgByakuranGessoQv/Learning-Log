from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB  # 引入各种朴素贝叶斯分类器
from sklearn.model_selection import train_test_split
from IPython.display import display
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import numpy as np

banknote = pd.read_csv(r'E:\STUDYCONTENT\Pycharm\JiQiXueXi\实验4 banknote.csv')
banknote.columns = ['特征0', '特征1', '特征2', '特征3', 'class']
display(banknote)

# 获得样本特征数组data
data = banknote.values[:, 0:4]

# 获得样本标签数组target
target = banknote.values[:, -1]

print(data.shape)  # 查看样本特征数组形状
print(target.shape)  # 查看样本标签数组形状

# 数据集拆分
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state=0)

print(X_train.shape, X_test.shape)  # 查看拆分结果

# 归一化,由于多项式朴素贝叶斯不接受负值的输入，所以需要使用MinMaxScaler对其进行归一化
mms = MinMaxScaler().fit(X_train)
Xtrain = mms.transform(X_train)
Xtest = mms.transform(X_test)

# 创建贝叶斯分类器，输出模型在训练集和测试集上的准确率
print('-*-'*20, 'BernoulliNB', '-*-'*20)
model1 = BernoulliNB()
model1.fit(X_train, y_train)
score1 = model1.score(X_test, y_test)
print(r'创建贝叶斯分类器，输出模型在训练集和测试集上的准确率', end=':')
print(score1)

num = 10  # 显示的样本数量
y_pred1 = model1.predict(X_test)
print('y_pred:', y_pred1[:num])  # 预测结果
print('y_true:', y_test[:num])  # 实际结果
y_proba = model1.predict_proba(X_test[:num])  # 预测结果的概率（每个样本为真钞和假钞的概率）
print(np.around(y_proba, decimals=3))


print('-*-'*20, 'GaussianNB', '-*-'*20)
model2 = GaussianNB()
model2.fit(X_train, y_train)
score2 = model2.score(X_test, y_test)
print(r'创建贝叶斯分类器，输出模型在训练集和测试集上的准确率', end=':')
print(score2)

num = 10  # 显示的样本数量
y_pred2 = model2.predict(X_test)
print('y_pred:', y_pred2[:num])  # 预测结果
print('y_true:', y_test[:num])  # 实际结果
y_proba = model2.predict_proba(X_test[:num])  # 预测结果的概率（每个样本为真钞和假钞的概率）
print(np.around(y_proba, decimals=3))


print('-*-'*20, 'MultinomialNB', '-*-'*20)
MinMaxScaler()
model3 = MultinomialNB()
model3.fit(X_train, y_train)
score3 = model3.score(X_test, y_test)
print(r'创建贝叶斯分类器，输出模型在训练集和测试集上的准确率', end=':')
print(score3)

num = 10  # 显示的样本数量
y_pred3 = model3.predict(X_test)
print('y_pred:', y_pred3[:num])  # 预测结果
print('y_true:', y_test[:num])  # 实际结果
y_proba = model3.predict_proba(X_test[:num])  # 预测结果的概率（每个样本为真钞和假钞的概率）
print(np.around(y_proba, decimals=3))


print('-*-'*20, 'ComplementNB', '-*-'*20)
model4 = ComplementNB()
model4.fit(X_train, y_train)
score4 = model4.score(X_test, y_test)
print(r'创建贝叶斯分类器，输出模型在训练集和测试集上的准确率', end=':')
print(score4)

num = 10  # 显示的样本数量
y_pred4 = model4.predict(X_test)
print('y_pred:', y_pred4[:num])  # 预测结果
print('y_true:', y_test[:num])  # 实际结果
y_proba = model4.predict_proba(X_test[:num])  # 预测结果的概率（每个样本为真钞和假钞的概率）
print(np.around(y_proba, decimals=3))