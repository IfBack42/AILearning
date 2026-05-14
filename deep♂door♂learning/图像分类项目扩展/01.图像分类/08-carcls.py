# 1.导入工具包
import torch
import torch.nn as nn
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision import models

# 2.读取数据
# 2.1 指定数据集位置
car_train_path = './dataset/Stanford_Cars/train/'
car_test_path = './dataset/Stanford_Cars/test/'

# 2.2 设置增强方式
transform_RH = transforms.RandomHorizontalFlip(p=0.5)
transform_RR = transforms.RandomRotation(45)
transform_RS = transforms.Resize(size=(256, 256))
transform_color = transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.05)
train_transform = transforms.Compose([
    transforms.ToTensor(),
    transform_RS,
    transform_RR,
    transform_RH
])
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transform_RS
])

# 2.3 读取数据
car_train = ImageFolder(car_train_path, transform=train_transform)
car_test = ImageFolder(car_test_path, transform=test_transform)
# 2.4 获取batch数据
batch_size = 2
train_loader = DataLoader(dataset=car_train, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=car_test, batch_size=batch_size, shuffle=False)

# 2.5 遍历每个迭代的数据，将其结果展示出来
# import matplotlib.pyplot as plt
# for b, (imgs, targets) in enumerate(train_loader):
#     # 获取第一个batch的图像
#     if b == 1:
#         # 将其进行展示
#         fig, axes = plt.subplots(1, 2)
#         # 遍历batch中的每个图像
#         for i in range(batch_size):
#             # 图像显示出来
#             axes[i].imshow(imgs[i].permute(1, 2, 0))
#             # 设置图像标题
#             axes[i].set_title(targets[i].item())
#         plt.show()
#     elif b > 0:
#         break
# print(car_train.class_to_idx)

# 模型构建

# 3.模型实例化和参数设置
# 3.1 模型实例化
model = models.resnet50(pretrained=True)
# print(model.parameters)
# 3.2 参数设置
# 3.2.1 冻结参数
for param in model.parameters():
    param.requires_grad = False
# 3.2.2 获取模型中fc层的输入特征数
in_feature = model.fc.in_features
# 3.2.3 构建新的fc层
model.fc = nn.Linear(in_feature, 196)

# print(model.parameters)

# 4.模型训练
# 4.1 训练参数设置
# 4.1.1 学习率
learning_rate = 1e-3
# 4.1.2 训练轮数
num_epochs = 10
# 4.1.3 优化算法Adam = RMSProp + Momentum (梯度、lr两方面优化下降更快更稳)
optimizer = torch.optim.Adam(model.fc.parameters(), lr=learning_rate)
# 4.1.4 交叉熵损失函数
loss_fn = torch.nn.CrossEntropyLoss()


# 4.2 定义评估方法
def evaluate_accuracy(data_iter, model):
    total = 0
    correct = 0
    # 4.2.1 不进行梯度计算
    with torch.no_grad():
        # 4.2.2 模型是验证模式
        model.eval()
        # 4.2.3 获取每一个batch的数据，进行预测
        for images, labels in data_iter:
            outputs = model(images)
            # 4.2.4 获取预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 4.2.5 预测的次数
            total += labels.size(0)
            # 4.2.6 预测正确的个数
            correct += (predicts == labels).cpu().sum()
            break
    # 4.2.7 获取准确率
    return correct / total


# 4.3 定义模型训练过程:指定数据集，优化器，损失函数和轮次
def train(data_loader=train_loader,
          optimizer=optimizer,
          loss_fn=loss_fn,
          epochs=num_epochs):
    # 4.3.1 遍历每一个轮次进行训练
    for epoch in range(epochs):
        print('current epoch = {}'.format(epoch))
        # 4.3.2 每一个轮次的损失，迭代次数，预测个数和预测正确个数的初始化
        train_accuracy_total = 0
        train_correct = 0
        #  损失值的和
        train_loss_sum = 0
        #  迭代次数
        iter = 0
        for i, (images, labels) in enumerate(data_loader):
            # 4.3.3 模型定义为训练模式
            model.train()
            # 4.3.4 对数据进行预测
            outputs = model(images)
            # 4.3.5 计算模型的损失
            loss = loss_fn(outputs, labels)
            # 4.3.6 在做反向传播前先清除网络状态
            optimizer.zero_grad()
            # 4.3.7 损失值进行反向传播
            loss.backward()
            # 4.3.8 参数迭代更新
            optimizer.step()
            # 4.3.9 求损失的和
            train_loss_sum += loss.item()
            # 4.3.10 输出模型预测结果
            _, predicts = torch.max(outputs.data, dim=1)
            # 4.3.11 获取训练集预测正确的个数
            train_accuracy_total += labels.size(0)
            train_correct += (predicts == labels).cpu().sum().item()
            iter += 1
            break
        # 4.3.12 测试集预测的准确率
        test_acc = evaluate_accuracy(test_loader, model)
        torch.save(model.state_dict(), "./weights/model-{}.pth".format(epoch))
        print(
            'epoch:{0},   loss:{1:.4f},   train accuracy:{2:.3f},  test accuracy:{3:.3f}'
            .format(epoch+1, train_loss_sum / (iter + 0.01),
                    train_correct / train_accuracy_total, test_acc))
    print('------------finish training-------------')


# train()


# 5.模型预测
import glob
import os
from PIL import Image
import matplotlib.pyplot as plt

# 5.1 加载模型
model.load_state_dict(torch.load('./weights/model-149.pth', map_location=torch.device('cpu')))
# 5.2 待预测数据
file_path = './car_image/'
# 5.3 禁用梯度计算
with torch.no_grad():
    # 5.4 设置为验证模式
    model.eval()
    # 5.5 遍历每一个图片
    image_paths = glob.glob(os.path.join(file_path, '*.jpg'))   # 批量获取图像数据
    for image_path in image_paths:
        # 5.6 读取图片
        img = Image.open(image_path)
        batch = test_transform(img).unsqueeze(0)    # （B,C,H,W）
        # 5.7 网络预测
        outputs = model(batch).squeeze(0).softmax(0)   # {0:0.78}
        class_id = outputs.argmax().item()
        score = outputs[class_id].item()   # 置信度
        print(score)
        labels_name = car_train.classes[class_id]    # {0：audi,1:Benz}
        # 5.8 显示图片
        plt.imshow(img)
        plt.title(labels_name)
        plt.show()
