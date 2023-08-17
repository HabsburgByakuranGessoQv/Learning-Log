import torch
import numpy as np
import matplotlib.pyplot as plt

# 构造训练数据
x_train = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
y_train = np.sin(x_train)

# 转换为张量
x_train = torch.from_numpy(x_train).unsqueeze(1).float()
y_train = torch.from_numpy(y_train).unsqueeze(1).float()

# 定义神经网络模型
W1 = torch.randn(1, 10, requires_grad=True)
b1 = torch.zeros(1, 10, requires_grad=True)
W2 = torch.randn(10, 1, requires_grad=True)
b2 = torch.zeros(1, 1, requires_grad=True)

# 定义优化器
lr = 0.01
for epoch in range(1000):
    # 前向传播
    h1 = torch.relu(torch.mm(x_train, W1) + b1)
    y_pred = torch.mm(h1, W2) + b2

    # 计算损失
    loss = torch.mean((y_pred - y_train) ** 2)

    # 反向传播
    loss.backward()

    # 更新参数
    with torch.no_grad():
        W1 -= lr * W1.grad
        b1 -= lr * b1.grad
        W2 -= lr * W2.grad
        b2 -= lr * b2.grad

        # 清空梯度
        W1.grad.zero_()
        b1.grad.zero_()
        W2.grad.zero_()
        b2.grad.zero_()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss {loss.item()}")

# 将模型转换为评估模式
W1.requires_grad_(False)
b1.requires_grad_(False)
W2.requires_grad_(False)
b2.requires_grad_(False)

# 生成测试数据
x_test = np.linspace(-2 * np.pi, 2 * np.pi, 100)
y_test = np.sin(x_test)

# 转换为张量
x_test = torch.from_numpy(x_test).unsqueeze(1).float()
y_test = torch.from_numpy(y_test).unsqueeze(1).float()

# 使用训练好的模型进行预测
h1 = torch.relu(torch.mm(x_test, W1) + b1)
y_pred_test = torch.mm(h1, W2) + b2

# 计算预测结果的损失
test_loss = torch.mean((y_pred_test - y_test) ** 2)

# 将结果转换为numpy数组并绘制图形
y_pred_test = y_pred_test.detach().numpy()
y_test = y_test.detach().numpy()
plt.plot(x_test.numpy(), y_pred_test, label="Predicted")
plt.plot(x_test.numpy(), y_test, label="Ground Truth")
plt.legend()
plt.show()

# 输出训练和测试集的准确率以及损失值
h1_train = torch.relu(torch.mm(x_train, W1) + b1)
y_pred_train = torch.mm(h1_train, W2) + b2
train_loss = torch.mean((y_pred_train - y_train) ** 2)
train_acc = torch.sum(torch.abs(torch.round(y_pred_train) - y_train) < 0.5).item() / len(y_train)
test_acc = torch.sum(torch.abs(torch.round(torch.from_numpy(y_pred_test)) - y_test) < 0.5).item() / len(y_test)

print(f"Train Loss: {train_loss.item()}, Train Accuracy: {train_acc}")
print(f"Test Loss: {test_loss.item()}, Test Accuracy: {test_acc}")
