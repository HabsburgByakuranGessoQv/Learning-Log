# 1.导入数据
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
                'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli',
                'Mitoses', 'Class']
dataFrame = pd.read_csv("./2/breast-cancer-wisconsin.data", names=column_names)
headdata = dataFrame.head()
print(headdata)

# 2.数据预处理
print(dataFrame.shape)

# 将?替换成标准缺失值表示
dataFrame = dataFrame.replace('?', value=np.nan)
# 丢弃带有缺失值的数据
dataFrame = dataFrame.dropna(how='any')
print(dataFrame.shape)

# 3.准备训练测试数据

# 数据中第一列到第九列为输入X
X = dataFrame[column_names[1:10]]
# 第十列为标签y
y = dataFrame[column_names[10]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 4. 标准化数据

# 标准化数据，保证每个维度的特征数据方差为1，均值为0。使得预测结果不会被某些维度过大的特征值而主导
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


plan = [0.01, 0.1, 1.0]
for i in plan:
    # 调用linear_model.LogisticRegression模型进行建模
    # 调用fit函数训练模型，确定参数
    print('-' * 20, 'C = {}'.format(i), '-' * 20)
    model2 = LogisticRegression(C=i)
    model2.fit(X_train, y_train)

    # 训练后模型截距
    print('训练后模型截距')
    print(model2.intercept_)

    # 训练后模型权重
    print('训练后模型权重')
    print(model2.coef_)

    m = model2.coef_
    b = model2.intercept_

    # 调用predict函数进行预测，得到y_predict，并打印出y_predict
    print('打印出y_predict:', end=' ')
    y_predict = model2.predict(X_test)
    print(model2.predict(X_test))

    # 输出测试个数和预测正确的个数
    score2 = model2.score(X_test, y_test)
    print('测试个数: {}\t预测正确个数: {}'.format(len(X_test), int(len(y_predict)*score2)))

    # 查看查准率和查重率
    print(classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"]))

    # 性能分析
    print(r'使用.score函数计算X和y之间的拟合度并打印拟合度(性能分析): ', end=' ')
    print(score2)

    kfold = KFold(n_splits=10)
    score = 0
    for train_index, test_index in kfold.split(X):
        # train_index 就是分类的训练集的下标，test_index 就是分配的验证集的下标
        train_x, test_x = X.iloc[train_index], X.iloc[test_index]
        train_y, test_y = y.iloc[train_index], y.iloc[test_index]
        # 训练本组的数据，并计算准确率
        model2.fit(train_x, train_y)
        prediction = model2.predict(test_x)
        score += model2.score(test_x, test_y)

    print("模型的平均精确率为：", score / 10)

# 调用linear_model.LogisticRegression模型进行建模
# 调用fit函数训练模型，确定参数
print('-' * 20, 'C = auto', '-' * 20)
model2 = LogisticRegressionCV()
model2.fit(X_train, y_train)

# 训练后模型截距
print('训练后模型截距')
print(model2.intercept_)

# 训练后模型权重
print('训练后模型权重')
print(model2.coef_)

m = model2.coef_
b = model2.intercept_

# 调用predict函数进行预测，得到y_predict，并打印出y_predict
print('打印出y_predict:', end=' ')
y_predict = model2.predict(X_test)
print(model2.predict(X_test))

# 输出测试个数和预测正确的个数
score2 = model2.score(X_test, y_test)
print('测试个数: {}\t预测正确个数: {}'.format(len(X_test), int(len(y_predict)*score2)))

# 查看查准率和查重率
print(classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"]))

# 性能分析
print(r'使用.score函数计算X和y之间的拟合度并打印拟合度(性能分析): ', end=' ')
print(score2)

kfold = KFold(n_splits=10)
score = 0
for train_index, test_index in kfold.split(X):
    # train_index 就是分类的训练集的下标，test_index 就是分配的验证集的下标
    train_x, test_x = X.iloc[train_index], X.iloc[test_index]
    train_y, test_y = y.iloc[train_index], y.iloc[test_index]
    # 训练本组的数据，并计算准确率
    model2.fit(train_x, train_y)
    prediction = model2.predict(test_x)
    score += model2.score(test_x, test_y)

print("模型的平均精确率为：", score / 10)

