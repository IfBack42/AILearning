"""
 计算机视觉模块 torchvision自带的 CIFAR10数据集, 包含6W张 (32,32,3)的图片, 5W张训练集, 1W张测试集, 10个分类, 每个分类6K张图片.

 颜色增强参数介绍：
    brightness（亮度）:
        控制图像亮度的变化范围。
        如果是数值 b，则亮度会在 [max(0, 1-b), 1+b] 范围内随机调整。
        示例：设置为 0.6 表示亮度会从 0.4 到 1.6 的范围内变化。
    contrast（对比度）:
        控制图像对比度的变化范围。
        类似地，如果值为 c，则对比度将在 [max(0, 1-c), 1+c] 区间内随机选取。
        设置成 0.6 意味着对比度取值于 [0.4, 1.6]。
    saturation（饱和度）:
        控制图像饱和度的变化程度。
        值域规则同上。
        设定为 0.6 代表图像饱和度将被缩放到 [0.4, 1.6] 之间的一个因子。
    hue（色相）:
        改变图像的颜色（即色相）。
        取值应在 [0, 0.5] 之间；较小的变动更自然。
        若设为 0.05，表示色相会在 [-0.05, 0.05] 的区间中做偏移。
    """

import matplotlib.pyplot as plt
from torchvision.datasets import CIFAR10
from torchvision.datasets import ImageFolder
from torchvision import transforms
import numpy as np

def create_transform():
    # 1.定义数据增强transforms 用于增强训练数据的多样性，提高模型泛化能力
    transform_Horizon = transforms.RandomHorizontalFlip(p=0.5) # 随机水平翻转
    transform_Rotation = transforms.RandomRotation(45)         # 随机旋转
    transform_Color = transforms.ColorJitter(brightness=0.6, contrast=0.6, saturation=0.6, hue=0.05) # 定义颜色抖动变换，随机调整图像的亮度、对比度、饱和度和色相
    # transform_RS = transforms.Resize(size=(256, 256)) # 这里数据集很规范所以不需要resize

    # 2.分别 整合 训练集和测试集的数据增强方式
    train_transform = transforms.Compose([ # 训练集数据增强
        transform_Color,
        transform_Rotation,
        transform_Horizon,
        transforms.ToTensor() # 将图像数据转换为张量，且把通道从HWC变成CHW！
    ])
    test_transorm = transforms.Compose([ # 测试集图像增强，需要保持最原始的样子，所以只需要ToTensor
        # transform_RS,
        transforms.ToTensor()
    ])

    return train_transform,test_transorm

# 准备数据集（不包括dataloader）
def create_dataset(CIFAR_root=None,test_path=None,train_path=None):
    train_transform,test_transform = create_transform()

    # 3.获取测试集，并设置图像增强
    if train_path and test_path:
        train_dataset = ImageFolder(root=train_path,transform=train_transform)
        test_dataset = ImageFolder(root=test_path,transform=test_transform)
    elif CIFAR_root:
        train_dataset = CIFAR10(root=CIFAR_root, train=True, transform=train_transform, download=True)
        test_dataset = CIFAR10(root=CIFAR_root, train=False, transform=test_transform, download=True)
    else:
        raise ValueError("必须提供 train_path 和 test_path 或者 CIFAR_root ")
    return train_dataset,test_dataset

if __name__ == '__main__':
    # 测试返回数据
    train_transform,_ = create_transform()

    from PIL import Image
    image = Image.open('../../data/test.png') # 先将图片用PIL格式打开，才能传入transfer
    test_img = train_transform(image)  #  transform设置了to_tensor参数，返回张量
    test_img = np.array(test_img)      # 再转回 numpy，plt.imshow接收np数组类型
    test_img = np.transpose(test_img,(1,2,0)) # np数组没有permute，张量专属

    """
    这一段弄了挺久：
        1.transform需要传入的图像是PIL格式，而plt.imread是np数组格式，但是训练时不需要手动转为PIL格式是因为imgfolder自动封装
        2.transform加入了to_tenser，会将PIL转为张量
        3.plt.imshow接收np数组类型，需要将张量又转回np数组
        4.np数组没有permute，需要使用np.transpose
    """

    plt.imshow(test_img)
    plt.show()

