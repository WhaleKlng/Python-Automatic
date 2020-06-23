import os
import re
import time
from time import sleep
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

dr = re.compile(r'<[^>]+>', re.S)

def make_url(id): #传入作者id，返回作者主页的URL
    url = "https://author.baidu.com/home/" + str(id)
    return url

def get_soup(url):#传入作者主页URL，返回找出的所有视频li标签，所有的<li>是列表对象
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#tab > div.tab-wrap > div > div.tab-list > div:nth-child(3)')))
    button.click()
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    sleep(0.4)
    driver.execute_script(js1)
    time.sleep(2.5)
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'lxml')

    return soup

def mkdir(path):#自动生成路径
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    else:
        pass

def time_ok(p_time): #看是否符合时间条件
    global gy        #设置全局变量
    ts_n = time.time()
    cha=ts_n-float(p_time)
    t=int(gy)*3600
    if(cha<t):
        return 1
    else:
        return 0

def vid_ok(vid):
    result = []
    with open('D:\\百家指定作者采集\\vid_log.txt', 'r') as f:
        for line in f:
            result.append(list(line.strip('\n').split(','))[0])
    if vid in result:
        return 0
    else:
        return 1

def write_vid(vid): #写入vid到文本里面
    try:
        # 在E盘以只写的方式打开/创建一个名为 titles 的txt文件
        file = open(r'D:\百家指定作者采集\vid_log.txt', 'a')  #需要加一家日志存放位置
        file.write(vid + '\n')
    finally:
        if file:
            # 关闭文件（很重要）
            file.close()

def down_media(url,title): #自动下载视频到本地文件夹，只需要传入解析之后的URL即可
    local_path = r'D:\百家指定作者采集\好看视频采集'
    print('正在下载 %s  please wait....'%title,end=" ")
    request.urlretrieve(url,local_path + r'\%s.mp4'%title)
    print('本视频下载完成')

def do_li(soup):#传入一个作者的主页的所有li，逐一完成对每一个li的所有操作
    li = soup.find_all('li', 'cnt-list largevideo') # li的长度是20 列表对象[0][1]...
    l=len(li)
    i=0
    while i<l:
        do_1li(li[i])
        i+=1

def vidot_ok(dd):
    dd=dd[-5:]
    listt=list(dd)
    tn1=int(listt[0])*600+int(listt[1])*60+int(listt[3])*10+int(listt[4]) #视频秒数
    return tn1
def readnum_ok(readnum):
    qb=readnum[:-2]#9999   /  1.1万
    data=qb[-1:] #9  / 万
    if data=="万":
        return int(10000)*float(qb[:-1])
    else:
        return int(qb)

def do_1li(li):#传入某一个li，然后对每一个li进行提取，数据存储，（需要判断时间戳了）下载记录啊
    global axds
    global rdnum
    div = li.find_all('span')
    ptime = div[3].attrs['data-date']
    url = li.find_all('div', 'largevideo-box')
    url = url[0].attrs['data-src']
    data = li.attrs  # 得到的是一个字典
    id = data['data-dynamic_id']
    title = data['data-title']
    vidot = li.find('span', 'largevideo-time')
    readnum=li.find('span', 'pv')
    #print(vidot)
    dd = dr.sub('', str(vidot)) ##dd是一个字符串
    readdd=dr.sub('', str(readnum))
    #print(readdd)
    print(readnum_ok(readdd))
    if ((time_ok(ptime))and(vid_ok(id)))and((vidot_ok(dd)>int(0)))and((readnum_ok(readdd)>int(rdnum))):
        down_media(url,title)
        write_vid(id)

def do_onea(id):
    url = make_url(id)
    soup = get_soup(url)  # li是一个列表,当成列表用 一个作者主页的所有li
    do_li(soup)
def main():
    mkdir("D:\\百家指定作者采集\\好看视频采集")
    list1=[]
    with open('D:\\百家指定作者采集\\作者id.ini', 'r') as f:#成功读取每一个id
        for line in f:
            list1.append(list(line.strip('\n').split(','))[0])
    lenth=len(list1)
    k=0
    while k<lenth:
        do_onea(list1[k])
        k+=1

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    gy = input('采集多长时间以来的视频：')
    #axds = input('请输入采集视频的最短长度：')
    rdnum=input('请输入视频最小播放量')
    main()
    sada = input('所有符合条件的视频采集完毕，按任意键结束')
    driver.close()


