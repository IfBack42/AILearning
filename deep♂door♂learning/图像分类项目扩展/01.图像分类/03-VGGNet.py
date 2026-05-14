# 1.导入工具包
import torch
import torchvision.models as models
from torchsummary import summary
import matplotlib.pyplot as plt
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# 2. 实例化模型
model = models.vgg16()
# 观察模型结构
# print(summary(model=model, input_size=(3, 224, 224), batch_size=1))
# print(model.parameters)

# -----------------------------------鲜花识别案例-------------------------------------- #

# 1.数据获取
# 1.1 指定批次大小
batch_size = 2
# 1.2 指定数据集路径
flower_train_path = './dataset/flower_datas/train/'
flower_test_path = './dataset/flower_datas/val/'

# 1.3 先将数据转换为tensor类型，并调整数据的大小为224x225
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

# 1.6 遍历每个迭代的数据，将其结果展示出来
for b, (imgs, targets) in enumerate(train_loader):
    # 获取第一个batch的图像
    if b == 1:
        # 将其进行展示
        fig, axes = plt.subplots(1, 2)
        # 遍历batch中的每个图像
        for i in range(batch_size):
            # 图像显示出来
            axes[i].imshow(imgs[i].permute(1, 2, 0))
            # 设置图像标题
            axes[i].set_title(targets[i].item())
        # plt.show()
    elif b > 0:
        break

# 2.模型实例化和参数设置
# 2.1 模型实例化
model = models.vgg16(num_classes=5)
# print(model.parameters)
# 2.2 模型训练的参数设置
# 1 学习率
learning_rate = 1e-3
# 2 训练轮数
num_epochs = 3
# 3 优化算法Adam = RMSProp + Momentum
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# 4 交叉熵损失函数
loss_fn = torch.nn.CrossEntropyLoss()


# 3.模型评估方法
# 计算模型预测精度:测试集数据，模型
def evaluate_accuracy(data_iter, model):
    total = 0
    correct = 0
    # 3.1 不进行梯度计算
    with torch.no_grad():
        # 3.2 模型是验证模式
        model.eval()
        # 3.3 获取每一个batch的数据，进行预测
        for images, labels in data_iter:
            outputs = model(images)
            # 3.4 获取预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 3.5 预测的次数
            total += labels.size(0)
            # 3.6 预测正确的个数
            correct += (predicts == labels).cpu().sum()
            break
    # 3.2 获取准确率
    return correct / total


# 4.定义模型训练过程:指定数据集，优化器，损失函数和轮次
# 4.1 定义训练方法train
def train(data_loader=train_loader,
          optimizer=optimizer,
          loss_fn=loss_fn,
          epochs=num_epochs):
    # 4.1.1 遍历每一个轮次进行训练
    for epoch in range(epochs):
        print('current epoch = {}'.format(epoch))
        # 4.1.2 每一个轮次的损失，预测个数和预测正确个数的初始化
        train_accuracy_total = 0
        train_correct = 0
        # 4.1.3 损失值的和
        train_loss_sum = 0
        # 4.1.4 迭代次数
        iter = 0
        for i, (images, labels) in enumerate(data_loader):
            # 4.1.5 模型定义为训练模式
            model.train()
            # 4.1.6 对数据进行预测
            outputs = model(images)
            # 4.1.7 计算模型的损失
            loss = loss_fn(outputs, labels)
            # 4.1.8 在做反向传播前先清除网络状态
            optimizer.zero_grad()
            # 4.1.9 损失值进行反向传播
            loss.backward()
            # 4.1.10 参数迭代更新
            optimizer.step()
            # 4.1.11 求损失的和
            train_loss_sum += loss.item()
            # 4.1.12 输出模型预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 4.1.13 获取训练集预测正确的个数
            train_accuracy_total += labels.size(0)
            train_correct += (predicts == labels).cpu().sum().item()
            iter += 1
            break
        # 4.1.14 测试集预测的准确率
        test_acc = evaluate_accuracy(test_loader, model)
        print(
            'epoch:{0},   loss:{1:.4f},   train accuracy:{2:.3f},  test accuracy:{3:.3f}'
            .format(epoch, train_loss_sum / (iter + 0.01),
                    train_correct / train_accuracy_total, test_acc))
    print('------------finish training-------------')


# train()
