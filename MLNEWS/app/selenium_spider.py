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

#driver=webdriver.Chrome()
#global driver

def parse_hot_city():
    try:
        wait=WebDriverWait(driver,10)
        #访问景点首页
        driver.get('http://piao.qunar.com/')
        cookies_string = '''QN1=00008c80306c402788e0c8ce; QN300=organic; QN99=499; QunarGlobal=10.66.84.45_-2473e4f5_180023e513a_-fcc|1649306398046; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN205=organic; QN277=organic; csrfToken=L1NgJDRRUiWg6zxyLB2MHh5KNJz6x5ar; QN601=1108ee87545940274e506867115fcfe8; _i=RBTjekXhFSmISApTUxViu35MSCTx; QN163=0; QN269=C7FC26D0B62C11EC9D24FA163E7D47C7; QN48=c2a5fc74-3034-43c8-b581-4c525c6ef470; fid=74fb80aa-97a4-449b-bf3b-b7f0071c88c1; QN267=099227585633d2e259; _vi=VJVDID2UsWlURHuloIbFkSi26fRWv0S-QvXuIikKoM2eM1vAjAsKRiJVGN5Exxz0URs10BZtiRkxzVqoHxdFp-NIqc42QwuNopEEZtNP6ds5R38iC9jbn3MilV9eABGbFznU5dif7WPLUQZQpzO5Dx6K6ZgjN_w1Vv8p4U_oz1S1; ariaDefaultTheme=undefined; QN271=8703aee5-52a4-4581-8196-e390c4094aad'''

        from http.cookies import SimpleCookie
        cookie = SimpleCookie()
        cookie.load(cookies_string)
        for key, morsel in cookie.items():
            driver.add_cookie({"name":key, "value":morsel.value})


        uls = driver.find_element(by=By.XPATH, value="//ul[@mp-role='hotCityList']")
        #lis = uls.find_element(by=By.XPATH, value="li")
        lis = uls.find_elements_by_css_selector('li a')
        #lis = uls.find_elements_by_tag_name("li")
        #获取景点主页标签句柄
        main_windows = driver.current_window_handle
        print(main_windows)
        #对每一个热门城市进行访问
        for li in lis[13:]:
            #driver.switch_to.window(main_windows)
            #逐个热门城市点击
            driver.execute_script("arguments[0].click();",li)
            #li.click()
            #点击后在新标签页打开页面，需要获取当前所有标签页句柄
            handle_all = driver.window_handles
            #切换至当前新打开的标签页
            driver.switch_to.window(handle_all[1])
            #print(now_windows)
            ##获取下一页的链接
            search_list_jd_counts = 0
            time.sleep(5)
            for j in range(30):
                js = 'window.scrollTo(0,1000)'
                driver.execute_script(js)
                time.sleep(0.5)
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'pager-container')))
            MoveElement = driver.find_element_by_xpath('//*[@id="pager-container"]')
            Action = ActionChains(driver)
            Action.move_to_element(MoveElement).perform()
            pages = driver.find_element(by=By.XPATH, value="//div[@id='pager-container']")
            jd_counts = int(pages.get_attribute("data-total-count"))
            page_links = pages.find_elements_by_css_selector('a')
            page_now = pages.find_elements_by_css_selector('em')
            page_size = jd_counts // 15
            for click_count in range(page_size):
                #处理每一个搜索景点列表信息
                jd_ids = parse_search_page()
                #处理每个景点详情页面信息
                parse_page_jd(jd_ids)
            time.sleep(10)
            driver.close()
            #time.sleep(10)
            driver.switch_to.window(main_windows)
            #print(li.get_attribute("href"))

        time.sleep(10)

    finally:
        driver.close()

