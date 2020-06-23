#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
import time
import requests
from urllib import request
pattern= re.compile(r'(?<=upic/).*?(?=/B)')# 先行编译了正则表达式 res3 = re.search(pattern,string) 用法  示例如下2019/04/26/17 只需要传入字符串string
def mkdir(path):#自动生成路径
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    else:
        pass

def down_media(url,caption):
    local_path=r'D:\快手视频采集'
    global num
    try:
        request.urlretrieve(url, local_path + r'\%s-%s.mp4' % (num, caption))
        num+=1
    except:
        request.urlretrieve(url, local_path + r'\%s-%s.mp4' % (num, time.time()))
        num += 1


def get_json(url):# 获取API接口的json
    # url='http://api.gifshow.com/rest/n/feed/hot?app=0&kpf=ANDROID_PHONE&ver=6.3&c=XIAOMI&mod=Xiaomi%28MI%208%20Lite%29&appver=6.3.2.8798&ftt=&isp=CMCC&kpn=KUAISHOU&lon=120.343858&language=zh-cn&sys=ANDROID_8.1.0&max_memory=256&ud=1311540528&country_code=cn&pm_tag=&oc=XIAOMI&hotfix_ver=&did_gt=1549244692851&iuid=&extId=8a6ca6915bd742fe4e7275c85d129582&net=WIFI&did=ANDROID_a4c0e69fbd323fe4&lat=30.317185'
    headers = {
         'Accept - Language': 'zh - cn',
         'User-Agent': 'kwai-android',
         'Content - Type': 'application / x - www - form - urlencoded',
         'Host': '101.251.217.216'
               }
    r = requests.get(url, headers=headers)
    jsondata=r.json() # jsdata已经是python对象,为字典对象
    return jsondata # 返回之

def url_1(url):
    try:
        res=re.search(pattern,url)[0] #返回了2019/04/25/21
        list = re.findall(r"\d+\.?\d*", res) #list 存储了年月日小时
        #开始构造抓取的url的时间戳
        year=list[0]
        month=list[1]
        day=list[2]
        hour=list[3]
        min=00
        sec=00
        #写入时间节点完成
        #开始构造时间戳
        str1 = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(min) + ":" + str(sec)
        ts_u = time.mktime(time.strptime(str1, "%Y-%m-%d %H:%M:%S"))
        ts_n = time.time()
        cha=ts_n-ts_u
        global time1
        t=3600*int(time1)
        if(cha<t):
            return 1
        else:
            return 0
    except:
        return 0

def re_url(json_dict):  # 放入json对象的字典形式，逐一地输出链接
    global num,x
    feeds=json_dict['feeds']  # 拿出json字典的feeds,为列表对象，需要审查这个feed的数组长度,注意我们需要的东西在feed是里面
    l=len(feeds) #长度为20个
    i=0
    while i<l:
        list1=feeds[i]    #list是20组（个内容），一组里面有标题，作者，链接（链接还要再进一层）
        #time.sleep(0.1)
        try:
            main_mv_urls=list1['main_mv_urls'] #在第一组中找到main_mv_urls,为列表对象
            caption=list1['caption'] #标题
            url=main_mv_urls[0]      # 找到了main_mv_url两个链接数组中的第一个，为字典对象,都是取链接数组字典里面的第一个，都可以!!!
        except:
            break
        nu=url['url']          # 本次的json所有的need url获取成功，需要正则筛选,用一个函数
        i = i + 1
        if (num<(int(x)+1))and(url_1(nu))==1:
            nunum=num
            print('正在下载第%s个视频'%nunum+'   %s,   请稍后......'%caption)
            down_media(nu,caption)
            print('第%s个视频' % nunum + '   %s,   下载成功！' % caption)
url='http://103.107.217.65/rest/n/feed/hot?isp=CMCC&mod=OPPO%28OPPO%20R11%29&pm_tag=&lon=101.565261&country_code=CN&kpf=ANDROID_PHONE&extId=62420079ff557d6c3c0feae0fb3ca44c&did=ANDROID_cc2f71dd0cf27225&kpn=KUAISHOU&net=WIFI&app=0&oc=MYAPP%2C1&ud=1311540528&hotfix_ver=&c=MYAPP%2C1&sys=ANDROID_5.1.1&appver=6.3.1.8720&ftt=&language=zh-cn&iuid=&lat=33.999458&did_gt=1554987561809&ver=6.3&max_memory=192&type=7&page=1&coldStart=false&count=20&pv=false&id=239&refreshTimes=2&pcursor=&source=1&needInterestTag=false&browseType=1&seid=f964320c-7380-4ca6-b0e3-798c406042ed&__NStokensig=70a917d30d70b23f476661829f87ef3ea59ab851561c8468c77103fb1b03ef97&token=0f9336edf3344759823e37022d6bb1b9-1311540528&client_key=3c2cd3f3&os=android&sig=564b9941599f1aa7b4e7d6377cb1767a'
mkdir("D:\\快手视频采集")
time1=input("请老板输入你想要多少小时以内的视频啊？打数字就行了：")
x=input("你想要几个视频啊?打数字就行了： ")
num=1
print('正在获取视频.........')
print('没说下载完成就不要关了它，因为它没有卡，它真的在动，只是你没看到而已！')
while num<(int(x)+1):
    json=get_json(url)
    time.sleep(1)
    re_url(json)#一次刷新的全部链接
s=input('视频下载完成，祝愿咱们搬运发大财')
    #num=num+1
   # print(alllist)

