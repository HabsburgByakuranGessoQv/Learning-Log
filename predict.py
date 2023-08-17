import os
import json

import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

from model import AlexNet


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize((224, 224)),
         transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    # load image
    # img_path = "./1.png"
    img_path = r"E:\STUDYCONTENT\Pycharm\AlexNet\2.png"
    assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    img = Image.open(img_path)

    plt.imshow(img)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = AlexNet(num_classes=5).to(device)

    # load model weights
    weights_path = r"E:\STUDYCONTENT\Pycharm\AlexNet\400\BESTnet.pth"
    assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path))

    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
                                                 predict[predict_cla].numpy())
    plt.title(print_res)
    for i in range(len(predict)):
        print("class: {:10}   prob: {:.3}".format(class_indict[str(i)],
                                                  predict[i].numpy()))
    plt.show()

    # 预测汇总
    pic_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\datasets\test'
    classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
    print('*' * 50)
    num_all, acc_all = 0, 0
    for c_path in classes:
        temp_acc, temp_num = 0, 0
        val_path_elem = os.path.join(pic_path, c_path)
        pic_list = os.listdir(val_path_elem)
        # print(every_pic)
        for every_pic in pic_list:
            temp_num += 1
            num_all += 1
            pic_elem = os.path.join(val_path_elem, every_pic)
            img = Image.open(pic_elem)

            plt.imshow(img)
            # [N, C, H, W]
            img = data_transform(img)
            # expand batch dimension
            img = torch.unsqueeze(img, dim=0)
            with torch.no_grad():
                # predict class
                output = torch.squeeze(model(img.to(device))).cpu()
                predict = torch.softmax(output, dim=0)
                predict_cla = torch.argmax(predict).numpy()
            if class_indict[str(predict_cla)] == c_path:
                temp_acc += 1
                acc_all += 1
        print('class: {:10} Accurate: {:.3}'.format(c_path, temp_acc/temp_num))
    print('Aver Accurate: {:.3}'.format(acc_all/num_all))
    print('*' * 50)


if __name__ == '__main__':
    main()
