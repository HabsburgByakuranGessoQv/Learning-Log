import warnings

from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize

warnings.filterwarnings('ignore')
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt

# 加载Digits数据集
digits = load_digits()
data = digits.data  # 样本数据
target = digits.target  # 标签数据
print(data.shape, target.shape)  # 输出数组形状

# 使用Matplotlib，显示前20张图片
fig = plt.figure(figsize=(8, 8), facecolor='w')
for i in range(20):
    ax = fig.add_subplot(4, 5, i + 1)
    # matshow方法将像素矩阵显示为图片
    # data中的图片像素为长度64的一维数组，需要转成8*8的二维数组来显示
    ax.matshow(data[i].reshape(8, 8))

# plt.show()

# 拆分数据集
X_train, X_test, y_train, y_test = train_test_split(data, target,
                                                    test_size=0.8, random_state=5)
print(X_train.shape, X_test.shape)

modelss = {}
modelss["rbf_kernel"] = SVC(kernel='rbf', gamma='scale')
modelss["poly_kernel"] = SVC(kernel='poly', gamma='scale')
modelss["sigmoid_kernel"] = SVC(kernel='sigmoid', gamma='scale')
modelss["linear_kernel"] = SVC(kernel='linear', gamma='scale')

# 使用不同核函数的支持向量机分类模型进行分类
print('-' * 20, '使用不同核函数的支持向量机分类模型进行分类', '-' * 20)
for key, value in modelss.items():
    model = value.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print("%s score is : %.2f" % (key, score))
    y_pred = model.predict(X_test[:20])
    print('%s验证的预测数字：' % key, y_pred)
    print('%s验证的实际数字：' % key, y_test[:20])
    print("\n")

# 正则化系数C的修改
print('-' * 20, '正则化系数C的修改', '-' * 20)
c_l = [0.01, 0.05, 0.1, 0.5, 1]
for c_e in c_l:
    print('-' * 40, 'C={}'.format(c_e), '-' * 40)
    modelss2 = {}
    modelss2["rbf_kernel"] = SVC(C=c_e, kernel='rbf', gamma='scale')
    modelss2["poly_kernel"] = SVC(C=c_e, kernel='poly', gamma='scale')
    modelss2["sigmoid_kernel"] = SVC(C=c_e, kernel='sigmoid', gamma='scale')
    modelss2["linear_kernel"] = SVC(C=c_e, kernel='linear', gamma='scale')
    for key, value in modelss2.items():
        model = value.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print("%s score is : %.2f" % (key, score))
        y_pred = model.predict(X_test[:20])
        print('%s验证的预测数字：' % key, y_pred)
        print('%s验证的实际数字：' % key, y_test[:20])
        print("\n")

# 多项式核多项式维度degree的修改
print('-' * 20, '多项式核多项式维度degree的修改', '-' * 20)
vid = [1, 3, 5, 7, 9]
for i in vid:
    model = SVC(kernel='poly', degree=i)
    model = model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print('degree = {}, score={}'.format(i, score))
    y_pred = model.predict(X_test[:20])
    print('验证的预测数字：{}'.format(y_pred))
    print('验证的实际数字：{}'.format(y_test[:20]))
    print("\n")

# 绘制 ROC 曲线
print('-' * 20, '绘制 ROC 曲线', '-' * 20)
y = label_binarize(target, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
n_classes = y.shape[1]

X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=.5, random_state=0)

classifier = OneVsRestClassifier(SVC(kernel='linear', probability=True,
                                     random_state=1))
y_score = classifier.fit(X_train, y_train).decision_function(X_test)

# 计算每一类的ROC
'''此部分循环计算了每一类分类相对于其它所有类别的真阳率tpr和假阳率fpr，并记录在响应字典值中'''
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])


# 绘制ROC曲线
plt.figure()
lw = 2

plt.plot(fpr[8], tpr[8], color='darkorange', lw=lw, label='ROC curve 8(area = %0.2f)' % roc_auc[8])
plt.plot(fpr[9], tpr[9], color='red', lw=lw, label='ROC curve 9(area = %0.2f)' % roc_auc[9])

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC CURVE')
plt.legend(loc="lower right")
plt.show()

