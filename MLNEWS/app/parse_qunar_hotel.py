#!/usr/bin/env python
# -*- coding: utf8 -*-
from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.action_chains import ActionChains
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
import time


from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import time

import datetime

from urllib.request import urlopen

from urllib.error import HTTPError

from urllib.error import URLError

from bs4 import BeautifulSoup

from http.cookies import SimpleCookie
def parse_hotel():
    try:
        driver.get('https://www.qunar.com/')
        cookies_string = '''QN1=00008c80306c402788e0c8ce; QN300=organic; QN99=499; QunarGlobal=10.66.84.45_-2473e4f5_180023e513a_-fcc|1649306398046; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=L1NgJDRRUiWg6zxyLB2MHh5KNJz6x5ar; QN601=1108ee87545940274e506867115fcfe8; _i=RBTjekXhFSmISApTUxViu35MSCTx; QN163=0; QN269=C7FC26D0B62C11EC9D24FA163E7D47C7; QN48=c2a5fc74-3034-43c8-b581-4c525c6ef470; fid=74fb80aa-97a4-449b-bf3b-b7f0071c88c1; QN205=organic; QN277=organic; HN1=v154f5e7300cdb3c89e8af7ca872901340; HN2=qurlsuqqnlluk; ariaDefaultTheme=null; ctt_june=1644991819166##iK3wVKt%3DWwPwawPwasv%2BWPiDWsDAWSEhW2EhWRTIVDP8aK2wWDjnaSoDEKkDiK3siK3saKjAaKDAaS2%3DWst8VuPwaUvt; _vi=nZ5eZVFDZRYpWGUsMbrf4S2_c5iaR8Gyigi4T6ti8SEPFsA9Q22cB-fa2uXQT5NAfhljC2I2e-2ECx5oKxIjZs2xAo3lXDXHE_pfu58UrAd64ZzFWJO-uKgO0avB5VZxHgEaZFFNvQdbhRCxOXWbhrttf9RGj2gXYOtQqzEupnQi; QN267=0992275856c48533bf; ctf_june=1644991819166##iK3waKvAWUPwawPwasPOa2aOEKt8aRGhVD38X2D%2BXSgnWPD%2Ba%3DGTEK2sWsv%3DiK3siK3saKjAaK3NWsDNaRDnaUPwaUvt; cs_june=61b18a10d688b7b352227af8b861d842c72bb09e8616d573d8bd2d439d2b61f8744a7fd546846604ce41645159f9d951bdb3ef441c1775a157bd0e2a6200a386b17c80df7eee7c02a9c1a6a5b97c1179b844a9dda762285d8d79646d0ffd09485a737ae180251ef5be23400b098dd8ca; QN271=f8ad407e-a767-4844-b092-b7b5db89e068'''
        cookie = SimpleCookie()
        cookie.load(cookies_string)
        for key, morsel in cookie.items():
            driver.add_cookie({"name": key, "value": morsel.value})

        button = driver.find_element_by_link_text('酒店')
        button.click()
        time.sleep(1)
        input = driver.find_element_by_class_name("inputText")
        input.clear()
        input.send_keys("上海")
        time.sleep(2)
        day1 = datetime.date(2022, 5, 1)
        print(day1)
        input = driver.find_elements_by_xpath("//div[@class='live clearfix input_container']//input[@tabindex='0']")
        print(input)
        checkIn = driver.find_element_by_xpath(
            "//div[@class='live clearfix input_container']//input[@class='inputText date']")
        checkIn.clear()
        checkIn.send_keys(str(day1))
        time.sleep(5)
        day2 = datetime.date(2022, 5, 5)
        input[1].clear()
        input[1].send_keys(str(day2))
        time.sleep(1)

        input = driver.find_element_by_class_name('main')

        input.click()

        time.sleep(1)

        # wait=WebDriverWait(driver,10)
        #访问景点首页
        # driver.get('http://hotel.qunar.com/cn/chongqing_city?fromDate=2022-04-28&toDate=2022-04-29&cityName=%E9%87%8D%E5%BA%86')

        time.sleep(2)
        # js = 'window.scrollTo(0,400)'
        # driver.execute_script(js)
        time.sleep(2)
        links = driver.find_elements(by=By.XPATH, value="//a[@class='btn hotel-card-detail-btn ']")
        # links = driver.find_element_by_class_name('hotel-card-detail-btn')
        # links.click()
        time.sleep(3)
        main_windows = driver.current_window_handle
        print(main_windows)
        for li in links:
            li.click()
            # driver.execute_script("arguments[0].click();",li)
            time.sleep(5)
            handle_all = driver.window_handles
            driver.switch_to.window(handle_all[1])
            time.sleep(5)

            score_item = driver.find_elements(by=By.XPATH, value="//div[@class='score_box']//p[@class='score']")
            score = score_item.text

            tabs = driver.find_elements(by=By.XPATH, value="//div[@class='tab_bar']//span[@class='inner']")
            comment_item = tabs[3]


            driver.execute_script("arguments[0].click();",comment_item)
            count_item = driver.find_elements(by=By.XPATH, value="//span[@class='count']")
            score_counts = [i.text[1:-1] for i in count_item]

            hotel_name_element = driver.find_element(by=By.XPATH, value="//div[@class='name_cont']//p[@class='name']")
            hotel_name = hotel_name_element.text
            addr_element = driver.find_element(by=By.XPATH, value="//div[@class='name_cont']//p[@class='addr']")
            addr = addr_element.text
            hotel_type_element = driver.find_element(by=By.XPATH, value="//div[@class='name_cont']//span[@class='type']")
            hotel_type = hotel_type_element.text
            save_hotel(hotel_name=hotel_name, addr=addr, type=hotel_type, score_count=score_counts, score=score)

        time.sleep(10)

    finally:
        driver.close()

def save_hotel(hotel_name, addr, type, score_count, score):
    with open("./hotel1.txt","a+",encoding='utf-8') as f:
        try:
            f.write('''{}|{}|{}|{}|{}|{}|{}\n'''.format(hotel_name,addr,type,score_count[0],score_count[1],score_count[2],score))
        except Exception as e:
            with open("./comments错误.txt","a+",encoding='utf-8') as err_file:
                err_file.write("{}====>{}\n".format(jd_name,e))

if __name__ == "__main__":
    global driver
    driver=webdriver.Chrome()
    parse_hotel()