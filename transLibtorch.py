import torch
import torchvision
from PIL import Image
import numpy as np
# from trainVGG16 import VGG16net

# 图片发在了build文件夹下
image = Image.open("/home/cheng/git/new_parking/onebag/occupied/onebag21.jpg")
image = image.resize((224, 224), Image.ANTIALIAS)
image = np.asarray(image)
image = image / 255
image = torch.Tensor(image).unsqueeze_(dim=0)
image = image.permute((0, 3, 1, 2)).float()

# model = VGG16net().to('cpu')
# model.load_state_dict(torch.load('/home/cheng/git/new_parking/model/model.pth', map_location=torch.device('cpu'))
model = torch.load('/home/cheng/git/new_parking/model/model.pth', map_location=torch.device('cpu'))
model.eval()
input_cpu_ = image.cpu()


torchd_cpu = torch.jit.trace(model, input_cpu_)
torch.jit.save(torchd_cpu, "cpu.pth")

