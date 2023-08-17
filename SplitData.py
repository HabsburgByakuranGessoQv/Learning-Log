import os
from sklearn.model_selection import train_test_split
import shutil

classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

base_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\flowersPlus'
test_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\datasets\val'
train_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\datasets\train'
# train_sets, test_sets = [], []


for type_path in test_path, train_path:
    print(type_path)
    for clean in classes:
        clean_path = os.path.join(type_path, clean)
        if not os.path.exists(clean_path):
            os.mkdir(clean_path)
        else:
            shutil.rmtree(clean_path)
            os.mkdir(clean_path)

for category in classes:
    photo_path = os.path.join(base_path, category)
    test_det = os.path.join(test_path, category)
    train_det = os.path.join(train_path, category)
    photo_name = os.listdir(photo_path)
    # cls_id = classes.index(category)  # 种类的index
    # data:需要进行分割的数据集
    # random_state:设置随机种子，保证每次运行生成相同的随机数
    # test_size:将数据分割成训练集的比例
    train_set, test_set = train_test_split(photo_name, test_size=0.2, random_state=42)  # 42 47 52 57 62
    print(len(train_set), len(test_set))
    # train_sets = train_set + train_sets
    # test_sets = test_set + test_sets
    trn, ten = 0, 0
    for train_name in train_set:
        _, postfix = os.path.splitext(train_name)
        if postfix not in ['.jpg', '.png', '.jpeg', '.tif']:
            continue
        raw_train_path = os.path.join(photo_path, train_name)
        shutil.copy(raw_train_path, train_det)
        # with open("cls_train.txt", 'a') as tr:
        #     trn += 1
        #     tr.write(str(cls_id) + ";" + r'{}\{}'.format(photo_path, train_name))
        #     tr.write('\n')
    for test_name in test_set:
        _, postfix = os.path.splitext(test_name)
        if postfix not in ['.jpg', '.png', '.jpeg', '.tif']:
            continue
        raw_test_path = os.path.join(photo_path, test_name)
        shutil.copy(raw_test_path, test_det)
        # with open("cls_test.txt", 'a') as ts:
        #     ten += 1
        #     ts.write(str(cls_id) + ";" + '{}'.format(raw_test_path))
        #     ts.write('\n')
    print(len(train_set)+len(test_set))

# tr.close()
# ts.close()
