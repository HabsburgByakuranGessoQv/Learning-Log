from cv2 import cv2
import os
import shutil

classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
pic_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\flowers\\'
save_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\flowersPlus\\'

for flower in classes:
    flower_path = os.path.join(pic_path, flower)
    flower_save = os.path.join(save_path, flower)
    flower_list = os.listdir(flower_path)
    if os.path.exists(flower_save) is not True:
        os.mkdir(flower_save)

    for elem in flower_list:
        elem_flower = os.path.join(flower_path, elem)
        elem_save = os.path.join(flower_save, elem)
        # Copy
        shutil.copy(elem_flower, elem_save)
        # DataPlus
        pic_raw = cv2.imread(elem_flower)
        pic_sp = cv2.flip(pic_raw, 1)
        pic_cz = cv2.flip(pic_raw, 0)
        pic_sp_cz = cv2.flip(pic_raw, -1)
        # Write
        sp_path = flower_save + r'\\sp_{}'.format(elem)
        cz_path = flower_save + r'\\cz_{}'.format(elem)
        sp_cz_path = flower_save + r'\\sp_cz_{}'.format(elem)
        cv2.imwrite(sp_path, pic_sp)
        cv2.imwrite(cz_path, pic_cz)
        cv2.imwrite(sp_cz_path, pic_sp_cz)
    print('class: {:10} Amplified'.format(flower))
