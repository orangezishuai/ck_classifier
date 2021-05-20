import torch
from PIL import Image
from torchvision import transforms
from trainVGG16 import VGG16net
import sys
sys.path.append('mbv3')
from mobilenetv3 import mobilenetv3_small
import time
from getdata import GetData
from torch.utils.data import DataLoader

name2label = {'empty': 0, 'occupied': 1}
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cuda')
def image_transforms(image_path):
    resize = 224
    tf = transforms.Compose([                                               # 常用的数据变换器
                            lambda x:Image.open(x).convert('RGB'),          # string path= > image data 
                                                                            # 这里开始读取了数据的内容了
                            transforms.Resize(                              # 数据预处理部分
                                (int(resize * 1.25), int(resize * 1.25))), 
                            transforms.RandomRotation(15), 
                            transforms.CenterCrop(resize),             # 防止旋转后边界出现黑框部分
                            transforms.ToTensor(),
                            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                std=[0.229, 0.224, 0.225])
                            ])
    return tf(image_path)


test_batch_size = 16
test_dataset = GetData('./onebag', 224, 'test')
test_loader = DataLoader(test_dataset, batch_size=test_batch_size, shuffle=True)

def prediect():
    # model = mobilenetv3_small(num_classes=2).to(device)
    model = VGG16net().to(device)
    model.load_state_dict(torch.load('model/model.pth'))
    model.eval()
    # net = net.to(device)
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            start = time.time()
            output = model(images)
            _, predicted = torch.max(output.data, 1)
            print(predicted)
            end = time.time()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        acc = 100*(correct/total)
        print('Test Accuracy  {} %'.format(100*(correct/total)))


if __name__ == '__main__':
    prediect()
