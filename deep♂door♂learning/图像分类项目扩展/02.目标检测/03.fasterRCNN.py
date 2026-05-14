# 1.pytorh相关的工具包
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.io import read_image
from PIL import Image
import matplotlib.pyplot as plt

# 2.获取图片
img = Image.open('img3.jpg')
# plt.imshow(img)
# plt.show()
# print(img.size)

# 3.将图片格式转换为tensor形式，大小转换为800x800的大小
transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((800, 800))])
img = transform(img)

# 3.1 进行通道的调整并展示图片
plt.imshow(img.permute(1, 2, 0))
# print(img.shape)
# plt.show()



# 4.设置coco数据集的class，共90个类别：人，自行车，火车，。。。
coco_names = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# 5.实例化模型
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

# 6.将模型设置为eval模式
model.eval()
# print(model)

# 7.直接进行预测
pred = model([img])
# print(pred)

# 8.获取类别名称,框及对应的置信度
pred_class = [coco_names[i] for i in list(pred[0]['labels'].numpy())]
pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
pred_score = list(pred[0]['scores'].detach().numpy())

# print(pred_class)
# print(pred_score)

# 9.展示绘图结果
# 9.1 图像读取
img = Image.open('img3.jpg').resize((800, 800))
# 9.2 图像展示
fig = plt.imshow(img)
# # 9.3 将框绘制在图像上
# for index, boxes in enumerate(pred_boxes):
#     fig.axes.add_patch(plt.Rectangle(
#     xy=(boxes[0]), width=boxes[1][0]-boxes[0][0], height=boxes[1][1]-boxes[0][1],
#     fill=False, edgecolor="blue", linewidth=1))
# plt.show()


# 10.过滤分数较低的预测
threshold = 0.5
# 因pred_score是从大大小进行排列的，只要获取最后一个索引即可
pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
pred_boxes = pred_boxes[:pred_t + 1]
pred_class = pred_class[:pred_t + 1]

# 11.将过滤后的结构绘制在图像上
# 11.1 图像读取
img = Image.open('img3.jpg').resize((800, 800))
# 11.2 将框绘制在图像上
# fig = plt.imshow(img)
# for index, boxes in enumerate(pred_boxes):
#     fig.axes.add_patch(plt.Rectangle(
#         xy=(boxes[0]), width=boxes[1][0] - boxes[0][0], height=boxes[1][1] - boxes[0][1],
#         fill=False, edgecolor="g", linewidth=1))
# plt.show()



