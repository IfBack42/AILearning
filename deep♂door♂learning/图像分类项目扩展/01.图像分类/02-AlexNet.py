# AlexNet模型构建
# 1.导入工具包
import torch.nn
from torch import nn
from torchsummary import summary
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


# 2.定义网络类
class AlexNet(nn.Module):
    # init:构建层架构
    def __init__(self, in_dim, n_class):
        super().__init__()
        # 卷积层
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=in_dim, out_channels=96, kernel_size=11, stride=4, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2),
            nn.Conv2d(96, 256, 5, 1, 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2),
            nn.Conv2d(256, 384, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, 3, 1, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2)
        )
        # 全连接层
        self.fc = nn.Sequential(
            nn.Linear(9216, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, n_class)
        )

    # forward：完成前向传播
    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        out = self.fc(x)
        return out

#
# net = AlexNet(3, 1000)
# print(summary(net, input_size=(3, 227, 227), batch_size=1))

# --------------------------------鲜花分类案例------------------------------------------ #

# 1.数据获取
# 1.1 指定数据集路径
flower_train_path = './dataset/flower_datas/train/'
flower_test_path = './dataset/flower_datas/val/'
# 1.2 定义数据处理方法（resize）
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((227, 227))
])
# 1.3 ImageFolder读取数据
flower_train_data = ImageFolder(flower_train_path, transform=transform)
flower_test_data = ImageFolder(flower_test_path, transform=transform)
# 1.4 DataLoader获取batch数据

batch_size = 2   # config.py && 参数解析器

flower_train_loader = DataLoader(dataset=flower_train_data, batch_size=batch_size, shuffle=True)
flower_test_loader = DataLoader(dataset=flower_test_data, batch_size=batch_size, shuffle=False)
# 1.5 数据的展示
for b, (images, targtes) in enumerate(flower_train_loader):
    if b == 10:
        fig, axes = plt.subplots(1, 2)
        for i in range(batch_size):
            axes[i].imshow(images[i].permute(1, 2, 0))
            axes[i].set_title(targtes[i].item())
        # plt.show()
    elif b > 10:
        break

# 2.模型实例化和参数设置
# 2.1 模型实例化
model = AlexNet(3, 5)
# 2.2 参数设置
# 2.2.1 lr
lr = 0.001
# 2.2.2 轮次
num_epoch = 3
# 2.2.3 损失
loss = torch.nn.CrossEntropyLoss()
# 2.2.4 优化器
opti = torch.optim.Adam(model.parameters(), lr=lr)


# 3.评估方法：准确率
def eval_acc(test_data, model):
    # 3.1 设置参数
    corr = 0
    total = 0
    # 3.2 遍历数据，进行模型预测
    with torch.no_grad():
        model.eval()
        for imags, label in test_data:
            out_put = model(imags)
            _, pred = torch.max(out_put.data, dim=1)
            total += label.size(0)
            corr += (pred == label).cpu().sum()
    return corr / total


# 4.模型训练
# 4.1 定义训练方法train
def train(data_loader=flower_train_loader, model=model, optim=opti, loss_fn=loss):
    # 4.1.1 遍历每个轮次
    for epoch in range(num_epoch):
        print(f'current epoch:{epoch}')
        # 4.1.2 定义一些参数
        train_data_num = 0
        train_data_corr = 0
        loss_sum = 0
        iter = 0
        # 4.1.3 遍历每个batch
        for i, (image, targtes) in enumerate(data_loader):
            # 4.1.4 将模型设置为训练模式
            model.train()
            # 4.1.5 通过模型预测输出
            output = model(image)
            # 4.1.6 计算损失
            loss = loss_fn(output, targtes)
            # 4.1.7 清除之前的梯度
            optim.zero_grad()
            # 4.1.8 反向传播计算梯度
            loss.backward()
            # 4.1.9 更新模型参数
            optim.step()
            # 4.1.10 计算准确率，loss的变化
            train_data_num += targtes.size(0)
            _, pred = torch.max(output.data, dim=1)
            train_data_corr += (pred == targtes).cpu().sum()
            loss_sum += loss.item()
            iter += 1
        corr = train_data_corr / train_data_num
        # 4.1.11 评估模型效果
        test_corr = eval_acc(flower_test_loader, model)
        print(
            f'epoch:{epoch+1},   loss:{loss_sum / (iter + 0.01):.4f},   train accuracy:{corr:.3f},  test accuracy:{test_corr:.3f}')


if __name__ == '__main__':
    train()
