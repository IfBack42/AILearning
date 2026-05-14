# 1.相关依赖包导入
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.io import read_image
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
# 加载数据集
from voc_data_util import VocDataset, VOC_BBOX_LABEL_NAMES
from torch.utils.data import DataLoader

# 2.数据集加载
dataset = VocDataset(root='datasets/VOCdevkit/VOC2007', transforms=VocDataset.get_transform())

# # 数据集绘制
# # 获取图像及对应的标注信息
# img, targets = dataset[141]
# img = img.permute(1, 2, 0).numpy().astype(np.uint8)
# fig = plt.imshow(img)
# # 将标注信息绘制在图像上
# for index, boxes in enumerate(targets['boxes'].numpy()):
#     fig.axes.add_patch(
#         plt.Rectangle(xy=(boxes[0], boxes[1]),
#                       width=boxes[2] - boxes[0],
#                       height=boxes[3] - boxes[1],
#                       fill=False,
#                       edgecolor="green",
#                       linewidth=1))
# plt.show()

# 3.模型加载及实例化
# N+1包含背景

# 3.模型实例化及参数设置
num_classes = 21
# 3.1 模型实例化：不使用预训练模型，修正类别个数，backbone使用预训练结果
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
    pretrained=False,
    num_classes=num_classes,
    pretrained_backbone=True)

def collate_fn(batch):
    return tuple(zip(*batch))


# 3.2 参数设置
# 3.2.1 获取batch的数据，送入网络中进行训练
train_data_loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True,
    collate_fn=collate_fn
)

# 遍历数据，获取第一个batch的数据进行展示
# for i, data in enumerate(train_data_loader):
#     inputs, labels = data
#     # batch的大小
#     print('图片个数：', len(inputs))
#     print('目标值：', labels)
#     break


# 获取所有要进行训练的参数，设置优化器
# 3.2.2 参数冻结
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
# 3.2.3 迭代次数
itr = 1
# 3.2.4 存放训练损失
total_train_loss = []
# 3.2.5 损失值
losses_value = 0

# 4.模型训练
# 4.1 遍历每个轮次进行训练
for epoch in range(2):
    # 4.2 训练模式
    model.train()
    train_loss = []
    # 4.3 遍历数据，获取图像，目标值和图像id
    for images, targets in train_data_loader:
        # 4.4 将数据送入网络中进行训练，获取损失值(RPN的损失+FastRCNN的损失),将信息打印出来分析
        loss_dict = model(images, targets)
        print(loss_dict)
        # 4.5 将损失求和
        losses = sum(loss for loss in loss_dict.values())
        # 4.6 获取loss值
        losses_value = losses.item()
        train_loss.append(losses_value)
        # 4.7 进行反向传播，更新参数
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        # 4.8 日志信息
        print(f"Epoch: {epoch + 1}, Batch: {itr}, Loss: {losses_value}")
        # 4.9 迭代次数增1
        itr += 1
    # 4.10 获取当前轮次的损失
    epoch_train_loss = np.mean(train_loss)
    # 4.11 轮次损失写入到列表中
    total_train_loss.append(epoch_train_loss)

# 5.绘制损失函数变化的曲线
plt.plot(range(len(total_train_loss)), [loss.numpy() for loss in total_train_loss])
plt.grid()
