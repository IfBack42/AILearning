# 1.目标检测Demo
# # 导入预测工具
# import detect
#
# # 运行预测程序：指定要预测的图片，预训练好的模型及是否显示图片
# detect.run(source="data/images/bus.jpg", weights='yolov5s.pt', view_img=False)

# ------------------------------------------------------------------------------------------------------------------ #

# # 2.网络结构
# # 2.1 输入端
# from utils.augmentations import letterbox
# import matplotlib.pyplot as plt
# import cv2
#
# cat = plt.imread("data/images/bus.jpg")
# print(cat.shape)
# img = letterbox(cat, new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, stride=32)
# print(img[0].shape)
# plt.imshow(img[0])
# plt.show()

# ------------------------------------------------------------------------------------------------------------------ #

# 3.模型训练
# 导入模型训练
# import train
#
#
# if __name__ == '__main__':
#     # 模型训练：设置相应的参数：模型配置信息
#     train.run(cfg='models/yolov5s.yaml',  # 模型结构的配置文件
#               data='data/coco128.yaml',  # 数据的配置文件
#               imgsz=640,  # 图像大小
#               batch_size=2,  # 批次大小
#               weights='yolov5s.pt',  # 预训练模型
#               epochs=1,  # 训练轮次
#               worker=1,  # 数据加载的线程数，根据硬件资源进行设置
#               lr=0.01
#               )

# ------------------------------------------------------------------------------------------------------------------ #

# # 4.模型预测
# 导入预测工具
import detect

# 运行预测程序：指定要预测的图片，预训练好的模型及是否显示图片
detect.run(source="data/images/bus.jpg", weights='runs/train/exp/weights/best.pt', view_img=False)
