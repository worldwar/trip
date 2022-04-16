#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import random

from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素

driver=webdriver.Chrome()

# 解析出每个城市及其该城市对应的url
def parse_city(url):
    print(url)
    html = requests.get(url,headers=headers)
    html = html.text
    #print(html)
    soup = BeautifulSoup(html,'html.parser')
    city = soup.find_all('ul',{'class':'mp-sidebar-list','mp-role':'hotCityList'})[0].find_all('li')
    for i in city:
        # 得到每个城市的名字和对应的url
        city_name = i.a.text
        city_url = i.a['href']
        city_url='http://piao.qunar.com'+city_url
        print(city_url)
        city_page(city_name,city_url)
        #if city_name == "北京":
        #    continue
        time.sleep(random.randint(5,10))

# 解析出每个城市的url的下一页
def city_page(city_name,city_url):
    html = requests.get(city_url,headers=headers)
    print(city_url)
    html = html.text
    print(html)
    soup = BeautifulSoup(html,'html.parser')
    page = soup.find_all('div',{'class':'pager'})[0].find_all('a')
    # 得到a标签中的href
    page_url = page[0]['href']
    # 得到下一页的url，这个url由我们来指定，只需把页数前面的字符串匹配出来即可
    page_select_url = re.findall('(.*page=)',page_url)[0]
    # 将完整的页数的url拼接起来
    page_select_url = 'http://piao.qunar.com'+page_select_url
    # 这里选-2是有深意的，因为在选择每一页的地方倒一是下一页，而倒二则是尾页数
    page_num = int(page[-2].text)
    print('有%s页的数据'%page_num)
    for i in range(1,page_num+1):
        #if city_name == "北京" or (i < 79 and city_name == "上海"):
        #   continue
        # 遍历得到某个城市中所有页数
        print('第%d页信息'%i)
        parse_page_url = page_select_url+str(i)
        print('网页地址：',parse_page_url)
        # 将每一页的url都传递到parse_page中进行解析
        time.sleep(random.randint(2,5))
        parse_page(city_name,parse_page_url)


def parse_jd_detail(city_name, jd_url):
    html = requests.get(jd_url, headers=headers)
    time.sleep(5)
    html = html.text
    #print(html)
    print(jd_url)
    soup = BeautifulSoup(html,'html.parser')
    # mark count 可以获取 评分分差评 中评 好评使用soap暂时无法获取
    #jd_comments_mark = soup.find_all('div',{'class':'mp-comments-score'})[0].find_all('span',{"class":'mp-gain-score'})[0].text
    #jd_comments_cout = soup.find_all('div',{'class':'mp-comments-number'})[0].find_all('span',{"id":'commentsTotalNum'})[0].text
    #jd_comments_low = soup.find_all("ul",{'id':'tagList'})[0].find_all('li',{'class':'mp-commentstab-item','mp-role':'tagItem', 'data-type':'3'})[0].text
    jd_comments_mid = soup.find_all('div',{'class':'mp-comments'})[0].find_all("ul",{'id':'tagList'})[0].find_all('li',{'class':'mp-commentstab-item','mp-role':'tagItem','data-type':'2'})[0].text
    jd_comments_high = soup.find_all('div',{'class':'mp-comments'})[0].find_all("ul",{'id':'tagList'})[0].find_all('li',{'class':'mp-commentstab-item','mp-role':'tagItem','data-type':'1'})[0].text
    jd_detail = jd_comments_mark+"|"+jd_comments_cout+"|"+jd_comments_low+"|"+jd_comments_mid+"|"+jd_comments_high

    print(jd_detail)

