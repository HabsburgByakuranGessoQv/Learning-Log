import torch

# 检测torch环境是否可用
print(torch.__version__)
print(torch.cuda.is_available())


# 第一题
print('*'*20, '第一题', '*'*20)
# 初始化 A 和 B
M = torch.Tensor([1, 2, 3])
N = torch.Tensor([[1], [2]])

# 方式一：使用 torch.sub() 函数进行减法操作
res1 = torch.sub(M, N)

# 方式二：使用 - 运算符进行减法操作
res2 = M - N

# 方式三：使用 torch.add() 函数进行加法操作，并传递负数作为参数
res3 = torch.add(M, torch.neg(N))

# 打印结果
print("res 1:", res1)
print("res 2:", res2)
print("res 3:", res3)


# 第二题
print('*'*20, '第二题', '*'*20)

# 创建大小分别为 3x2 和 4x2 的随机数矩阵
P = torch.randn(3, 2) * 0.01
Q = torch.randn(4, 2) * 0.01

print('P:\n', P)
print('Q:\n', Q)

# 对 P 进行形状变换得到 Q 的转置
QT = Q.t()

# 对 P 和 QT 求内积
res_2 = torch.mm(P, QT)
print('内积结果', res_2)


# 第三题
print('*'*20, '第三题', '*'*20)
x = torch.tensor(1.0, requires_grad=True)

# 计算 y1
y1 = x ** 2

with torch.no_grad():
    # 中断梯度追踪，计算 y2
    y2 = x ** 3

# 计算 y3
y3 = y1 + y2

# 计算 y3 对 x 的梯度
y3.backward()

# 输出 dy3/dx 的值
print(x.grad)
