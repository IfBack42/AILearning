# 导入相应的工具包
import torchvision
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch.utils.data import DataLoader
# 数据获取的
import pandas as pd
from datasets import Wheat
from dataset_utils import show_images, show_bboxes
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import numpy as np
import seaborn as sns

# 1.模型构建
# 1.1 创建模型：torchvision
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False, pretrained_backbone=True,
                                                             trainable_backbone_layers=False)
print(model.roi_heads.box_predictor)
# 1.2 修改模型的输出端(迁移学习)
num_classes = 2
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes=num_classes)
print(model.roi_heads.box_predictor)
# 2.训练参数的设置
# 2.1 设备
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)
model.to(device)
# 2.2 优化器
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.0001, momentum=0.9, weight_decay=0.0005)
print(optimizer)
# 2.3 参数
epochs = 2
batch_size = 2
# 3.获取数据
# 3.1 指定数据集路径
train_data_dir = 'wheatData/train'
train_data_label = pd.read_csv('wheatData/train_data.csv')
# 3.2 实例化数据读取类
train_dataset = Wheat(train_data_label, train_data_dir, transforms=Wheat.get_transform())


# 3.3 调用dataloader
def collate_fn(batch):
    return tuple(zip(*batch))


train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
# # 将数据进行展示
# for i, (imgs, targets, img_id) in enumerate(train_dataloader):
#     imgs = [imgs[j].permute(1, 2, 0) for j in range(batch_size)]
#     # 图像展示
#     axes = show_images(imgs, 1, 2)
#     # 标注框展示
#     for ax, target in zip(axes, targets):
#         show_bboxes(ax, target['boxes'], labels=None, colors=['w'])
#     plt.show()
#     break

# 4.模型训练
# 4.1 参数设置
# 4.1.1 迭代次数
itr = 1
# 4.1.2 存放训练损失
total_train_loss = []
# 4.1.3 损失值
losses_value = 0
# 4.2 遍历每个轮次进行训练
for epoch in range(epochs):
    # 计时
    start_time = time.time()
    # 4.2.1 训练模式
    model.train()
    train_loss = []
    # 进度条
    pbar = tqdm(train_dataloader, desc='let\'s train')
    # 4.2.2 遍历数据，获取图像，目标值和图像id
    for images, targets, image_ids in pbar:
        # 4.2.3 将图像写入设备中
        images = list(image.to(device) for image in images)
        # print(targets)
        # 4.2.4 将目标值写入设备中：key：value
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        # 4.2.5 将数据送入网络中进行训练，获取损失值
        loss_dict = model(images, targets)
        # print(loss_dict)
        # 4.2.6 将损失求和
        losses = sum(loss for loss in loss_dict.values())
        # 4.2.7 获取loss值
        losses_value = losses.item()
        train_loss.append(losses_value)
        # 4.2.8 进行反向传播，更新参数
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        # 4.2.9 日志信息
        pbar.set_description(f"Epoch: {epoch + 1}, Batch: {itr}, Loss: {losses_value}")
        # 4.2.10 迭代次数增1
        itr += 1
        break
    # 4.2.11 获取当前轮次的损失
    epoch_train_loss = np.mean(train_loss)
    # 4.2.12 轮次损失写入到列表中
    total_train_loss.append(epoch_train_loss)

# 5.模型保存
torch.save(model.state_dict(), 'fasterrcnn.pth')
