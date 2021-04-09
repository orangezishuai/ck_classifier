import cv2
import numpy as np


def OnMouseAction(event,x,y,flags,param):
    global coor_x, coor_y, coor, num_list_pro, num_list
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        counter = counter + 1                               # 每点击一次计数器+1
        if(counter % 2 == 0):                               # 每两个点更新一下pro值        
            num_list_pro += 2
            num_list.append(num_list_pro)                   # 得到列表 [1,3,5]
        coor_x ,coor_y = x ,y
        coor_m = [coor_x,coor_y]
        coor = np.row_stack((coor,coor_m))
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


def output_choose_vedio(fourcc, fps, coor, frame, num_i):
    Width_choose = coor[num_i+1,0]-coor[num_i,0]
    Height_choose = coor[num_i+1, 1] - coor[num_i, 1]
    out = cv2.VideoWriter('output_test%d.avi' %int(num_i / 2),fourcc, fps, (Width_choose,Height_choose))
    Video_choose = frame[coor[num_i,1]:coor[num_i+1,1],coor[num_i,0]:coor[num_i+1,0]]
    out.write(Video_choose)
    cv2.imshow('Video_choose %d' %int(num_i / 2), Video_choose)
    cv2.rectangle(frame, tuple(coor[num_i,:]), tuple(coor[num_i +1,:]), (0, 255, 0), 2) 




coor_x,coor_y = -1, 0                   # 初始值并无意义,只是先定义一下供后面的global赋值改变用于全局变量
coor = np.array([[1,1]])

counter = 0                             # 计数器
num_list_pro = -1                       # 生成每个num_i,每两个点生成
num_list = []                           # 将得到的num_i 存入列表，最后的形式[1,3,5,7·····]



fourcc = cv2.VideoWriter_fourcc(*'XVID')                        # 使用XVID编码器
camera = cv2.VideoCapture('/home/cheng/Desktop/12.mp4')         # 从文件读取视频,Todo:只需要修改成自己的视频路径即可进行测试
fps = camera.get(cv2.CAP_PROP_FPS)                              # 获取视频帧率
grabbed, img = camera.read()                                    # 逐帧采集视频流
video_info(camera, fps)
get_chosse_action(img, OnMouseAction)


def main():
    while True:
        grabbed, frame = camera.read()                                                      # 逐帧采集视频流，如果读取结束则退出
        if not grabbed:
            break
        
        for value in num_list:
            output_choose_vedio(fourcc, fps, coor, frame, value)
                                                                             

        cv2.imshow('video', frame)                                                          # 显示采集到的视频流
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):                                                                 # 按Q推出
            break

    # out.release()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()