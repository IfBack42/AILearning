# 1.导入工具包
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torchvision import models
from torch.utils.data import DataLoader

# 2.数据获取
# 2.1 指定批次大小
batch_size = 2
# 2.2 指定数据集路径
flower_train_path = './dataset/flower_datas/train/'
flower_test_path = './dataset/flower_datas/val/'
# 2.3 先将数据转换为tensor类型，并调整数据的大小为224x224
dataset_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224))
])
# 2.4 获取训练集数据和测试集数据
flower_train = ImageFolder(flower_train_path, transform=dataset_transform)
flower_test = ImageFolder(flower_test_path, transform=dataset_transform)
# 2.5 获取数据的迭代
train_loader = DataLoader(dataset=flower_train, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=flower_test, batch_size=batch_size, shuffle=False)


# 3.构建模型：预训练模型
class Vgg16_finetune(nn.Module):
    def __init__(self, num_class=5):
        super(Vgg16_finetune, self).__init__()
        vgg16_pre = models.vgg16(pretrained=True)
        self.features = vgg16_pre.features
        self.avgpool = vgg16_pre.avgpool
        self.classfier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 512),
            nn.ReLU(True),
            nn.Dropout(0.2),
            nn.Linear(512, 128),
            nn.ReLU(True),
            nn.Dropout(0.2),
            nn.Linear(128, num_class),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x=torch.flatten(x,1)
        output =self.classfier(x)
        return output


# 4.模型实例化和参数设置
# 4.1 模型实例化
model = Vgg16_finetune(num_class=5)
# 4.2 参数设置
# 4.2.1 冻结参数
for param in model.features.parameters():
    param.requires_grad = False
# 4.2.2 学习率/优化器/损失函数/轮次
lr = 0.001
optimizer = torch.optim.Adam(model.classfier.parameters(),lr = lr)
loss_fn = torch.nn.CrossEntropyLoss()
num_epochs = 10

# 5.模型训练
# 5.1 定义评估函数
def evaluate_accuracy(data_iter, model):
    total = 0
    correct = 0
    # 5.1.1 不进行梯度计算
    with torch.no_grad():
        # 5.1.2 模型是验证模式
        model.eval()
        # 5.1.3 获取每一个batch的数据，进行预测
        for images, labels in data_iter:
            outputs = model(images)
            # 5.1.4 获取预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 5.1.5 预测的次数
            total += labels.size(0)
            # 5.1.6 预测正确的个数
            correct += (predicts == labels).cpu().sum()
    # 5.1.7 获取准确率
    return correct / total

# 5.2 定义模型训练过程:指定数据集，优化器，损失函数和轮次
def train(data_loader=train_loader,
          optimizer=optimizer,
          loss_fn=loss_fn,
          epochs=num_epochs):
    # 5.2.1 遍历每一个轮次进行训练
    for epoch in range(epochs):
        print('current epoch = {}'.format(epoch))
        # 5.2.2 每一个轮次的损失，预测个数和预测正确个数的初始化
        train_accuracy_total = 0
        train_correct = 0
        # 损失值的和
        train_loss_sum = 0
        # 迭代次数
        iter = 0
        # 5.2.3 遍历每一个批次的数据进行训练
        for i, (images, labels) in enumerate(data_loader):
            # 5.2.4 模型定义为训练模式
            model.train()
            # 5.2.5 对数据进行预测
            outputs = model(images)
            # 5.2.6 计算模型的损失
            loss = loss_fn(outputs, labels)
            # 5.2.7 在做反向传播前先清除网络状态
            optimizer.zero_grad()
            # 5.2.8 损失值进行反向传播
            loss.backward()
            # 5.2.9 参数迭代更新
            optimizer.step()
            # 5.2.10 求损失的和
            train_loss_sum += loss.item()
            # 5.2.11 输出模型预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 5.2.12 获取训练集预测正确的个数
            train_accuracy_total += labels.size(0)
            train_correct += (predicts == labels).cpu().sum().item()
            iter+=1
        # 5.2.13 测试集预测的准确率
        test_acc = evaluate_accuracy(test_loader, model)
        print(
            'epoch:{0},   loss:{1:.4f},   train accuracy:{2:.3f},  test accuracy:{3:.3f}'
            .format(epoch, train_loss_sum / (iter+0.01),
                    train_correct / train_accuracy_total, test_acc))
    print('------------finish training-------------')

train()