# 1.导入工具包
import torchvision
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt

# 2.加载数据(公开数据集)
# train_data = torchvision.datasets.MNIST(root='./dataset', train=True, download=True)
# test_data = torchvision.datasets.MNIST(root='./dataset', train=False, download=True)
# print(f'类别索引：{train_data.class_to_idx}')
# print(len(train_data))

# 3.加载数据集（自定义的数据集）
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor, Resize
import matplotlib.pyplot as plt

# train_dataset = ImageFolder(root='dataset/flower_datas/train',
#                             transform=torchvision.transforms.Compose(
#                                 [ToTensor(), Resize((224, 224))]))


train_dataset = ImageFolder(root='dataset/flower_datas/train', transform=torchvision.transforms.Compose([ToTensor(),
                                                                                                         Resize((224,
                                                                                                                 224))]))

print(f'训练集的数量：{len(train_dataset.imgs)}')

# 绘图展示
# plt.show()
print(type(train_dataset.__getitem__(2000)[0]))
print(train_dataset.__getitem__(2000)[0].shape)
plt.imshow(train_dataset.__getitem__(2000)[0].permute(1, 2, 0))
plt.show()
