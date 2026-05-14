# 1.导入工具包
import torch
import torchvision.models as models
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt

# 2.模型实例化
model = models.googlenet()
# 3.模型展示
# print(model.parameters)
# print(model.inception5a)
# print(model.aux1)


# -------------------------------鲜花案例的实现--------------------------------------------- #

# 1.获取数据
# 1.1 指定批次大小
batch_size = 2
# 1.2 指定数据集路径
flower_train_path = './dataset/flower_datas/train/'
flower_test_path = './dataset/flower_datas/val/'
# 1.3 先将数据转换为tensor类型，并调整数据的大小为224x224
dataset_transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Resize((224, 224))])
# 1.4 获取训练集数据和测试集数据
flower_train = ImageFolder(flower_train_path, transform=dataset_transform)
flower_test = ImageFolder(flower_test_path, transform=dataset_transform)
# 1.5 获取数据的迭代
train_loader = DataLoader(dataset=flower_train,
                          batch_size=batch_size,
                          shuffle=True)
test_loader = DataLoader(dataset=flower_test,
                         batch_size=batch_size,
                         shuffle=False)

# 1.6 图像展示,遍历每个迭代的数据，将其结果展示出来
for b, (imgs, targets) in enumerate(train_loader):
    # 获取第一个batch的图像
    if b == 20:
        # 将其进行展示
        fig, axes = plt.subplots(1, 2)
        # 遍历batch中的每个图像
        for i in range(batch_size):
            # 图像显示出来
            axes[i].imshow(imgs[i].permute(1, 2, 0))
            # 设置图像标题
            axes[i].set_title(targets[i].item())
        # plt.show()
    elif b > 20:
        break

# 2.模型实例化及参数设置
# 2.1 模型实例化
model = models.googlenet(num_classes=5)
# print(model.parameters)
# 2.2 参数的设置
# 2.2.1 学习率
learning_rate = 1e-3
# 2.2.2 训练轮数
num_epochs = 3
# 2.2.3 优化算法Adam = RMSProp + Momentum
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# 2.2.4 交叉熵损失函数
loss_fn = torch.nn.CrossEntropyLoss()


# 3.定义模型评估方法，计算模型预测精度:测试集数据，模型
def evaluate_accuracy(data_iter, model):
    total = 0
    correct = 0
    # 3.1 不进行梯度计算
    with torch.no_grad():
        # 3.2 模型是验证模式
        model.eval()
        # 3.3 获取每一个batch的数据，进行预测
        for images, labels in data_iter:
            # 3.4 google进行模型预测时只返回最终的结果
            outputs = model(images)
            # 3.5 获取预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 3.6 预测的次数
            total += labels.size(0)
            # 3.7 预测正确的个数
            correct += (predicts == labels).cpu().sum()
    # 3.8 获取准确率
    return correct / total


# 4.模型训练
def train(data_loader=train_loader, optim=optimizer, loss_fn=loss_fn, epochs=num_epochs):
    # 4.1 遍历每个轮次
    for i in range(epochs):
        # 4.2 准确率和loss初试参数设置
        total_image = 0
        correct_image = 0
        loss_sum = 0
        iter = 0
        # 4.3 遍历每个bacth
        for b, (images, labels) in enumerate(data_loader):
            model.train()
            # 4.4 模型预测
            output, aux2, aux1 = model(images)
            # 4.5 损失计算
            loss_0 = loss_fn(output, labels)
            loss_2 = loss_fn(aux2, labels)
            loss_1 = loss_fn(aux1, labels)
            loss = loss_0 + 0.3 * loss_2 + 0.2 * loss_1
            loss_sum += loss.item()
            # 4.6 梯度清零
            optimizer.zero_grad()
            # 4.7 反向传播
            loss.backward()
            # 4.8 参数更新
            optimizer.step()
            # 4.9 统计数据
            total_image += labels.size(0)
            _, pred = torch.max(output.data, dim=1)
            correct_image += (pred == labels).cpu().sum().item()
            iter += 1
        # 4.10 测试集准确率
        test_acc = evaluate_accuracy(test_loader, model)
        print('epoch:{0},   loss:{1:.4f},   train accuracy:{2:.3f},  test accuracy:{3:.3f}'
              .format(i, loss_sum / (iter + 0.01),
                      correct_image / total_image, test_acc))


# train()
