# 1.导入工具包
from PIL import Image  # pip install pillow
from torchvision import transforms
import matplotlib.pyplot as plt

# 2.读取图片
dog = Image.open('./dog.jpg')
# 3. 图像展示
plt.imshow(dog)
plt.show()

# -----------------------------图像增强（几何+颜色）---------------------------------------- #

# 1.几何增强
# 1.1水平翻转
transforms_RH = transforms.RandomHorizontalFlip(p=0.8)
dog_RH = transforms_RH(dog)
plt.imshow(dog_RH)
# plt.show()

# 1.2垂直翻转
transforms_RV = transforms.RandomVerticalFlip(p=0.1)
dog_RV = transforms_RV(dog)
plt.imshow(dog_RV)
# plt.show()
#
# 1.3 裁剪
transforms_Crop = transforms.RandomCrop(size=(500, 700))
dog_crop = transforms_Crop(dog)
plt.imshow(dog_crop)
# plt.show()

# 1.4 缩放
transforms_Resize = transforms.Resize(size=(224, 224))
dog_resize = transforms_Resize(dog)
plt.imshow(dog_resize)
# plt.show()


# 2.颜色增强
transforms_color = transforms.ColorJitter(brightness=0.6, contrast=0.6, saturation=0.6, hue=0.05)
dog_color = transforms_color(dog)
plt.imshow(dog_color)
plt.show()

# 3.增强方式的组合
transform = transforms.Compose([
    transforms_Resize,
    transforms_RH,
    transforms_color
])

dog_ = transform(dog)
plt.imshow(dog_)
plt.show()
