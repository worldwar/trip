from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import time

import datetime

from urllib.request import urlopen

from urllib.error import HTTPError

from urllib.error import URLError

from bs4 import BeautifulSoup

#import requests
#import numpy as np

import pandas as pd


driver = webdriver.Chrome()

driver.get('https://www.qunar.com/')

# 点击酒店，进入酒店页面

button = driver.find_element_by_link_text('酒店')

button.click()

time.sleep(1)

# 输入目的地上海
#获取城市输入框

input = driver.find_element_by_class_name("inputText")

input.clear()

input.send_keys("上海")

time.sleep(10)

#输入入住时间2022年05月01日

day1 = datetime.date(2022,5,1)
print(day1)
#获取时间搜索输入框
input = driver.find_elements_by_xpath("//div[@class='live clearfix input_container']//input[@tabindex='0']")
print(input)
#获取checkin时间输入框
checkIn = driver.find_element_by_xpath("//div[@class='live clearfix input_container']//input[@class='inputText date']")
#time.sleep(199)

checkIn.clear()
#time.sleep(2)

checkIn.send_keys(str(day1))

time.sleep(5)

#输入离开时间2022年05月05日

day2 = datetime.date(2022,5,5)

#input[] = driver.find_element_by_xpath("//input[@tabindex='0']")

input[1].clear()

input[1].send_keys(str(day2))

time.sleep(1)

# 点击搜索按钮

input = driver.find_element_by_class_name('main')

input.click()

time.sleep(1)

#获取此次爬取数据的网页url

html = driver.current_url

#创建三个存放数据的空列表

name = []

allnum = []

alladress = []

allprice = []