# 解析每个城市每一页的信息
def parse_page(city_name,parse_page_url):
    html = requests.get(parse_page_url,headers=headers)
    html = html.text
    soup = BeautifulSoup(html,'html.parser')
    jingdian = soup.find_all('div',{'class':'result_list','id':'search-list'})[0].find_all('div',{'class':'sight_item'})
    for c in jingdian:
        # 景点名
        jd_name = c.find_all('a',{'data-click-type':'l_title','class':'name'})[0].text
        jd_url = c.find_all('h3',{'class':'sight_item_caption'})[0].find_all('a')[0]['href']
        ###景点详细页面，暂未成功获取信息
        print("*"*40)
        print(jd_url)
        jd_url = "http://piao.qunar.com"+jd_url+"#mp-comments"
        jd_detail = parse_jd_detail(city_name, jd_url)
        print("*"*40)
        raise
        # 景点级别，有的景区无级别，所以要设置一个异常
        try:
            jd_jb = c.find_all('span',{'class':'level'})[0].text
        except:
            jd_jb='普通景区'

        jd_score = c.find_all('span',{'class':'product_star_level'})[0].find_all('em')[0].find_all('span')[0].text
        print(jd_score)
        jd_score = float(jd_score.split(" ")[1])
        print(jd_score)
        # text得到的是  地址：北京市东城区景山前街4号  这种格式，所以以空格拆分，取后面那个
        jd_address = c.find_all('p',{'class':{'address','color999'}})[0].text.split()[-1]
        # 景点介绍
        jd_jieshao = c.find_all('div',{'class':{'intro','color999'}})[0].text
        # 景点价格，有的是免费，并无价格这一参数，所以设置一个异常
        try:
            jd_price = c.find_all('span',{'class':'sight_item_price'})[0].find_all('em')[0].text
        except:
            jd_price=0
        # 有的是免费，并销量这一参数，所以设置一个异常
        try:
            jd_xiaoliang = c.find_all('span',{'class':'hot_num'})[0].text
            # 景点销量
            jd_xiaoliang=int(jd_xiaoliang)
        except:
            jd_xiaoliang=0
        print('{0}  {1}  {2}  {3}  {4} {5} {6}'.format(jd_name,jd_jb,jd_jieshao,jd_price,jd_xiaoliang, jd_address, jd_score))
        save2file(city_name,jd_name,jd_jb,jd_jieshao,jd_price,jd_xiaoliang, jd_address, jd_score,jd_detail)
        time.sleep(random.randint(1,1))

def save2file(city_name, jd_name, jd_jb, jd_jieshao, jd_price, jd_xiaoliang, jd_address, jd_score, jd_detail):
    with open("./data/{}.txt".format(city_name),"a+",encoding='utf-8') as f:
        try:
            f.write('''{}|{}|{}|{}|{}|{}|{}|{}\n'''.format(jd_name, jd_jb, jd_jieshao, jd_price, jd_xiaoliang, jd_address,jd_score,jd_detail))
        except:
            with open("./data/{}错误.txt".format(city_name),"a+",encoding='utf-8') as err_file:
                err_file.write("{}\n".format(jd_name))


