#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#导入所需要的包
import os
import time
import pickle
from os import listdir
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#所需要的路径
cookies_path = '.\\cookies\\'
article_path='.\\article\\'
article_list= [file_name for file_name in listdir(article_path)]
cook_list= [filename for filename in listdir(cookies_path)]
anum=0
cnum=0
#初始化浏览器，并到指定网址，开发者模式

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=option)
wait = WebDriverWait(driver, 10)
driver.get(url='https://mp.dayu.com/dashboard/article/write')

#设置指定用户的cookies,传入username
def set_cookie(cookpath):
    '''往浏览器添加cookie'''
    '''利用pickle序列化后的cookie'''
    try:
        cookies = pickle.load(open(cookpath, "rb"))
        for cookie in cookies:
            cookie_dict = {
                "domain": ".dayu.com",  # 火狐浏览器不用填写，谷歌要需要
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": "",
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False}
            driver.add_cookie(cookie_dict)
    except Exception as e:
        print(e)

#上传文件或者图片，传入文件的绝对路径即可，浏览器类型，exe路径都已经指定完毕
def sc_img(imgdic):
    path_01 = r"Upload.exe %s %s" % ("chrome", imgdic)
    r_v = os.system(path_01)

#一次发表的细节操作，前提是已经进到了图文发表页面，传入文章的绝对路径即可
def sc_word(wdic): #放入需要插入的word的位置！ 绝对路径
    title=os.path.basename(wdic)
    title=title.split('.')[0]
    input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]')))
    input.send_keys(title)  # 标题输入完毕
    drwd = driver.find_element_by_class_name("import_doc_link")
    try:
        ActionChains(driver).click(drwd).perform()
    except Exception as e:
        print('fail')
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.widgets-pop.w-scrollbar > div > div.widgets-pop_content.w-scrollbar > div > div.article-write-importDocDialog_local > div:nth-child(1) > button')))
    button.click()
    sc_img(wdic)
    #导入成功，准备确认发表
    fb = driver.find_element_by_css_selector("body > div.container > div.w-contentbox > div > div:nth-child(2) > div > div.article-write_box.w-scrollbar.article-write_box_rightbox > div.article-write_box-opt > div > button.w-btn.w-btn_primary")
    time.sleep(15)
    js1 = "window.scrollTo(0,document.body.scrollHeight)"
    time.sleep(0.5)
    driver.execute_script(js1)
    time.sleep(1.5)
    while True:
            try:
                ActionChains(driver).click(fb).perform()
                qrfb=driver.find_element_by_css_selector("body > div.widgets-pop.w-scrollbar > div > div.widgets-pop_content.w-scrollbar > div > div.article-write-preview_btn > div > button")
                ActionChains(driver).click(qrfb).perform()
                #ActionChains(driver).click(qrfb).perform()
                time.sleep(1)
                print('发表成功')
                break
            except Exception as e:
                print('fail')

#传入某个作者的cook名，然后执行十次发布！
def userfb(cookpath):
    global anum
    art_abspath = os.path.abspath(article_path)
    set_cookie(cookpath)
    driver.maximize_window()
    i=0
    while i<10:
        try:
            time.sleep(1)
            driver.get(url='https://mp.dayu.com/dashboard/article/write')  # 至此已经登录到了本账号的发表页面,执行十次发布
            article_abspath=os.path.join(art_abspath,article_list[anum])#某文章的绝对路径
            sc_word(article_abspath)
            i+=1
            anum+=1
        except:
            1

if __name__ == '__main__':
    cook_abspath = os.path.abspath(cookies_path)
    for cok_list in cook_list:
        cookies_abspath=os.path.join(cook_abspath,cok_list)
        print(cookies_abspath)
        userfb(cookies_abspath)