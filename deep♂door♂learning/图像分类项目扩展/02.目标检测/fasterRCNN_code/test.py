# 使用测试集数据进行预测
# 1.导入依赖包
import torch
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datasets import Wheat
from torch.utils.data import DataLoader
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from dataset_utils import show_images, show_bboxes

# 2.加载数据并实例化数据读取类
# 2.1 设置测试数据集路径
test_data_dir = 'wheatData/test'
# 2.2 指明模型参数的路径
weight_dir = 'weights/fasterrcnn_resnet50_fpn.pth'
# 2.3 加载数据
test_data = pd.read_csv('wheatData/submission.csv')
print(test_data.tail())
# 2.4 实例化数据读取类
test_data = Wheat(test_data, test_data_dir, phase="test", transforms=Wheat.get_test_transform())


def collate_fn(batch):
    return tuple(zip(*batch))

# 2.5 设置batch_size
batchsize = 1
# 2.6 加载测试集数据
test_data_loader = DataLoader(
    # 测试数据
    test_data,
    # 批次大小
    batch_size=batchsize,
    # 测试集不需要打乱
    shuffle=False,
    # 不满batch的数据依然要进行预测
    drop_last=False,
    collate_fn=collate_fn
)

# 2.7 测试集图片的展示
for i, (imgs, img_id) in enumerate(test_data_loader):
    # 获取当前batch中的图像
    imgs = [imgs[j].permute(1, 2, 0) for j in range(batchsize)]
    # 图像展示
    for img in imgs:
        plt.imshow(img)
        plt.show()
    break


# 3.加载训练好的模型
# 3.1 设置设备信息
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
# 3.2 构建fasterRCNN模型
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False, pretrained_backbone=False)
# 3.3 类别个数：N+1
num_classes = 2
# 3.4 获取输出层输入特征向量的维度
in_features = model.roi_heads.box_predictor.cls_score.in_features
# 3.5 构建fasterRCNN的输出端
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
# print("当前任务的输出端{}".format(model.roi_heads.box_predictor))
# 3.6 加载训练好的参数
model.load_state_dict(torch.load(weight_dir, map_location=device))
model.to(device)
model.eval()


# 4.模型预测
# 4.1 设置阈值：删选置信度较高的数据
score_the = 0.7
img_outputs = []
# 4.2 遍历所有数据送入网络中进行预测
for images, img_ids in test_data_loader:
    images = list(image.to(device) for image in images)
    outputs = model(images)
    print(outputs)
    # 4.3 筛选结果，进行存储
    for img_id, output in zip(img_ids, outputs):
        boxes = output['boxes'].data.cpu().numpy()
        scores = output['scores'].data.cpu().numpy()
        mask = scores > score_the
        score = scores[mask]
        box = boxes[mask].astype(np.int32)
        img_outputs.append((img_id, box, score))


# 5.预测结果及展示
# 5.1 获取测试集图片数据
datas = [test_data[i] for i in range(0, len(img_outputs))]
imgs = [d[0].permute(1, 2, 0).numpy() for d in test_data]
# 5.2 图像展示
axes = show_images(imgs, 2, len(img_outputs) // 2)
# 5.3 预测框的展示
for ax, (img_id, boxes, score) in zip(axes, img_outputs):
    show_bboxes(ax, boxes, labels=None, colors=['blue'])
plt.show()
