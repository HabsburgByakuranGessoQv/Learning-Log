import os.path

import torch
print(torch.__version__)
print(torch.cuda.is_available())

elem = 'rerea.jpg'
save_path = r'E:\STUDYCONTENT\Pycharm\AlexNet\flowersPlus\\'
rew = 'we'

sp_path = os.path.join(save_path, rew) + r'\\sp_{}'.format(elem)
print(sp_path)
