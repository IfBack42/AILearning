# 1.pytorh相关的工具包
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.io import read_image
from PIL import Image
import matplotlib.pyplot as plt

# 2.图像读取并转换
img = Image.open('img3.jpg')

transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((800, 800))])
img_transform = transform(img)

# 3.实例化模型
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 4.送入网络中的数据是【N,C,H,W】
images = [img_transform]
images, targets = model.transform(images, targets=None)

# 5.使用backbone获取特征图
features_body = model.backbone.body(images.tensors)
C2, C3, C4, C5 = features_body.values()
# print(C2.shape)
# print(C3.shape)
# print(C4.shape)
# print(C5.shape)


# 6.FPN网络融合：C2,C3,C4,C5是resnet提取的特征结果
features_fpn = model.backbone.fpn(features_body)
P2, P3, P4, P5, P6 = features_fpn.values()
# print(P2.shape)
# print(P3.shape)
# print(P4.shape)
# print(P5.shape)
# print(P6.shape)

# 7.RPN网络
# 7.1 生成anchors,送入图片信息及相应的特征图
anchors = model.rpn.anchor_generator(images, [P2, P3, P4, P5, P6])
# print(anchors)
# print(anchors[0].shape)

# 7.1.2 将生成的anchor绘制在图像上
# 将框绘制在图像上
fig = plt.imshow(img)
# for index, boxes in enumerate(anchors[0]):
#     if index < 1000:
#         fig.axes.add_patch(plt.Rectangle(
#             xy=(boxes[0], boxes[1]), width=boxes[2] - boxes[0], height=boxes[3] - boxes[1],
#             fill=False, edgecolor="red", linewidth=1))
# plt.show()

# 7.2 RPN分类和RPN回归
# 7.2.1 RPN网络预测分类，返回：logits送入softmax之前的分数
cls_logits = model.rpn.head.cls_logits(P3)
# 7.2.2 RPN网络预测目标框
box_pred = model.rpn.head.bbox_pred(P4)
# print(cls_logits.size())
# print(box_pred.size())
# print(cls_logits)

# 7.3 Proposal层（修正目标框）
# 7.3.1 RPN网络生成proposal
proposal = model.rpn(images, features_fpn)
# print(proposal[0][0].size())
# print(proposal)


# 7.3.2 候选区域的绘制
# 将候选区域显示在图像上
fig = plt.imshow(img)
# for index, boxes in enumerate(proposal[0][0]):
#     fig.axes.add_patch(plt.Rectangle(
#         xy=(boxes[0], boxes[1]), width=boxes[2] - boxes[0], height=boxes[3] - boxes[1],
#         fill=False, edgecolor="blue", linewidth=0.5))
# plt.show()

# 8.ROI Pooling层实现
pool_region_list = model.roi_heads.box_roi_pool(features_fpn, proposal[0], images.image_sizes)
print(pool_region_list.size())

# 9.目标分类与回归
# 9.1 模型最终输出的结果
detection = model.roi_heads(features_fpn, proposal[0], images.image_sizes)
print(detection)

# 9.2 检测结果的绘制
detection_boxes = detection[0][0]['boxes'].detach().numpy()
# 9.2.1 将检测结果绘制在图像上
fig = plt.imshow(img)
for index, boxes in enumerate(detection_boxes):
    fig.axes.add_patch(plt.Rectangle(
        xy=(boxes[0], boxes[1]), width=boxes[2] - boxes[0], height=boxes[3] - boxes[1],
        fill=False, edgecolor="purple", linewidth=1))
plt.show()