# 本代码主要提供一些针对图像分类的数据增强方法

# 1、平移。在图像平面上对图像以一定方式进行平移。
# 2、翻转图像。沿着水平或者垂直方向翻转图像。
# 3、旋转角度。随机旋转图像一定角度; 改变图像内容的朝向。
# 4、随机颜色。包括调整图像饱和度、亮度、对比度、锐度
# 5、缩放变形图片。
# 6、二值化图像。
# 7、随机黑色块遮挡
# 8、添加噪声
# @ author : cheng

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageChops
import os
import numpy as np


# 1、图像平移
def move(img): #平移，平移尺度为off
    # img = Image.open(os.path.join(root_path, img_name))
    offset = ImageChops.offset(img, np.random.randint(1, 20), np.random.randint(1, 40))
    return offset

# 2、翻转图像
def flip(img):   #随机翻转图像，水平或者左右
    # img = Image.open(os.path.join(root_path, img_name))
    factor = np.random.randint(1, 3)
    if factor == 1:
        filp_img = img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        filp_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return filp_img

#  3、旋转角度
def rotation(img):
    # img = Image.open(os.path.join(root_path, img_name))
    factor = np.random.randint(1, 21)
    rotation_img = img.rotate(factor) #旋转角度
    return rotation_img

# 4、随机颜色 
def color(img): #随机颜色
    """
    对图像进行颜色抖动
    :param image: PIL的图像image
    :return: 有颜色色差的图像image
    """
    # image = Image.open(os.path.join(root_path, img_name))
    random_factor = np.random.randint(5, 15) / 10.  # 随机因子
    color_image = ImageEnhance.Color(img).enhance(random_factor)                   # 调整图像的饱和度
    random_factor = np.random.randint(8, 15) / 10.  # 随机因子
    brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)   # 调整图像的亮度
    random_factor = np.random.randint(10, 13) / 10.  # 随机因子
    contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
    random_factor = np.random.randint(5, 31) / 10.  # 随机因子
    random_color = ImageEnhance.Sharpness(contrast_image).enhance(random_factor)     # 调整图像锐度
    return random_color 

# 5、缩放变形图片
def crop(img):
    factor_1 = np.random.randint(10, 50)
    factor_2 = np.random.randint(20, 50)
    crop_img = img.crop((img.size[0]/factor_1, img.size[1]/factor_2, img.size[0]*(factor_1-1)/factor_1, img.size[1]*(factor_2-1)/factor_2))
    cropResize_img = crop_img.resize((img.size[0], img.size[1]))
    return cropResize_img

# 6、二值化图像
def convert(img):
    convert_img = img.convert('L')
    return convert_img


# 7、黑色块遮挡
def paste(img):
    # 左上右下
    factor_1 = np.random.randint(20, 70)
    factor_2 = np.random.randint(30, 60)
    # img.paste((0,0,0),(20.3, 10.4, 50, 60))
    # 随机进行左边遮罩
    a = np.random.randint(1,3)
    if a == 2:
        img.paste((0,0,0),(int(img.size[0]*(factor_1-np.random.randint(2,4))/factor_1), 
                        int(img.size[1]*(np.random.randint(1,25))/factor_2), 
                        int(img.size[0]*(factor_1-np.random.randint(0,2))/factor_1),
                        int(img.size[1]*(np.random.randint(26,50))/factor_2)
                        ))
    else:
        # 随机进行底部遮罩
        img.paste((0,0,0),(int(img.size[0]*(np.random.randint(1,19))/factor_1), 
                        # int(img.size[1]*(factor_2-2)/factor_2), 
                        int(img.size[1]*(factor_2-np.random.randint(3,6))/factor_2),
                        int(img.size[0]*(np.random.randint(21,41))/factor_1),
                        # int(img.size[1]*(factor_2-1)/factor_2)
                        int(img.size[1]*(factor_2-np.random.randint(0,3))/factor_2)
                        ))
    return img


# 8、随机添加黑白噪声
def salt_and_pepper_noise(img, proportion = 0.00025):
    noise_img = img
    height,width =noise_img.size[0],noise_img.size[1]
    proportion = proportion * np.random.randint(1, 50)
    num = int(height * width * proportion) #多少个像素点添加椒盐噪声
    pixels = noise_img.load()
    for i in range(num):
        w = np.random.randint(0,width-1)
        h = np.random.randint(0,height-1)
        if np.random.randint(0,2) == 1:
            pixels[h,w] = 0
        else:
            pixels[h,w] = 255
    return noise_img


# # 9、添加爱高斯噪声
# def gauss_noise(img):
#     sigma = np.random.randint(6, 12)
#     gauss_img = img
#     height, width = gauss_img.size[0], gauss_img.size[1] 
#     noise = np.random.randn() 
#     pixels = gauss_img.load()
#     num = int(height * width)
#     for i in range(num):
#         w = np.random.randint(0,width-1)
#         h = np.random.randint(0,height-1)
#         pixels[h,w] = pixels[h,w] + int(noise)
#     return noise_img



# 概率执行函数
def random_run(probability, func, useimage):
    """以probability%的概率执行func(*args)"""
    list = []
    for i in range(probability):
        list.append(1)                      #list中放入probability个1
    for x in range(100 - probability):
        list.append(0)                      #剩下的位置放入0
    a = np.random.choice(list)              #随机抽取一个
    if a == 0:
        return useimage
    if a == 1:
        image = func(useimage)
        return image




def main():
    imageDir = "./pricture/"            #要改变的图片的路径文件夹
    saveDir = "./save/"                 #要保存的图片的路径文件夹
    for name in os.listdir(imageDir):
        i=0
        for i in range(10):
            i = i+1
            saveName = str(name[:-4]) + str(i) +".jpg"
            img = Image.open(os.path.join(imageDir, name))
            saveImage = random_run(60, flip, img)                               # 翻转
            saveImage = random_run(70, color, saveImage)                        # 色彩变化
            saveImage = random_run(30, crop, saveImage)                         # 裁减缩放
            saveImage = random_run(30, paste, saveImage)                        # 添加遮罩
            saveImage = random_run(20, move, saveImage)                         # 平移
            saveImage = random_run(50, rotation, saveImage)                     # 旋转
            saveImage = random_run(10, convert, saveImage)                      # 二值化  
            saveImage = random_run(20, salt_and_pepper_noise, saveImage)        # 添加噪声点
            # saveImage = random_run(90, gauss_noise, saveImage)
            print(type(saveImage))
            if saveImage != None:
                saveImage.save(os.path.join(saveDir, saveName))
            else:
                pass
            print(i)


if __name__ == "__main__":
    main()