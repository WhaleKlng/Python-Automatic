#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import cv2
import os
from PIL import Image
from aip import AipOcr
high_size = 0#高
width_size = 0#宽
input_path = '.\\待提取视频\\'
cache_path1 = '.\\截图缓存\\'
cache_path2 = '.\\字幕缓存\\'
output_path = '.\\字幕文本\\'
def jt():  #截取视频 将来可以在这里加一个 要提取的视频的名字
    global high_size,width_size #后面修改用
    global input_path,cache_path1

    vc = cv2.VideoCapture(input_path+'1.mp4')  # 读入视频文件
    height=int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width=int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    high_size=int(height/5)
    width_size=int(width*4/5)
    c = 1
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
    timeF =int(int(vc.get(cv2.CAP_PROP_FPS))*2) # 视频帧计数间隔频率
    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if (c % timeF == 0):
            try:# 每隔timeF帧进行存储操作
                im = frame[int(4*height/5):height, int(width/10):int(9*width/10),0]
                img = Image.fromarray(im)
                img.save(cache_path1+'%s.jpg' % str(c))
            except:
                pass
        c = c + 1
    vc.release()
#成功截图 并且把全局变量得以改变

def pj(): #将来可以在这里加一个输出的图片的名字
    global high_size
    global width_size
    global cache_path1
    path =cache_path1
    path2=cache_path2
    '''
    imghigh = sum([len(x) for _, _, x in os.walk(os.path.dirname(path))])  # 获取当前文件路径下的文件个数
    print(imghigh)
    '''
    images = []  # 存储图像的名称的列表
    for root, dirs, files in os.walk(path):
        for f in files:
            images.append(f)
    # 至此已经把所有的图片导入到了images

    images.sort()
    images.sort(key=lambda x: int(x[:-4]))
    #成功把他安装数字大小排序
    for i in range((len(images) // 10)):  # 10个图像为一组，某一轮
        imagefile = []
        for j in range(10):
            imagefile.append(Image.open(path + '/' + images[i * 10 + j]))
        target = Image.new('RGB', (width_size, high_size * int(10)))  # 最终拼接的图像的大小
        left = 0
        right = high_size
        for image in imagefile:
            target.paste(image, (0, left, width_size, right))
            left += high_size  # 从上往下拼接，左上角的纵坐标递增
            right += high_size  # 左下角的纵坐标也递增
            target.save(path2 + 'result%s.jpg' % i, quality=100)
        imagefile = []

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def wordsb():
    global cache_path2
    global output_path

    # 定义常量
    APP_ID = '16158387'
    API_KEY = 'CStdIR7YDT4Ybt8jAC1gAsz2'
    SECRET_KEY = 'zRrRl3kCk1zKamWsjtreUGgRl230dniB'

    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
     }
    # 初始化AipFace对象
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    images = []  # 存储图像的名称的列表i
    for root, dirs, files in os.walk(cache_path2):
        for f in files:
            images.append(f)
    for im in images:  #
        print(im)
        filePath = cache_path2 + im
        result = aipOcr.basicGeneral(get_file_content(filePath), options)
        l = len(result['words_result'])
        i = 0
        while i < l:
            try:
                # 在E盘以只写的方式打开/创建一个名为 titles 的txt文件
                file = open(r'D:\Code\frames\字幕存放\vid_log.txt', 'a')  # 需要加一家日志存放位置
                file.write(result['words_result'][i]['words'] + '\n')
            finally:
                if file:
                    # 关闭文件（很重要）
                    file.close()
            i += 1

def mian():
    jt()
    pj()
    wordsb()

if __name__ == "__main__":
    mian()
