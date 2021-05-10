from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def paste_img_fun(img, paste_path):

    paste_img = Image.open(paste_path)

    max_rule_width = img.size[0]
    max_rule_height = img.size[1]
    factor = np.random.randint(2, 7) / 17                   

    re_paste_img = paste_img.resize((int(factor * max_rule_width), int(factor * max_rule_height)))
    # 长度范围极端越界
    rand_width_pos_cr_w = np.random.randint((max_rule_width - (re_paste_img.size[0])), (max_rule_width - (re_paste_img.size[0]*2/3)))
    rand_height_pos_cr_w = np.random.randint(0, max_rule_height)

    # 高度范围极端越界
    rand_width_pos_cr_h = np.random.randint(0, max_rule_width)
    rand_height_pos_cr_h = np.random.randint((max_rule_width - (re_paste_img.size[0])), (max_rule_width - (re_paste_img.size[0]*2/3)))

    # 正常数据越界
    # rand_width_pos_cr = np.random.randint(0, (max_rule_width - (re_paste_img.size[0]*2/3)))
    # rand_height_pos_cr = np.random.randint(0, (max_rule_height - (re_paste_img.size[1]*2/3)))
    rand_width_pos = np.random.randint(0, (max_rule_width - re_paste_img.size[0]))
    rand_height_pos = np.random.randint(0, (max_rule_width - re_paste_img.size[1]))
    

    # 设置越界概率
    list = []
    for i in range(50):
        list.append(1)                     
    for x in range(50):
        list.append(0)                     
    a = np.random.choice(list)              
    if a == 0:
        rwp = rand_width_pos_cr_w
        rhp = rand_height_pos_cr_w
    if a == 1:
        rwp = rand_width_pos_cr_h
        rhp = rand_height_pos_cr_h



    img.paste(re_paste_img,(rwp,rhp,re_paste_img.size[0]+rwp,re_paste_img.size[1]+rhp),re_paste_img)
    
    # plt.imshow(img)
    # plt.show()

def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.png')]

# print(len(img_path))
# print(img_path)


def main():
    # 存储位置
    saveDir = './onebag/occupied'
    # 初始素材图片文件夹路径
    all_img_path = get_imlist("./png")
    # 背景库位路径
    
    for k in range(50):
        img_path = './kuwei/kuwei.png'
        img = Image.open(img_path)
        # 每次随机插入几个素材(5-15个)
        random_1 = np.random.randint(1, 3)
        for i in range(random_1):
            # 随机选定素材
            random_2 = np.random.randint(0, len(all_img_path))
            paste_path = all_img_path[random_2]
            paste_img_fun(img, paste_path)
        # plt.imshow(img)
        # plt.show()
        saveName = "onebag" + str(k) +".jpg"
        img = img.convert('RGB')
        img.save(os.path.join(saveDir, saveName))


if __name__ == '__main__':
    main()