if __name__ == "__main__":
    headers = {
        #"Cookie":'''SECKEY_ABVK=G61YYyZlIqKHkdhDDHY/U6cQFUKU9IelP487TOu+a/k=; BMAP_SECKEY=DzMQGTx1qy6ZYEhLiR_hzmJjOXA0f2GhNjF9mEe-5Evo3ERj3eWyWuchECLxOEEwaID8cEWnstEbYldocvLeRTOfwYxq0gBKhd1X6Tz-Eo2h9hhWQkb5aIdg5MOgPIToFsCbo0odnihzXSQz8cKfpg3j4Yj3PzisnsB-lEorIeJAv4LuwYTk7A9eMrFmVXKM; QN1=00009100306c4007d5986b16; QN300=s=baidu; QN99=6786; QunarGlobal=10.66.84.45_-2473e4f5_17ff2c57319_-2515|1649046707787; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; QN205=s=baidu; QN277=s=baidu; csrfToken=cQIzm2Mty6mN2YSq4XCx1nmLa4jEQgGg; QN601=676a7d59c7c3d284b4eaa165843bdb3d; _i=DFiEuYd2-BtlLHCw-c4JbJ_6tfyw; QN48=tc_66114f5204b728e7_17ff2d7e02d_3c3e; QN163=0; QN269=2419C1C0B3D011EC8DADFA163E52BE3B; fid=41fb5abf-2ee9-47bf-8c7b-823f67cd2a4a; activityClose=1; QN243=17; QN71="MTE0LjIxOS45My44Njroi4/lt546MQ=="; ariaDefaultTheme=null; QN57=16490468175360.1904194863208848; Hm_lvt_15577700f8ecddb1a927813c81166ade=1649046818; QN67=2267; _vi=hAueQSGcGQgre2eLV_CGPLosmZ66VdsJ0NkcVfupyI29pOMiL3nJ8rJCpPv5z5RgatC31l__CbIVoq_b-KU1gbAIeuUp4elSoV1T7IPXYr1WijUkAx1D-ENVfnbco2akZQYG98tl1mn6y4b9ynw2jkU6a1o2vQonuQDDRmBDG8GG; QN267=17005624067a2acc15; QN58=1649059120203|1649059359323|2; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1649059360; QN271=c38ffb8c-70b0-4ebc-ad0d-d99a9132631e; JSESSIONID=C3910E0190BA22A919963952F5FF0A4C; __qt=v1|VTJGc2RHVmtYMTlGbDY3Zm5tNkdZekZyOTdtTXE4NEs2NVQxQ2JEVFZDSmxZU0t4K3Y2N0pZMUFwODNqcEdBZVlwSjZQRS9jMFl4Q3B6cDhXbkg5QWk0WUVBR0owS0lyUEhtc0JxUEorYXZibHZMK2RVVGt0dVdHa2ZLQ3ByR05GaklGS01QdDdaTmNtUjlqbExvbVhhMkFWTDZVOTEvMm9DRHJ0ZFZoYlkwPQ==|1649059492180|VTJGc2RHVmtYMTlDUGpjeXJPQjZXdXp5enh1R3VTZ0lYSTN1a2IrK3FuaXF4R3BXVVRxamdVYkFiUDk0YWxoZE9zV09ycFo4TlUya09oNnBsYUYzbkE9PQ==|VTJGc2RHVmtYMTgwM2FMallHNVJTRlVkb05JMU42cHYxVGNPV0JXV29xb0g1TkpScURaVVYwZGMzRzFhbDg4MGZaeEtGaHNLT0pyRUxHYnhKRURrWmRmbzYwMTVXbE94c1ZOS3RIRGhONXRsNHFta2dXL2wreURzcFdQWW10NWsrWkRPUkUzZVRtSUsxN2IyMTRmaXVKdld6dmJqV3pEbnlTQndCQ0ljWHc0b1g0Z2luR1haSFlMUzFSUmFxT1BrUVArR00yOTB0bGozb1oxbzRyR2pkR1Z5RDM3MjR3dDlqbndrSW1PZUJQUUZRWVZsb1I5YnRlUnd6bkJ3T0pVeFRIN05yMys2MU1XTC9mcmxUakI2MUg2VWt0SlFGL0RxdUg1bUZMTVNOemlXbFlnREN5N2tZVVM5Q3VodDlmaHlldlhONlVVSFRZYjdTK3QrdmJKMzJjV3ZjeEdyelNxcmp2WmhBUFI1SVZheTFKbWRSL3UzQVRiaGhEam13OXRQMGdwVGZZSWx0Ui9MbEhYdTUvMWVheDNSZ2dmZnBwajQzbENqajhJUmRIeEFpTXMrT3JBbllReldveEVrYWpabkhHMW9qZC9vd1dCMHltNlNneHo0YS9ueGQ0OFU2M2t3b2xFNmxZcHQyNE9IRnUydlcyUlR4ZmRITTZJRjViRms0clVEcW9GSHhBbGJwemZjZ3paUVdYVXUzUUZvNkhyK3hvUHBkZnpxTFVTTStlT0xBdjdxMzQ3MjJJSmZjOUFLYXdrR2UwR1hUT0x4cE5mK1RSNFBWa2FiNFBsclFYSXVDTThVcVpzd3lldkxBdnNkbVNOU1VMSlhPUzN2OWcyWjdFM0VJTHpPZmVpcXJMekZHM1ZMQTZPTU05UnYxaDl2TStiNDNTRGtlWlE9''',
        "Cookie": '''QN1=00009100306c4007d5986b16; QN300=s=baidu; QN99=6786; QunarGlobal=10.66.84.45_-2473e4f5_17ff2c57319_-2515|1649046707787; QN205=s=baidu; QN277=s=baidu; QN601=676a7d59c7c3d284b4eaa165843bdb3d; _i=DFiEuYd2-BtlLHCw-c4JbJ_6tfyw; QN48=tc_66114f5204b728e7_17ff2d7e02d_3c3e; QN269=2419C1C0B3D011EC8DADFA163E52BE3B; fid=41fb5abf-2ee9-47bf-8c7b-823f67cd2a4a; QN243=17; QN71="MTE0LjIxOS45My44Njroi4/lt546MQ=="; ariaDefaultTheme=null; QN57=16490468175360.1904194863208848; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; csrfToken=LyD4iyJjHw3nH3XZokzrxBpJaibqputP; _vi=8cnEo4SQpZh2jkvha2W5jEciKYSc7ZUbvW7NrzNj3n2UxtiFRz7kh5wuhZrJ-VXgzEo69S63v42SOCbqcEvPUJBuqpo3qtDJPs3El36QahikPlw2ydvWLso9-xsDgMnO5g2YgxJuMnd7YcvwxYzVr0duMMpqKO3qNe2PcsBgGeEE; QN163=0; Hm_lvt_15577700f8ecddb1a927813c81166ade=1649046818,1649245436; QN67=2267,202021,14454,15477,10265; QN58=1649245435254|1649245442244|3; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1649245442; QN271=5439e1e8-5950-4b7a-b19b-b84098a2acc5; JSESSIONID=E92FC800F4813E3697FA012CC6C69F8D; QN267=170056240616c0a2a1; __qt=v1|VTJGc2RHVmtYMTlGUEVjRnF2WHN5OWd5RjVRWDJqVjBydWRnbFczaUZzeGpQb0JpeXZtbFViMm83SkRibGVQRE5BQXVWRmpuRWpDSjI0ck9SYjhWbkVndWdiTDE0amdVcnhoQjJOaGVla1ZaTElrZVJBRmJ4QWgyUFBnNi8rekI4YXR2cmkzNkd5MEk3cURSMnVLL2hSaFhwZHBjZnJ6ZlZwT2tjbmVjREp3PQ==|1649245552485|VTJGc2RHVmtYMStqeG1wc1JjUmFIRWRRLytvWHlJbGVqNWEwYWt2QnlrVEU3cW5lcUJjbHNhTUFOVkRPQWVZdkUySS9MN3Iyc2xBelg5L0RsS1ZTL3c9PQ==|VTJGc2RHVmtYMTlscmpXTlV5Vk42MFZCdnBzRXZ6Mlc5bHhHbEN6d1IrRGMybVBIbk1aMEMvc3FpMDNHclNFYlFWZlUvR01leHVqbFQ1WmxVR2JUWVcrUW0xNWFMNElOb3dmbzlQQjl2YmJwWGZmV0tiSTFJbDFscytiWUgza1p6WnRPMkhrWHdGK2ZZZ05oTC9kU3NjRzRXZ2luZ3NlNmVHTENkc0JRS29teHg3dyswaTdiWEt3MEo1OG9iMU1aakxxdmdLVVI5bnFtalgvNk8ramw1Sk1EdmJQa09UblJpVDlpS2wwZk9hVmszZWxsOHJxOWVtRjFKMlVPUkJQQnRtWjZpcTFlaGJia0hQVTBRdmJGc2xybFBDQkdwQ0o3VjBubzcrdDhud0xZdkduWExhRjVHUldQRmNxYTJVQnppN1VtRW0rd2FJU2twREdCanp6MVQ5Q3dkaHFIOWRRbEFJQzFCdDl5V2FYS2dKclZVVGZGV1pqckVCV3A2RnRTS0VDeVd0d0Q2V3ROdTVNclU5MDk3YmQ1L2loUm9BTU5iWGMrVGZwL2JNNG1rV0dmY0VQT21pTkdvZXkxWnpuRlQzUjVDRG8vVVk5a1RyNis1ZVFlUEpOWktjdjFRZDloaVZyY1BVeEpKRXVnOGNMSmhzVFVXTkJsRUEwRlA1aFhOc01hMC8vdGZkKzRjL0M4THBNNnNKUEw5MzYxS3lLUGxDV0tydkQ3NmVma0xXUWxxS1VrL2hCeUdTQ3dJV25jNWYzVmN2cGE0QWo3OHdVVml5U1RkNFR1dDFzN0plNG41VHVoMUorZUFyOWIxYkp3eU9hbEE5Nk1FQUkvWlg0b1BORkZWdzhqTXZ2M0g3UzhCaGw1WVVHNkJPWmF1cEo3MUhMNUhxb2JrVXVBakgzNDBCTFptSzlydzFSUkkwWHphbVYvWGxRYXJoRjBMU2hjcEV2Qlc1MnlHTjNlRmc1NnF2R1h2NjhDT2J1ZmVEbWE5dGFWckVVWEU3Z0VFd1p4UHdpemRRUHJDQ09pSy85dzB6WURjbkpoL1NnRENMamprOTBTdEJOYks2YVppMGNqemtIcGxNQVhWaXNEb1JkNA==''',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36", }
    start_url='http://piao.qunar.com/'
    parse_city(start_url)
    #save2file("aa","bb","cc","dd","ee","ff","gg")
