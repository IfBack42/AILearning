import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from PIL import Image
from xml.dom.minidom import parse
import os
import albumentations as A
from albumentations.pytorch.transforms import ToTensor

VOC_BBOX_LABEL_NAMES = (
    '_backbone_',
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'pottedplant',
    'sheep',
    'sofa',
    'train',
    'tvmonitor')

class VocDataset(torch.utils.data.Dataset):
    def __init__(self, root,transforms = None):
        self.root = root
        self.transforms = transforms
        # load all image files, sorting them to ensure that they are aligned
        self.imgs = list(sorted(os.listdir(os.path.join(root, "JPEGImages"))))
        self.bbox_xml = list(sorted(os.listdir(os.path.join(root, "Annotations"))))
    

    def __getitem__(self, idx):
        # load images and bbox
        img_path = os.path.join(self.root, "JPEGImages", self.imgs[idx])
        bbox_xml_path = os.path.join(self.root, "Annotations", self.bbox_xml[idx])
        #img = Image.open(img_path).convert("RGB")  
        img = plt.imread(img_path).astype(np.float32)
        if img_path.find('000282.jpg') == 1:
            print(img_path)
            print("索引为：{}".format(idx))
        
        # 读取文件，VOC格式的数据集的标注是xml格式的文件
        dom = parse(bbox_xml_path)
        # 获取文档元素对象
        data = dom.documentElement
        # 获取 objects
        objects = data.getElementsByTagName('object')        
        # get bounding box coordinates
        boxes = []
        labels = []
        for object_ in objects:
            # 获取标签中内容
            name = object_.getElementsByTagName('name')[0].childNodes[0].nodeValue  # 就是label，mark_type_1或mark_type_2
            labels.append(VOC_BBOX_LABEL_NAMES.index(name))
            bndbox = object_.getElementsByTagName('bndbox')[0]
            xmin = np.float(bndbox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
            ymin = np.float(bndbox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
            xmax = np.float(bndbox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
            ymax = np.float(bndbox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
            boxes.append([xmin, ymin, xmax, ymax])        
 
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.as_tensor(labels, dtype=torch.int64)        
 
        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((len(objects),), dtype=torch.int64)
 
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        # 由于训练的是目标检测网络，因此没有教程中的target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        if self.transforms != None:
            sample = {
                        'image': img,
                        'bboxes': target['boxes'],
                        'labels': labels,
                        }
            sample = self.transforms(**sample)
            img = sample['image']
            target['boxes'] = torch.stack(tuple(map(torch.tensor, zip(*sample['bboxes'])))).permute(1, 0)
 
        return img, target
 
    def __len__(self):
        return len(self.imgs)
    

    @staticmethod
    def get_transform():
      	#	 图像增强进行翻转和类型的转换
        return A.Compose([
            A.Flip(0.5),
            A.Resize(height=800, width=800),
            ToTensor()
        ], bbox_params={'format': 'pascal_voc', 'label_fields': ['labels']})
  
    