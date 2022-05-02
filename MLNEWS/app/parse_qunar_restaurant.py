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
def parse_restaurant():
    try:
        # driver.get('https://travel.qunar.com/p-cs299914-beijing-meishi?page=1&sort=12') #北京
        # driver.get('http://travel.qunar.com/p-cs299878-shanghai-meishi?page=1&sort=12') #上海
        # driver.get('http://travel.qunar.com/p-cs300085-chengdu-meishi?page=1&sort=12') #成都
        # driver.get('http://travel.qunar.com/p-cs300188-sanya-meishi?page=1&sort=12') #三亚
        # driver.get('http://travel.qunar.com/p-cs300132-guangzhou-meishi?page=1&sort=12') #广州
        # driver.get('http://travel.qunar.com/p-cs299979-chongqing-meishi?page=1&sort=12') #重庆
        driver.get('http://travel.qunar.com/p-cs300118-shenzhen-meishi?page=1&sort=12') #深圳

        # driver.get('http://travel.qunar.com/p-cs300100-xian-meishi?page=1&sort=12') #西安
        # driver.get('http://travel.qunar.com/p-cs300195-hangzhou-meishi?page=1&sort=12') #杭州
        # driver.get('http://travel.qunar.com/p-cs299782-xiamen-meishi?page=1&sort=12') #厦门
        # driver.get('http://travel.qunar.com/p-cs300133-wuhan-meishi?page=1&sort=12') #武汉
        # driver.get('http://travel.qunar.com/p-cs300134-dalian-meishi?page=1&sort=12') #大连
        # driver.get('http://travel.qunar.com/p-cs299937-suzhou-meishi?page=1&sort=12') #苏州
        # driver.get('http://travel.qunar.com/p-cs299783-qingdao-meishi?page=1&sort=12') #青岛
        #

        cookies_string = '''QN1=00008c80306c402788e0c8ce; QN300=organic; QN99=499; QunarGlobal=10.66.84.45_-2473e4f5_180023e513a_-fcc|1649306398046; QN601=1108ee87545940274e506867115fcfe8; _i=RBTjekXhFSmISApTUxViu35MSCTx; QN269=C7FC26D0B62C11EC9D24FA163E7D47C7; QN48=c2a5fc74-3034-43c8-b581-4c525c6ef470; fid=74fb80aa-97a4-449b-bf3b-b7f0071c88c1; QN205=organic; QN277=organic; HN1=v154f5e7300cdb3c89e8af7ca872901340; HN2=qurlsuqqnlluk; ariaDefaultTheme=null; ctt_june=1644991819166##iK3wVKt%3DWwPwawPwasv%2BWPiDWsDAWSEhW2EhWRTIVDP8aK2wWDjnaSoDEKkDiK3siK3saKjAaKDAaS2%3DWst8VuPwaUvt; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=N8Xheo8mrcKCEzTmP5NTvi4fN4bcVNcQ; QN163=0; activityClose=1; QN243=3; ctf_june=1644991819166##iK3waSaOWhPwawPwasiIWsWDaSgwaKg%3DaKkDED3AXPjnWs3nEDP8WPP%3DX%3DXsiK3siK3saKjAaKamWKtwWRvsawPwaUvt; cs_june=cdc0d3cfef4ecef746275d9f8525b42e131b75dc7aecf78ea0fc11d94c3ad047744a7fd546846604ce41645159f9d951bdb3ef441c1775a157bd0e2a6200a386b17c80df7eee7c02a9c1a6a5b97c117928619726d84c236143eaac204dd6f39c5a737ae180251ef5be23400b098dd8ca; Hm_lvt_c56a2b5278263aa647778d304009eafc=1651386268; viewpoi=3564514|27337781|3567196|3190493; viewdist=299914-16; uld=1-299914-21-1651392384; JSESSIONID=D3723382DA98AB464C3DC6BBCF858B68; QN267=09922758569c945664; _vi=x0nfIUkkYYUzOnZFnguHNHjDnSGihVQWbusrWBmv5lPCGdNdZsV65Hesd9iVmvwf5dc_HDSrLMAzH9hdEEvDORD0ZvmC5YR_MBlhkN3Z6QIM3My_CINCEFZlqVb7MLTdUM_LTjB5Y1mYm6h9MV6fB1z9lvEdl7xETe89u6IWcJvw; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1651392386; QN271=fd043244-c7e8-44ef-8582-97920f0624cf; SECKEY_ABVK=fVXktUZrSNTMHsMsmsiY5YFd+uyDja5ZHZJtQQLXjxk%3D; BMAP_SECKEY=_OlMnFhef_6ED9Kss5vfLsxTxvgo85uMMaXnSMVP3tRZJOf5TFU7gj36UC36T82NLzmzfdW84AMnW9svuXCeJ3ZMpuBmOX2_R1su5zLSTQDDMrYXYc90OGKOjcVkIhSreTqSijJNfhJ8mV6wXnw_uY3stzTIU756fwFE924r41TkuxWZoz3-W0CEvrTCrxpE'''
        cookie = SimpleCookie()
        cookie.load(cookies_string)
        for key, morsel in cookie.items():
            driver.add_cookie({"name": key, "value": morsel.value})

        # button = driver.find_element_by_link_text('酒店')
        # button.click()
        # time.sleep(1)
        # input = driver.find_element_by_class_name("inputText")
        # input.clear()
        # input.send_keys("上海")
        # time.sleep(2)
        # day1 = datetime.date(2022, 5, 1)
        # print(day1)
        # input = driver.find_elements_by_xpath("//div[@class='live clearfix input_container']//input[@tabindex='0']")
        # print(input)
        # checkIn = driver.find_element_by_xpath(
        #     "//div[@class='live clearfix input_container']//input[@class='inputText date']")
        # checkIn.clear()
        # checkIn.send_keys(str(day1))
        # time.sleep(5)
        # day2 = datetime.date(2022, 5, 5)
        # input[1].clear()
        # input[1].send_keys(str(day2))
        # time.sleep(1)

        # input = driver.find_element_by_class_name('main')
        #
        # input.click()
        #
        # time.sleep(1)

        # wait=WebDriverWait(driver,10)
        #访问景点首页
        # driver.get('http://hotel.qunar.com/cn/chongqing_city?fromDate=2022-04-28&toDate=2022-04-29&cityName=%E9%87%8D%E5%BA%86')

        # time.sleep(2)
        # js = 'window.scrollTo(0,400)'
        # driver.execute_script(js)
        time.sleep(2)



        city = driver.find_element(by=By.XPATH, value="//div[@class='city_name clrfix']/span/h1").text

        has_next = True

        while has_next:
            time.sleep(3)
            links = driver.find_elements(by=By.XPATH, value="//div[@class='b_food_new']//ul[@class='list_item clrfix']//li/a")
            # links = driver.find_element_by_class_name('hotel-card-detail-btn')
            # links.click()

            main_windows = driver.current_window_handle
            print(main_windows)
            has_next = parse_page(city, links)

    finally:
        driver.close()

