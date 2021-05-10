import cv2
import numpy as np


def OnMouseAction(event,x,y,flags,param):
    global coor_x, coor_y, coor
    if event == cv2.EVENT_LBUTTONDOWN:
        print("左键点击")
        print("%s" %x,y)
        coor_x ,coor_y = x ,y
        coor_m = [coor_x,coor_y]
        coor = np.row_stack((coor,coor_m))
        print(coor)
    elif event==cv2.EVENT_LBUTTONUP:
        cv2.line(img, (coor_x, coor_y), (coor_x, coor_y), (255, 255, 0), 7)

def video_info(camera, fps):
    if (camera.isOpened()):                               # 判断视频是否成功打开
        print('视频已打开')
    else:
        print('视频打开失败!')
    print('视频帧率：%d fps' %fps)                          # 获取视频帧率
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print ('原视频尺寸:'+str(size))                         # 输出视频尺寸

def get_chosse_action(img, OnMouseAction):
    while True:
        cv2.imshow('IImage',img)
        cv2.setMouseCallback('IImage',OnMouseAction)
        k = cv2.waitKey(1) & 0xFF
        if k == ord(' '):                                 # 空格完成退出操作
            break
    cv2.destroyAllWindows()                               # 关闭页面


def output_choose_vedio(coor, frame):
    Video_choose = frame[coor[1,1]:coor[2,1],coor[1,0]:coor[2,0]]
    out.write(Video_choose)
    cv2.imshow('Video_choose', Video_choose)


def get_sum_image(frame, coor, Width_choose, Height_choose):
    global emptyImage
    emptyImage = np.zeros((Width_choose * 10, Height_choose * 2, 3), np.uint8)
    gray_lwpCV = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                        # 转灰度图
    frame_data = np.array(gray_lwpCV)                                           # 每一帧循环存入数组
    box_data = frame_data[coor[1,1]:coor[2,1], coor[1,0]:coor[2,0]]             # 取矩形目标区域
    pixel_sum = np.sum(box_data, axis=1)                                        # 行求和q

    for i in range(Height_choose):
        cv2.rectangle(emptyImage, (int(i*2), int((Width_choose-pixel_sum[i]//255)*10)), (int((i+1)*2), int(Width_choose)*10), (255, 0, 0), 1)
    emptyImage = cv2.resize(emptyImage, (320, 240))




coor_x,coor_y, emptyImage = -1, -1, 0                   # 初始值并无意义,只是先定义一下供后面的global赋值改变用于全局变量
coor = np.array([[1,1]])

fourcc = cv2.VideoWriter_fourcc(*'XVID')                        # 使用XVID编码器
camera = cv2.VideoCapture('/home/cheng/Downloads/test_data/8m/2021-01-28-00-29-57_rgb_image_raw.mp4')     # 从文件读取视频,Todo:只需要修改成自己的视频路径即可进行测试
fps = camera.get(cv2.CAP_PROP_FPS)                              # 获取视频帧率
grabbed, img = camera.read()                                    # 逐帧采集视频流
video_info(camera, fps)
get_chosse_action(img, OnMouseAction)


Width_choose = coor[2,0]-coor[1,0]                              # 选中区域的宽
Height_choose = coor[2, 1] - coor[1, 1]                         # 选中区域的高
print("视频选中区域的宽：%d" %Width_choose,'\n'"视频选中区域的高：%d" %Height_choose)
out = cv2.VideoWriter('output_test1.avi',fourcc, camera.get(cv2.CAP_PROP_FPS), (Width_choose,Height_choose)) # 参数分别是：保存的文件名、编码器、帧率、视频宽高


def main():
    while True:
        grabbed, frame = camera.read()                                                  # 逐帧采集视频流，如果读取结束则退出
        if not grabbed:
            break
        
        output_choose_vedio(coor, frame)                                                # 输出选定区域内的视频
        get_sum_image(frame, coor, Width_choose, Height_choose)                         # 得到选定区域内的求和图

        cv2.rectangle(frame, tuple(coor[1,:]), tuple(coor[2,:]), (0, 255, 0), 2)        # 在原视频显示选定的框的范围
        cv2.imshow('lwpCVWindow', frame)                                                # 显示采集到的视频流
        cv2.imshow('sum', emptyImage)                                                   # 显示画出的条形图

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):                                                             # 按Q推出
            break
        
    out.release()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()