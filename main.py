import torch
import torchviz

# 创建张量 x 和 y，并进行加法运算
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)
z = x + y

# 对张量 z 进行平方运算
s = z ** 2

# 计算梯度
s.backward()

# 可视化计算图
torchviz.make_dot(s, params={"x": x, "y": y})