import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from trainv3 import VGG16net
import time


def image_transforms(image):
    resize = 224
    tf = transforms.Compose([                                               # 常用的数据变换器
                            lambda x:x.convert('RGB'),                      # string path= > image data 
                                                                            # 这里开始读取了数据的内容了
                            transforms.Resize(                              # 数据预处理部分
                                (int(resize * 1.25), int(resize * 1.25))), 
                            transforms.RandomRotation(15), 
                            transforms.CenterCrop(resize),             # 防止旋转后边界出现黑框部分
                            transforms.ToTensor(),
                            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                std=[0.229, 0.224, 0.225])
                            ])
    return tf(image)

def prediect(imgg, model):
    # net = net.to(device)
    with torch.no_grad():
        img = image_transforms(imgg)
        img = img.unsqueeze(0)
        img_ = img.to(device)
        start = time.time()
        outputs = model(img_)
        _, predicted = torch.max(outputs, 1)
        predicted_number = predicted[0].item()
        end = time.time()
        label = list(name2label.keys())[list(name2label.values()).index(predicted_number)]
    return label

# 基本信息设置
name2label = {'empty': 0, 'occupied': 1}
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = VGG16net().to(device)
model.load_state_dict(torch.load('model/model.pth'))
final_spot_dict = {
    (895,  223,1080,  435): 1
}
video_name = '/home/cheng/Downloads/test_data/8m/2021-01-28-00-29-57_rgb_image_raw.mp4'
cap = cv2.VideoCapture(video_name)
ret = True
count = 0

fourcc = cv2.VideoWriter_fourcc(*'XVID')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
out = cv2.VideoWriter('./outputvideo/8moutput1.avi',fourcc, 10.0, (width, height))

while ret:
        ret, image = cap.read()
        count += 1
        if count == 5:
            count = 0
            
            new_image = np.copy(image)
            overlay = np.copy(image)
            cnt_empty = 0
            all_spots = 0
            color = [0, 255, 0] 
            alpha=0.5
            for spot in final_spot_dict.keys():
                all_spots += 1
                (x1, y1, x2, y2) = spot
                (x1, y1, x2, y2) = (int(x1), int(y1), int(x2), int(y2))
                #crop this image
                spot_img = image[y1:y2, x1:x2]
                # spot_img = cv2.resize(spot_img, (48, 48)) 
                start1 = time.time()
                spot_img = Image.fromarray(np.uint8(spot_img))
                end1 = time.time()
                print("time1 : " + str(end1 - start1))
                start2 = time.time()
                label = prediect(spot_img, model)
                # print(label)
                end2 = time.time()
                print("fps : " + str(1/(end2 - start2)))
                if label == 'empty':
                    cv2.rectangle(overlay, (int(x1),int(y1)), (int(x2),int(y2)), color, -1)
                    cnt_empty += 1

            cv2.addWeighted(overlay, alpha, new_image, 1 - alpha, 0, new_image)

            cv2.putText(new_image, "Available: %d spots" %cnt_empty, (30, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (255, 255, 255), 2)

            cv2.putText(new_image, "Total: %d spots" %all_spots, (30, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (255, 255, 255), 2)
            cv2.imshow('frame', new_image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            out.write(new_image)

out.release()
cv2.destroyAllWindows()
cap.release()