import os
import glob
from torch.utils.data import Dataset, DataLoader  
from torchvision.transforms import transforms
from PIL import Image 
import torch
import csv
import random

class GetData(Dataset):
    def __init__(self, root, resize, mode):
        super(GetData, self).__init__()
        self.root = root
        self.resize = resize
        self.name2label = {'empty': 0, 'occupied': 1}                   # "类别名称": 编号
        for name in sorted(os.listdir(os.path.join(root))):
            # 判断是否为一个目录
            if not os.path.isdir(os.path.join(root, name)):
                continue
            self.name2label[name] = self.name2label.get(name)           # 将类别名称转换为对应编号



        # image, label 划分
        self.images, self.labels = self.load_csv('images.csv')          # csv文件存在 直接读取
        # 正常测试集划分
        if mode == 'train':                                             # 80%划分为训练集                   
            self.images = self.images[:int(0.8 * len(self.images))]
            self.labels = self.labels[:int(0.8 * len(self.labels))]
        
        else:                                                           # 剩余20%划分为测试集
            self.images = self.images[int(0.8 * len(self.images)):]
            self.labels = self.labels[int(0.8 * len(self.labels)):]

        # 非正常测试集划分
        # if mode == 'train':                                             # 80%划分为训练集                   
            # self.images = self.images[:0]
            # self.labels = self.labels[:0]
        
        # else:                                                           # 剩余20%划分为测试集
            # self.images = self.images[:int(len(self.images))]
            # self.labels = self.labels[:int(len(self.labels))]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img, label = self.images[idx], self.labels[idx]
        
        tf = transforms.Compose([                                               # 常用的数据变换器
					            lambda x:Image.open(x).convert('RGB'),          # string path= > image data 
					                                                            # 这里开始读取了数据的内容了
					            transforms.Resize(                              # 数据预处理部分
					                (int(self.resize * 1.25), int(self.resize * 1.25))), 
					            transforms.RandomRotation(15), 
					            transforms.CenterCrop(self.resize),             # 防止旋转后边界出现黑框部分
					            transforms.ToTensor(),
					            transforms.Normalize(mean=[0.485, 0.456, 0.406],
					                                 std=[0.229, 0.224, 0.225])
       							 ])
        img = tf(img)
        label = torch.tensor(label)                                 # 转化tensor
        return img, label                                           # 返回当前的数据内容和标签
    
    def load_csv(self, filename):
        # 没有csv文件的话，新建一个csv文件
        if not os.path.exists(os.path.join(self.root, filename)): 
            images = []
            for name in self.name2label.keys():   
                images += glob.glob(os.path.join(self.root, name, '*.png'))
                images += glob.glob(os.path.join(self.root, name, '*.jpg'))
                images += glob.glob(os.path.join(self.root, name, '*.jpeg'))
            random.shuffle(images)

            with open(os.path.join(self.root, filename), mode='w', newline='') as f:
                writer = csv.writer(f)
                for img in images:                                              # './train/empty/spot429.jpg'
                    name = img.split(os.sep)[-2]                                # 截取出empty
                    label = self.name2label[name]                               # 根据种类写入标签
                    writer.writerow([img, label])                               # 保存csv文件
        	
        
        # 如果有csv文件的话直接读取
        images, labels = [], []
        with open(os.path.join(self.root, filename)) as f:
            reader = csv.reader(f)
            for row in reader:
                img, label = row
                label = int(label)
                images.append(img)
                labels.append(label)
        assert len(images) == len(labels)
        return images, labels
    

