# 步骤一、加载、查看鸢尾花数据集
# sklearn库中有现成的鸢尾花数据集可以直接调用

import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz, DecisionTreeRegressor
import graphviz

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

import warnings

warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

iris = load_iris()  # 准备数据集
features = iris.data  # 获取特征集
labels = iris.target  # 获取目标集
# 将鸢尾花特征与数据添加在一起
iris_dataset = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_dataset['label'] = iris.target
print(iris_dataset.head())

# 拆步骤二、数据处理及拆分

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=0)
print(X_train.shape, X_test.shape)  # 查看拆分结果

# 建立模型
model_CE2 = DecisionTreeClassifier(criterion="entropy", max_depth=2).fit(X_train, y_train)
model_CE5 = DecisionTreeClassifier(criterion="entropy", max_depth=5).fit(X_train, y_train)
model_CG2 = DecisionTreeClassifier(criterion="gini", max_depth=2).fit(X_train, y_train)
model_CG5 = DecisionTreeClassifier(criterion="gini", max_depth=5).fit(X_train, y_train)
model_RS = DecisionTreeRegressor(criterion="squared_error").fit(X_train, y_train)
model_RA = DecisionTreeRegressor(criterion="absolute_error").fit(X_train, y_train)
model_RR2 = RandomForestRegressor(n_estimators=20)
model_RR2.fit(X_train, y_train)
model_RR5 = RandomForestRegressor(n_estimators=50)
model_RR5.fit(X_train, y_train)

print('---------------\t决策树\t---------------')
# 评估模型（分类模型输出准确率，回归模型输出R2_score）
print('entropy max_depth=2:\ntest_score:', model_CE2.score(X_test, y_test))
# 预测测试集中的鸢尾花种类
y_predCE2 = model_CE2.predict(X_test)
n = 10  # 显示前n个样本的预测年龄，并与实际年龄作对比
print('预测种类：', np.round(y_predCE2[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])
# 评估模型（分类模型输出准确率，回归模型输出R2_score）
print('entropy max_depth=5:\ntest_score:', model_CE5.score(X_test, y_test))
# 预测测试集中的鸢尾花种类
y_predCE5 = model_CE5.predict(X_test)
n = 10  # 显示前n个样本的预测年龄，并与实际年龄作对比
print('预测种类：', np.round(y_predCE5[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])

print('\ngini max_depth=2:\ntest_score:', model_CG2.score(X_test, y_test))
y_predCG2 = model_CG2.predict(X_test)
print('预测种类：', np.round(y_predCG2[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])
print('gini max_depth=5:\ntest_score:', model_CG5.score(X_test, y_test))
y_predCG5 = model_CG5.predict(X_test)
print('预测种类：', np.round(y_predCG5[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])

# 评估模型（分类模型输出准确率，回归模型输出R2_score）
print('\nsquared_error:\ntest_score:', model_RS.score(X_test, y_test))
# 预测测试集中的鸢尾花种类
y_predRS = model_RS.predict(X_test)
n = 10  # 显示前n个样本的预测年龄，并与实际年龄作对比
print('预测种类：', np.round(y_predRS[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])

# 评估模型（分类模型输出准确率，回归模型输出R2_score）
print('absolute_error:\ntest_score:', model_RA.score(X_test, y_test))
# 预测测试集中的鸢尾花种类
y_predRA = model_RA.predict(X_test)
n = 10  # 显示前n个样本的预测年龄，并与实际年龄作对比
print('预测种类：', np.round(y_predRA[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])

print('---------------\t随机森林\t---------------')
# 评估模型（分类模型输出准确率，回归模型输出R2_score）
print('RandomForestRegressor 20:\ntest_score:', model_RR2.score(X_test, y_test))
# 预测测试集中的鸢尾花种类
y_predRR2 = model_RR2.predict(X_test)
n = 10  # 显示前n个样本的预测年龄，并与实际年龄作对比
print('预测种类：', np.round(y_predRR2[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])
# 评估模型（分类模型输出准确率，回归模型输出R2_score）
print('RandomForestRegressor 50:\ntest_score:', model_RR5.score(X_test, y_test))
# 预测测试集中的鸢尾花种类
y_predRR5 = model_RR5.predict(X_test)
n = 10  # 显示前n个样本的预测年龄，并与实际年龄作对比
print('预测种类：', np.round(y_predRR5[:n]))  # np.round()-四舍五入取整
print('实际种类：', y_test[:n])

# 可视化预测曲线
plt.figure(figsize=(12, 4))  # 图像尺寸
plt.title('DecisionTreeClassifier CE2')  # 标题
num = 50  # 图中显示样本的数量
plt.subplot()
plt.plot(np.arange(num), y_predCE2[:num], label='决策树CE2')  # 预测值
plt.plot(np.arange(num), y_test[:num], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

# 可视化预测曲线
plt.figure(figsize=(12, 4))  # 图像尺寸
plt.title('DecisionTreeClassifier CE5')  # 标题
num = 50  # 图中显示样本的数量
plt.subplot()
plt.plot(np.arange(num), y_predCE5[:num], label='决策树 CE5')  # 预测值
plt.plot(np.arange(num), y_test[:num], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

# 可视化预测曲线
plt.figure(figsize=(12, 4))  # 图像尺寸
plt.title('DecisionTreeClassifier CG2')  # 标题
num = 50  # 图中显示样本的数量
plt.subplot()
plt.plot(np.arange(num), y_predCG2[:num], label='决策树 CG2')  # 预测值
plt.plot(np.arange(num), y_test[:num], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

# 可视化预测曲线
plt.figure(figsize=(12, 4))  # 图像尺寸
plt.title('DecisionTreeClassifier CG5')  # 标题
num = 50  # 图中显示样本的数量
plt.subplot()
plt.plot(np.arange(num), y_predCG5[:num], label='决策树 CG5')  # 预测值
plt.plot(np.arange(num), y_test[:num], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

# 可视化预测曲线
plt.figure(figsize=(12, 4))  # 图像尺寸
plt.title('DecisionTreeRegressor RS')  # 标题
num = 50  # 图中显示样本的数量
plt.subplot()
plt.plot(np.arange(num), y_predRS[:num], label='决策树 RS')  # 预测值
plt.plot(np.arange(num), y_test[:num], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

# 可视化预测曲线
plt.figure(figsize=(12, 4))  # 图像尺寸
plt.title('DecisionTreeRegressor RA')  # 标题
num = 50  # 图中显示样本的数量
plt.subplot()
plt.plot(np.arange(num), y_predRA[:num], label='决策树 RA')  # 预测值
plt.plot(np.arange(num), y_test[:num], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

plt.figure(figsize=(12, 4))  # 图像尺寸
plt.subplot()
plt.title('RandomForestRegressor 2')  # 标题
plt.plot(np.arange(n), y_predRR2[:n], label='随机森林 2')  # 预测值
plt.plot(np.arange(n), y_test[:n], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()

plt.figure(figsize=(12, 4))  # 图像尺寸
plt.subplot()
plt.title('RandomForestRegressor 5')  # 标题
plt.plot(np.arange(n), y_predRR5[:n], label='随机森林 5')  # 预测值
plt.plot(np.arange(n), y_test[:n], label='true')  # 实际值
plt.legend()  # 显示图例
plt.show()


# 查看决策树图像
# 在本地环境中安装graphviz，pip install graphviz
# 需要在graphviz官网下载graphviz软件并安装，安装完成后配置此电脑环境变量即可查看决策树生成的pdf
dot_data = export_graphviz(model_CE5)
graph = graphviz.Source(dot_data)
# 生成 Source.gv.pdf 文件，并打开
graph.view()