def parse_page_jd(jd_ids):
    #print(jd_ids)
    #for jd in jd_ids:
    #    jd_name = jd.get_attribute('title')
    #    print(jd_name)
    #return 
    for jd in jd_ids:
        jd_name = jd.get_attribute('title')
        jd_url = jd.get_attribute('href')
        print("jd url {} {}".format(jd_name, jd_url))
        #点击景点详细页面
        driver.execute_script("arguments[0].click();",jd)
        #点击后在新标签页打开页面，需要获取当前所有标签页句柄
        handle_all = driver.window_handles
        print(handle_all)
        #切换至当前新打开的标签页
        driver.switch_to.window(handle_all[2])
        #to do
        #driver.find_element(by=By.XPATH, value="//ul[@id='tagList']")
        #获取当前景点详细信息
        time.sleep(2)
        ##模拟鼠标向下滚动
        for j in range(20):
            js = 'window.scrollTo(0,500)'
            driver.execute_script(js)
            time.sleep(0.2)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'tagList')))
        MoveElement = driver.find_element_by_xpath('//*[@id="tagList"]')
        Action = ActionChains(driver)
        Action.move_to_element(MoveElement).perform()
        time.sleep(5)
        #WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'tagList')))

        ##页面加载完成，在此页面获取相关元素
        comments = driver.find_element(by=By.XPATH, value="//ul[@id='tagList']")
        comment_mark = "无评分"
        comment_marks = driver.find_element(by=By.XPATH, value="//span[@id='gainScore']")
        if comment_marks:
            print("**********************")
            try:
                comment_mark = comment_marks.text
            except Exception as e:
                print(e)
                

        #comment_mark = comment_marks.find_elements_by_css_selector('span')
        comment_lis = comments.find_elements_by_css_selector('li')
        jd_comments_high = jd_comments_mid = jd_comments_low = jd_comments_all = 0
        for comment in comment_lis:
            if comment.get_attribute("data-type") == "0":
                jd_comments_all = comment.text
            elif comment.get_attribute("data-type") == "1":
                jd_comments_high = comment.text
            elif comment.get_attribute("data-type") == "2":
                jd_comments_mid = comment.text
            elif comment.get_attribute("data-type") == "3":
                jd_comments_low = comment.text
        print(jd_name,jd_comments_high,jd_comments_mid,jd_comments_low,jd_comments_all,comment_mark)
        save_data(jd_name,jd_comments_high,jd_comments_mid,jd_comments_low,jd_comments_all,comment_mark)

        time.sleep(2)
        #关闭景点详细页面标签页
        print("关闭{}景点详细页面".format(jd_name))
        driver.close()
        #time.sleep(10)

        #切换回搜索页面
        driver.switch_to.window(handle_all[1])

def parse_search_page():
    #driver.refresh()
    time.sleep(2)
    for j in range(30):
        js = 'window.scrollTo(0,1000)'
        driver.execute_script(js)
        time.sleep(0.5)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'pager-container')))
    MoveElement = driver.find_element_by_xpath('//*[@id="pager-container"]')
    Action = ActionChains(driver)
    Action.move_to_element(MoveElement).perform()
    time.sleep(3)
    pages = driver.find_element(by=By.XPATH, value="//div[@id='pager-container']")
    jd_counts = int(pages.get_attribute("data-total-count"))
    page_links = pages.find_elements_by_css_selector('a')
    #page_now = pages.find_elements_by_css_selector('em')
    if page_links[-1].text == "下一页":
        driver.execute_script("arguments[0].click();",page_links[-1])
        time.sleep(10)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'pager-container')))
        MoveElement = driver.find_element_by_xpath('//*[@id="pager-container"]')
        Action = ActionChains(driver)
        Action.move_to_element(MoveElement).perform()
    #获取当前城市搜索页面信息
        jd_info = driver.find_element(by=By.XPATH, value="//div[@id='search-list']")
    #获取当前城市搜索信息的所有景点的超链接信息，用户后续获取景点详细信息
        jd_ids = jd_info.find_elements_by_css_selector('.sight_item_show a')
        for jd in jd_ids:
            print(jd.get_attribute("title"))
    else:
        jd_ids = []
    return jd_ids

def save_data(jd_name,jd_comments_high,jd_comments_mid,jd_comments_low,jd_comments_all, comment_mark):
    with open("./comments6.txt","a+",encoding='utf-8') as f:
        try:
            f.write('''{}|{}|{}|{}|{}|{}\n'''.format(jd_name,jd_comments_high,jd_comments_mid,jd_comments_low,jd_comments_all,comment_mark))
        except Exception as e:
            with open("./comments错误.txt","a+",encoding='utf-8') as err_file:
                err_file.write("{}====>{}\n".format(jd_name,e))    

if __name__ == "__main__":
    global driver
    driver=webdriver.Chrome()
    parse_hot_city()