import numpy as np


def nms(bboxes, confidence_score, threshold):
    """非极大抑制过程
    :param bboxes: 同类别候选框坐标
    :param confidence: 同类别候选框分数
    :param threshold: iou阈值
    :return:
    """
    # 1.强转数组，并取出每个框左上角坐标和右下角坐标
    # 1.1 强转数组
    bboxes = np.array(bboxes)
    score = np.array(confidence_score)

    # 1.2 取出n个的极坐标点（左上角坐标和右下角坐标）
    x1 = bboxes[:, 0]
    y1 = bboxes[:, 1]
    x2 = bboxes[:, 2]
    y2 = bboxes[:, 3]
    # 1.3 计算每个框的面积
    areas = (x2 - x1) * (y2 - y1)

    # 2.对候选框进行NMS筛选
    # 2.1 返回的框坐标和分数
    picked_boxes = []
    picked_score = []
    # 2.2 对置信度进行排序, 获取排序后的下标序号, argsort默认从小到大排序
    order = np.argsort(score)
    while order.size > 0:
        # 2.3 将当前置信度最大的框加入返回值列表中
        index = order[-1]
        # 2.4 保留该类剩余box中得分最高的一个
        picked_boxes.append(bboxes[index])
        picked_score.append(confidence_score[index])

        # 2.5 计算交并比
        # 2.5.1 获取当前置信度最大的候选框与其他任意候选框的相交面积
        x11 = np.maximum(x1[index], x1[order[:-1]])
        y11 = np.maximum(y1[index], y1[order[:-1]])
        x22 = np.minimum(x2[index], x2[order[:-1]])
        y22 = np.minimum(y2[index], y2[order[:-1]])
        # 2.5.2 计算交集的面积,不重叠时面积为0
        w = np.maximum(0.0, x22 - x11)
        h = np.maximum(0.0, y22 - y11)
        intersection = w * h

        # 2.5.3 利用相交的面积和两个框自身的面积计算框的交并比
        ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)
        # 2.5.4 保留IoU小于阈值的box
        keep_boxes_indics = np.where(ratio < threshold)
        # 2.5.5 保留剩余的框
        order = order[keep_boxes_indics]
    # 2.6 返回NMS后的框及分类结果
    return picked_boxes, picked_score


if __name__ == "__main__":
    boxes = [(187, 82, 337, 317), (150, 67, 305, 282), (246, 121, 368, 304)]
    confidence_score = [0.9, 0.65, 0.8]
    threshold = 0.3
    picked_boxes, picked_score = nms(boxes, confidence_score, threshold)
    print(picked_boxes)
    print(picked_score)
