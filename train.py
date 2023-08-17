import json
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data  # 如果不用这个就会出现pycharm不识别data的问题
from torchvision import transforms, datasets
from tqdm import tqdm

from model import AlexNet


def main():
    loss_list, val_acc, context, val_loss_list = [], [], [], []
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device.".format(device))

    data_transform = {
        "train": transforms.Compose([transforms.RandomResizedCrop(224),
                                     transforms.RandomHorizontalFlip(),
                                     transforms.ToTensor(),
                                     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]),
        "val": transforms.Compose([transforms.Resize((224, 224)),  # cannot 224, must (224, 224)
                                   transforms.ToTensor(),
                                   transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])}

    data_root = os.path.abspath(os.path.join(os.getcwd(), "./"))  # get data root path
    image_path = os.path.join(data_root, "datasets")  # flower data set path
    assert os.path.exists(image_path), "{} path does not exist.".format(image_path)
    train_dataset = datasets.ImageFolder(root=os.path.join(image_path, "train"),
                                         transform=data_transform["train"])
    train_num = len(train_dataset)

    # {'daisy':0, 'dandelion':1, 'roses':2, 'sunflower':3, 'tulips':4}
    flower_list = train_dataset.class_to_idx
    cla_dict = dict((val, key) for key, val in flower_list.items())
    # write dict into json file
    json_str = json.dumps(cla_dict, indent=4)
    with open('class_indices.json', 'w') as json_file:
        json_file.write(json_str)

    batch_size = 4
    nw = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])  # number of workers
    print('Using {} dataloader workers every process'.format(nw))

    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=batch_size, shuffle=True,
                                               num_workers=nw)

    validate_dataset = datasets.ImageFolder(root=os.path.join(image_path, "val"),
                                            transform=data_transform["val"])
    val_num = len(validate_dataset)
    validate_loader = torch.utils.data.DataLoader(validate_dataset,
                                                  batch_size=4, shuffle=False,
                                                  num_workers=nw)

    print("using {} images for training, {} images for validation.".format(train_num,
                                                                           val_num))
    # test_data_iter = iter(validate_loader)
    # test_image, test_label = test_data_iter.next()
    #
    # def imshow(img):
    #     img = img / 2 + 0.5  # unnormalize
    #     npimg = img.numpy()
    #     plt.imshow(np.transpose(npimg, (1, 2, 0)))
    #     plt.show()
    #
    # print(' '.join('%5s' % cla_dict[test_label[j].item()] for j in range(4)))
    # imshow(utils.make_grid(test_image))

    net = AlexNet(num_classes=5, init_weights=True)

    net.to(device)
    loss_function = nn.CrossEntropyLoss()
    # pata = list(net.parameters())
    optimizer = optim.Adam(net.parameters(), lr=1.0E-4, weight_decay=0.0003)
    # optimizer = optim.SGD(net.parameters(), lr=0.0001, weight_decay=0.0003)

    epochs = 400
    save_path = r'.\net'
    best_acc = 0.0
    train_steps = len(train_loader)
    for epoch in range(epochs):
        # train
        net.train()
        running_loss = 0.0
        train_bar = tqdm(train_loader, file=sys.stdout)
        for step, data in enumerate(train_bar):
            images, labels = data
            optimizer.zero_grad()
            outputs = net(images.to(device))
            loss = loss_function(outputs, labels.to(device))
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()

            train_bar.desc = "train epoch[{}/{}] loss:{:.3f}".format(epoch + 1,
                                                                     epochs,
                                                                     loss)

        # validate
        net.eval()
        acc = 0.0  # accumulate accurate number / epoch
        val_loss_t = 0.0
        with torch.no_grad():
            val_bar = tqdm(validate_loader, file=sys.stdout)
            for val_data in val_bar:
                val_images, val_labels = val_data
                outputs = net(val_images.to(device))
                predict_y = torch.max(outputs, dim=1)[1]
                acc += torch.eq(predict_y, val_labels.to(device)).sum().item()
                val_loss_e = loss_function(outputs, val_labels.to(device))
                val_loss_t += val_loss_e.item()

        val_accurate = acc / val_num
        val_loss = val_loss_t / val_num

        print('[epoch %d] train_loss: %.3f  val_accuracy: %.3f' %
              (epoch + 1, running_loss / train_steps, val_accurate))
        val_acc.append(val_accurate)
        val_loss_list.append(val_loss)
        loss_list.append(running_loss/train_steps)
        elem_context = [epoch+1, running_loss/train_steps, val_loss, val_accurate]
        context.append(elem_context)

        # 保存每轮的模型
        # model_path = os.path.join(save_path, 'e{}net.pth'.format(epoch))
        # torch.save(net.state_dict(), model_path)
        if val_accurate > best_acc:
            best_acc = val_accurate
            torch.save(net.state_dict(), os.path.join(save_path, 'BESTnet.pth'))

    print('Finished Training')

    # Write
    names = ['Epoch', 'Train_loss', 'Val_loss', 'Accurate']
    context_csv = pd.DataFrame(columns=names, data=context)
    context_csv.to_csv('res.csv')

    # Draw
    epochs_list = range(len(loss_list))
    plt.plot(epochs_list, loss_list, 'r', label='Loss')
    plt.plot(epochs_list, val_acc, 'b', label='Accurate')
    plt.title('Training Loss and Validation Accurate')
    plt.legend()
    plt.savefig(r'loss_acc.png')
    plt.show()

    epochs_list = range(len(loss_list))
    plt.plot(epochs_list, loss_list, 'r', label='Train_loss')
    plt.plot(epochs_list, val_loss_list, 'b', label='Val_loss')
    plt.title('Training Loss and Validation Loss')
    plt.legend()
    plt.savefig(r'loss_loss.png')
    plt.show()

    plt.plot(epochs_list, loss_list, 'r', label='Loss')
    plt.title('Training Loss')
    plt.legend()
    plt.savefig(r'loss.png')
    plt.show()

    plt.plot(epochs_list, val_acc, 'b', label='Accurate')
    plt.title('Validation Accurate')
    plt.legend()
    plt.savefig(r'acc.png')
    plt.show()


if __name__ == '__main__':
    main()
