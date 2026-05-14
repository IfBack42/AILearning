import numpy as np


# 1.定义方法计算IOU
def Iou(box1, box2):
    # 1.1 使用极坐标形式表示：直接获取两个bbox的坐标，获取两个框的左上角坐标和右下角坐标
    xmin1, ymin1, xmax1, ymax1 = box1
    xmin2, ymin2, xmax2, ymax2 = box2
    # 1.2 获取矩形框交集对应的左上角和右下角的坐标（intersection）
    xx1 = np.max([xmin1, xmin2])
    yy1 = np.max([ymin1, ymin2])
    xx2 = np.min([xmax1, xmax2])
    yy2 = np.min([ymax1, ymax2])
    # 1.3 计算两个矩形框面积
    area1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    area2 = (xmax2 - xmin2) * (ymax2 - ymin2)
    # 1.4 计算交集面积
    inter_area = (np.max([0, xx2 - xx1])) * (np.max([0, yy2 - yy1]))
    # 1.5 计算交并比
    iou = inter_area / (area1 + area2 - inter_area)
    return iou


if __name__ == "__main__":
    True_bbox, predict_bbox = [100, 35, 398, 400], [40, 150, 355, 398]
    iou = Iou(True_bbox, predict_bbox)
    print(iou)
