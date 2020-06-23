#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pickle
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
cookies_path = '.\\cookies\\'
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=option)
wait = WebDriverWait(driver, 10)
driver.get("https://mp.dayu.com/dashboard/article/write")
driver.maximize_window()
#等待五秒钟，进而手动滑动模块
username=input('请输入账号')
password=input('请输入密码')
# 之后填入账号密码
driver.switch_to.frame(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/iframe"))
input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_name"]')))
input.send_keys(username)
input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
input.send_keys(password)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit_btn')))
button.click()
pickle.dump(driver.get_cookies(), open(cookies_path+"%s.pkl"%username, "wb"))



def get_path(distance):
        result = []
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0
        while current < (distance - 10):
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            s = v0 * t + 0.5 * a * t * t
            current += s
            result.append(round(s))
        return result