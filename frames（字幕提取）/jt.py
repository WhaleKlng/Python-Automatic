#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import cv2
from PIL import Image
vc = cv2.VideoCapture( 'D:\\try\\test.mp4')  # 读入视频文件
height=int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
width=int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
c = 1

if vc.isOpened():  # 判断是否正常打开
    rval, frame = vc.read()
else:
    rval = False

timeF =vc.get(cv2.CAP_PROP_FPS) # 视频帧计数间隔频率

while rval:  # 循环读取视频帧
    rval, frame = vc.read()
    if (c % timeF == 0):  # 每隔timeF帧进行存储操作
       # im = frame[:, :, 0]
        im = frame[int(4*height/5):height, 0:width,0]
        img = Image.fromarray(im)
        # img.show()
       # img.save('D:\\try\\tu\\ %s.jpg' % str(c))
        cv2.imwrite('D:\\try\\tu\\%s.jpg' % str(c), frame)  # 存储为图像
    c = c + 1
   ## cv2.waitKey(1)
vc.release()