try:

    headers = {

        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

        ,'accept-encoding': 'gzip, deflate, br'

        ,'accept-language': 'zh-CN,zh;q=0.9'

        ,'cache-control': 'max-age=0'

        ,'cookie': 'QN1=00009100306c4007d5986b16; QN300=s=baidu; QN99=6786; QunarGlobal=10.66.84.45_-2473e4f5_17ff2c57319_-2515|1649046707787; QN601=676a7d59c7c3d284b4eaa165843bdb3d; _i=DFiEuYd2-BtlLHCw-c4JbJ_6tfyw; QN48=tc_66114f5204b728e7_17ff2d7e02d_3c3e; QN269=2419C1C0B3D011EC8DADFA163E52BE3B; fid=41fb5abf-2ee9-47bf-8c7b-823f67cd2a4a; QN57=16490468175360.1904194863208848; QN58=1649596721907|1649597086298|7; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; QN205=organic; QN277=organic; csrfToken=RV1xDMNR6M39LIQiLXv9i1Jg9BlHxugt; _vi=dS0HFOMNlP-OuweBF4iXMWx0UPt7znoZnDvWLj6BVtJfM9M8H2H1p-uVMRM1cSL3ebG4p_CLkrx8wlfSkjKXSepNAIBP42E8W_734EYJ_ch1-SHioBcMTn3bHQZ-I0q3SJEF4GEjxw1ilHfXUWgq3IyYJuBHCSRyNRpRlVptBMUG; QN163=0; HN1=v123b969b3f56c2940604335cba67eab60; HN2=qurlkusnncunq; ariaDefaultTheme=null; checkInDate=2022-04-30; checkOutDate=2022-05-01; cityUrl=beijing_city; tabIndex=0; cityName=%E5%8C%97%E4%BA%AC; ctt_june=1644991819166##iK3wWs2AaUPwawPwa=DNEKERaREIVRtmERDNXK3mWSfTW=DNVPEhES3mESThiK3siK3saKjAaK3waS2waKDOVuPwaUvt; ctf_june=1644991819166##iK3wVKgsauPwawPwa=EIED3+WS0GWPiTXsfIXsoIXK2saskDX2ETXsDNWPa8iK3siK3saKjAaK3wasvwWKgOauPwaUvt; cs_june=c1bb5f2e42526eea7e1956dd7d5486388144f3e172248f4ff6cf5d9eb4e0f72ecaefce8dbc1eb721dd8129504c87b75b4dd8bfa2169aefc9b241e70a7fa1a268b17c80df7eee7c02a9c1a6a5b97c11794cca31e94c55fac8a10d35e3f4252e875a737ae180251ef5be23400b098dd8ca; QN267=170056240632743411; QN271=ca4c36b5-4cea-453e-b0b0-f10d5c3e6c1d; __qt=v1|VTJGc2RHVmtYMS9QN1p5Vm14U0RPUEZud2JuYlFDdWNZWVJlazVFczVva2NiQkFtY293dXB4ZjdNSGI0VDFNSTBSRk5GaVlYd1Q3ZmUwdW5abmoyYjZ6VHFRU1RlNVIrVk1PY0hSOWptK0cycVZFOTA2K0ROeFVrclpDYmRSRGlPVnp4aEZkbkQ3Z3g4VXZZdjlpOHJ6bG9WSk54TVNBK0VRYm9lVGNtY1Q4PQ==|1651223425847|VTJGc2RHVmtYMSt0SFJVZ3VVSEs4SFNaRFluYWJhckc3dWg2TWhRekdBSVJ0UVVTdXNlaVRnMm1oTEUvK3psUnVQNWR0WjNobDUwakZJOUdoOXZMamc9PQ==|VTJGc2RHVmtYMTg3dUxDbXp4b2hoY1dNQ2dOdURFdTlFbnJvcFFmMTkxOVVKcUgvY3lhWGxBLzJZWmlMVXVadTR4Q1EvN25GbjRsN1FxTEI3SWV1UVlENmxmNTZLeUQ5TklKQWVXOGFGSWZVZnRFc3JUWVdzZHRrb0NZMkxqZERKMms4M2FaY1BUM0NvbmhScXRWZ3RNVHNRSndURnVrSEhXMHprRUxRc0Zsc1U2Y2ZOSmVHdk9vZFF5cHN3eDc0R2M5QVNjVk9OKzcxZ2E1SHZCOERQa3lzRUZqMFdkcVF2SmJPM2VUM0NhU3NOc2tyZXR1ODF5NFJrckJVYVdMRXI0R1hmVkZTaGk4eGxkc2xTclRTYU9CdVg4YXkyajRKa2cwYTdWdVJSc05JNHV4YmtEUWJMcWJGWWl6WWRVL3M1Tlh6UmJnaHZ3ZmpTSitJazBxR1JCaWJzZk1ic1JsSXBwVWR4RFo5QWwzTzNCUUg0dExpcGhma1hjTWtBSk4yYm9JRENzR1RjS3oxNmMvTUd4UnA0YWZMaGxhNWYweXoyWkRzWlFKR3cwdmF6ZGg1SzdoQTcvN01BcFVjWDdha2RMZVNFOFJ5Qkd0UkhkR1YyU3V5RCtWaCt2R0pUcC9hWmZQc0xqN2UxeE44WFZIaHVpa0FFQUtvZnhWWnRnZmthVHFobmtPU1RrT1ltQlhuSG9qd0oyUllyTlNITTRwdnFtcmlzV2tBYm1kdVFSZTBBODNkR3BvWmxiMGlPaXZVWDRhYU1INVZLNklvbFg3cDR2NVNhL2lsZXhmQWdEYmdkNjBMcCtZTFpaVjFvdm50dkg2RTR1eENSMGkwUExmdG1idjV3S2ZWQUVRMHpJR2RIU045dHJpTEF4Vi9MS2NNSWdHQ21ZN2Zuclk9'

        ,'if-none-match': 'W/"52de8-3+EpRWW/CKyGsei/6265AGZFmK4"'

        ,'referer': 'https://hotel.qunar.com/'

        ,'sec-ch-ua': '"Chromium";v="100", "Google Chrome";v="100", ";Not A Brand";v="100"'

        ,'sec-ch-ua-mobile': '?0'

        ,'sec-ch-ua-platform': '"Windows"'

        ,'sec-fetch-dest': 'document'

        ,'sec-fetch-mode': 'navigate'

        ,'sec-fetch-site': 'same-origin'

        ,'sec-fetch-user': '?1'

        ,'upgrade-insecure-requests': '1'

        ,'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

    }

    #伪装成浏览器

    resp = requests.get(html,headers = headers)

    html = BeautifulSoup(resp.content,'html.parser')

    #找到所有酒店信息装进列表dds中

    dds = html.findAll('div',{'class':'inner clearfix'})

    #text编码格式输出

    #遍历dds找出酒店名、评分、地址、价格等信息装进列表中

    for dd in dds:

        #酒店名称

        name1 = dd.find('p',{'class':'name'}).text

        name.append(name1)

        print("酒店名:" + name1)

       #评分

        num = dd.find('p',{'class':'comm'}).text

        allnum.append(num)

        print("评分:" + num)

       #地址

        adress = dd.find('p',{'class':'adress'}).text

        alladress.append(adress)

        print("地址:" + adress)

       #价格

        price = dd.find('p',{'class':'price_new'}).text

        allprice.append(price)

        print("评分:" + price)

except HTTPError as e:

    print(e)

except URLError as e:

    print('The server could not be found')

else:

    print('It Worked!')

#将列表数据存成元组形式转换为数据框

dc = {

    "名称":name,

    "评分":allnum,

    "地址":alladress,

    "价格":allprice

}

print(dc)
#data = pd.DataFrame(dc)

#将爬取到的内容写入文档中

#data.to_csv('./data.csv', encoding="utf-8", index=False, mode='a')