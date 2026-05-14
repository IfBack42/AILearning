# 1.导入相应的工具包
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataset_utils import show_images, show_bboxes
import torch
from torch.utils.data import Dataset
import albumentations as A
from albumentations.pytorch.transforms import ToTensor


# 2.定义数据读取类
class Wheat(Dataset):
    # 2.1 初始化
    def __init__(self, dataframe, image_dir, phase='train', transforms=None):
        '''
        :param dataframe: 数据标注结果
        :param image_dir: 图像路径
        :param phase: 训练阶段train或预测阶段test
        :param transforms: 图像增强处理
        '''
        super().__init__()
        # 2.1.1 数据标注的CSV结果
        self.df = dataframe
        # 2.1.2 图像路径
        self.image_dir = image_dir
        # 2.1.3 阶段信息
        self.phase = phase
        # 2.1.4 图像增强方法
        self.transforms = transforms
        # 2.1.5 图像文件名称：去重之后的结果
        self.image_id = dataframe["image_id"].unique()

    # 2.2 获取数据的数量
    def __len__(self):
        return len(self.image_id)

    # 2.3 获取每一幅图片
    def __getitem__(self, idx):
        # 2.3.1 获取图像信息
        image_id = self.image_id[idx]
        image = plt.imread(f'{self.image_dir}/{image_id}.jpg').astype(np.float32) / 255.0
        # 2.3.2 训练阶段
        if self.phase == 'train':
            # 2.3.3 根据图像的名称获取对应的标注信息
            records = self.df[self.df['image_id'] == image_id]
            # 2.3.4 获取目标框
            boxes = records[['x', 'y', 'w', 'h']].values
            # 2.3.5 获取目标框的右下角坐标
            boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
            boxes[:, 3] = boxes[:, 1] + boxes[:, 3]
            # 2.3.6 每一框的类别为小麦，设为1（因为只有一个类别）
            labels = torch.ones((records.shape[0],), dtype=torch.int64)
            # 2.3.7 设置目标值信息，目标值存放在target字典中：目标框的位置，目标类别值
            target = {}
            target['boxes'] = boxes
            target['labels'] = labels
            # 2.3.8 增强处理
            if self.transforms:
                # 1 增强的内容包括：图像，框和类别
                sample = {
                    "image": image,
                    'bboxes': target["boxes"],
                    "labels": labels
                }
                # 2 将sample字典中的key和value解包为key=value的方式传输到数据增强方法中
                sample = self.transforms(**sample)
                # 3 获取增强后的图像
                image = sample["image"]
                # 4 对图像中的标注框坐标进行拼接，并调整成n*4的维度,n表示图像的目标框的数量
                target['boxes'] = torch.stack(tuple(map(torch.tensor, zip(*sample['bboxes'])))).permute(1, 0)
            # 5 返回增强后的图像，目标值和对应的图像名称
            return image, target, image_id
        # 2.3.3 预测阶段
        else:
            # 预测阶段只需对图像进行处理，没有目标值
            if self.transforms:
                sample = {"image": image}
                sample = self.transforms(**sample)
                image = sample['image']
            return image, image_id

    # 2.4 定义图像增强策略（训练+测试）
    # 2.4.1 训练阶段图像增强进行翻转（注意框也会随之变换）和类型的转换
    @staticmethod
    def get_transform():
        return A.Compose([
            A.Flip(0.5),
            ToTensor()
        ], bbox_params={'format': 'pascal_voc', 'label_fields': ['labels']})

    # 2.4.2 预测时只需要进行类型的转换
    @staticmethod
    def get_test_transform():
        return A.Compose([
            ToTensor()
        ])


if __name__ == "__main__":
    # 1.获取数据和标签信息
    train_data_dir = 'wheatData/train'
    train_data = pd.read_csv('wheatData/train_data.csv')
    dataset = Wheat(train_data, train_data_dir, transforms=Wheat.get_transform())
    datas = [dataset[i] for i in range(10, 12)]
    # 2.获取图像数据（CHW-》HWC）
    imgs = [d[0].permute(1, 2, 0).numpy() for d in datas]
    # img = data[0].permute(1,2,0).numpy()
    axes = show_images(imgs, 1, 2)
    for ax, (image, target, image_id) in zip(axes, datas):
        print(list(target['labels'].numpy()))
        show_bboxes(ax, target['boxes'], labels=list(target['labels'].numpy()), colors=['w'])
    plt.show()
