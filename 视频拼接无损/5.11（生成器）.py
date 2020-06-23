import os
from collections import Counter
from os import listdir
from random import *
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from psutil import pids, Process, NoSuchProcess

clip_path = '.\\原始视频\\'
title_path = '.\\片头视频\\'
output_path = '.\\输出视频\\'
titlog_path = '.\\片头log\\'
log_path = '.\\log'

def kill_ffmpeg():
    for pid in pids():
        try:
            p = Process(pid)
            if 'ffmpeg' in p.name():
                p.terminate()
        except NoSuchProcess:
            pass

def group_same(tuple): #不含有同人片段则返回1
    group=[]
    for tul in tuple:
        group.append(tul[:-1])
    flag=1
    result_dict=dict(Counter(group))
    for key in result_dict:
        if result_dict[key]>1:
            flag=0
    return flag

def pick(clip_names, clip_num):
    while True:
        yield sample(clip_names, clip_num)

def cha(group,titlen):#返回一是有重复的
    flag=0
    with open(titlog_path+titlen, 'r', encoding='utf-8') as f:
        log = f.read()
        for tul in group:
            if log.find(tul)!=(-1):
                flag=1
    return flag


def clip(clip_num, output_num):
    clip_names = [file_name[:-4] for file_name in listdir(clip_path) if file_name.endswith('.mp4')]
    title_video_paths = [title_path + file_name for file_name in listdir(title_path) if file_name.endswith('.mp4')]  # 带路径的
    if clip_num > len(clip_names): #先判断一下能不能拼接吧
        print('原始视频数量不足，无法拼接')
        exit()
    for title in title_video_paths:
        print("正在处理片头系     %s   "%(title.split("\\")[-1]))
        done_num = 0
        for index, group in enumerate(pick(clip_names, clip_num)):#这地方就是填这个clip
            if done_num == output_num:#这个地方就是填output_num，
                break
            # 每个片段没有采集够clipnum个视频
            if group_same(group):#四个组合的片段不同人
                # 公司内有没出过相同的？
                new_video_name = '_'.join(group) + '.mp4'
                with open(log_path, 'r+', encoding='utf-8') as f:
                    log = f.read()
                    if new_video_name in log:
                        continue
                    else:#公司内不相同的, qingkuang
                        # 需要一个作者不重复使用某片段
                        titlen = title.split("\\")[-1].split(".")[0]
                        titlog=titlog_path+titlen
                        if os.path.isfile(titlog):#如果文件存在的话，就查重
                            with open(titlog, 'a', encoding='utf-8') as file:
                                if (cha(group,titlen)==0):
                                    f.write(new_video_name + '\n')  # 我宁可去重新生成 也不用重的 写进公司的
                                    file.write(new_video_name + '\n')  # 我宁可去重新生成 也不用重的 写进作者的
                                    print((group))
                                    video = concatenate_videoclips(
                                        [VideoFileClip(title)] +
                                        [VideoFileClip(clip_path + video + '.mp4') for video in group]
                                    )
                                    video.write_videofile(output_path + titlen + '%s.mp4' % (done_num + 1))
                                    done_num += 1
                                    kill_ffmpeg()

                        else:#文件都没有创建呢 那肯定是可以的啊
                            with open(titlog, 'w', encoding='utf-8') as file:
                                f.write(new_video_name + '\n')#我宁可去重新生成 也不用重的 写进公司的
                                file.write(new_video_name + '\n')#我宁可去重新生成 也不用重的 写进作者的
                                print((group))
                                video = concatenate_videoclips(
                                    [VideoFileClip(title)] +
                                    [VideoFileClip(clip_path + video + '.mp4') for video in group]
                                )
                                video.write_videofile(output_path + titlen + '%s.mp4' % (done_num + 1))
                                done_num += 1
                                kill_ffmpeg()

                        #kill_ffmpeg()

if __name__ == '__main__':
    clip(int(input('请输入片段拼接视频的数量：')), int(input('单片头输出几个视频：')))