def parse_page(city, links):
    for li in links:
        parse_one(city, li)
    time.sleep(10)
    next = driver.find_elements(by=By.XPATH, value="//a[@class='page next']")
    if len(next) == 0:
        return False
    else:
        next[0].click()
        return True

def parse_one(city, li):
    li.click()
    # driver.execute_script("arguments[0].click();",li)
    time.sleep(5)
    handle_all = driver.window_handles
    driver.switch_to.window(handle_all[1])
    time.sleep(5)
    restaurant_name = driver.find_element(by=By.XPATH, value="//div[@class='b_title clrfix']/h1").text
    addr = driver.find_elements(by=By.XPATH, value="//td[@class='td_l']/dl/dd/span")
    if len(addr) == 0:
        addr = ''
    else:
        addr = addr[0].text

    desc = driver.find_elements(by=By.XPATH, value="//div[@class='b_detail_section b_detail_summary']/div/p")
    if len(desc) == 0:
        desc = ''
    else:
        desc = desc[0].text
    comment_count = driver.find_element(by=By.XPATH, value="//span[@class='e_nav_comet_num']").text
    score = driver.find_element(by=By.XPATH, value="//div[@class='scorebox clrfix']/span[@class='cur_score']").text
    save_restaurant(restaurant_name=restaurant_name, city=city, addr=addr, desc=desc, score_count=comment_count,
                    score=score)
    driver.close()
    driver.switch_to.window(handle_all[0])


def save_restaurant(restaurant_name, city, addr, desc, score_count, score):
    with open("./restaurant7.txt","a+",encoding='utf-8') as f:
        try:
            f.write('''{}|{}|{}|{}|{}|{}\n'''.format(restaurant_name,city,addr,desc,score_count,score))
        except Exception as e:
            with open("./comments错误.txt","a+",encoding='utf-8') as err_file:
                err_file.write("{}====>{}\n".format(restaurant_name,e))

if __name__ == "__main__":
    global driver
    driver=webdriver.Chrome()
    parse_restaurant()