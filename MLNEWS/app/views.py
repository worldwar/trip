import datetime
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests
import json
import jieba
from bs4 import BeautifulSoup
from django.db.models import F, Count, Sum
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import joblib
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from tqdm import tqdm
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys  # Keys类   #common
from selenium.webdriver.support.ui import Select  # select类定位下拉框

from app.itemBasedCF import  ItemBasedCF
from app.models import *
from random import shuffle


def type2sql(request):
    """
    数据录入
                'sheng':_['sheng'],
                'sheng_url':_['sheng_url'],
                'city_name':_['city_name'],
                'city_url':_['city_url'],

                'jingqu_name':jingqu_name,
                'jingqu_url':jingqu_url,
                'ever':ever,
                'never':never,
                'level':level,
    :param request:
    :return:
    """
    raw_data = json.load(open('sheng_city_jingqu_list.json','r'))
    for item in tqdm(raw_data):
        sheng = item['sheng']
        sheng_url = item['sheng_url']
        city_name = item['city_name']
        city_url = item['city_url']
        jingqu_name = item['jingqu_name']
        jingqu_url = item['jingqu_url']
        ever = item['ever']
        never = item['never']
        level = item['level']

        ever = int(ever)
        never = int(never)
        if not JingQu.objects.filter(sheng=sheng,sheng_url=sheng_url,city=city_name,city_url=city_url,
                              jingqu=jingqu_name,
                              jingqu_url=jingqu_url,
                              ever=ever,never=never,
                              level=level):
            JingQu.objects.create(sheng=sheng,sheng_url=sheng_url,city=city_name,city_url=city_url,
                              jingqu=jingqu_name,
                              jingqu_url=jingqu_url,
                              ever=ever,never=never,
                              level=level)
    return HttpResponse("数据录入完毕")


# 验证登录
def check_login(func):
    def wrapper(request):
        # print("装饰器验证登录")
        cookie = request.COOKIES.get('uid')
        if not cookie:
            return redirect('/login/')
        else:
            return func(request)

    return wrapper


# Create your views here.
@check_login
def index(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name
    sheng_kind = [item.sheng for item in JingQu.objects.all()]
    sheng_kind = list(set(sheng_kind))
    if 'sheng_name' not in request.GET:  # 新闻类别
        sheng_name = sheng_kind[0]
        if 'city_name'  not in request.GET:
            city_kind = list(set([item.city for item in JingQu.objects.filter(sheng=sheng_name)] ))
            city_name = city_kind[0]
        else:
            city_kind = list(set([item.city for item in JingQu.objects.filter(sheng=sheng_name)] ))
            city_name = request.GET.get('city_name')
    else:
        sheng_name = request.GET.get('sheng_name')
        if 'city_name'  not in request.GET:
            city_kind = list(set([item.city for item in JingQu.objects.filter(sheng=sheng_name)] ))
            city_name = city_kind[0]
        else:
            city_kind = list(set([item.city for item in JingQu.objects.filter(sheng=sheng_name)] ))
            city_name = request.GET.get('city_name')
    newlist = JingQu.objects.filter(sheng=sheng_name, city=city_name)
    tmp = []
    for item in newlist:
        if Like.objects.filter(uid_id=uid, jingqu_id=item.id):
            is_like = 1
        else:
            is_like = 0
        tmp.append({
            'id': item.id,
            'sheng': item.sheng,
            'sheng_url': item.sheng_url,
            'city': item.city,
            'city_url': item.city_url,
            'jingqu': item.jingqu,
            'jingqu_url': item.jingqu_url,
            'img': item.img,
            'ever': item.ever,
            'never': item.never,
            'level': item.level,
            'is_like': is_like,
        })
    newlist = tmp

    return render(request, 'index.html', locals())


def star_ajax(request):
    """
    收藏的ajax
    :param request:
    :return:
    """
    res = {}
    yid = int(request.POST.get('id'))
    uid = int(request.COOKIES.get('uid', -1))

    if Like.objects.filter(uid_id=uid, jingqu_id=yid):
        Like.objects.filter(uid_id=uid, jingqu_id=yid).delete()
        res['color'] = 'black'
    else:
        Like.objects.create(uid_id=uid, jingqu_id=yid)
        res['color'] = 'red'
    return JsonResponse(res)




def my_shoucang(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name

    newlist = []
    if Like.objects.filter(uid_id=uid):
        newlist = Like.objects.filter(uid_id=uid)
    id_list = [item.jingqu_id for item in newlist]
    newlist = JingQu.objects.filter(id__in=id_list)
    tmp = []
    for item in newlist:
        if Like.objects.filter(uid_id=uid, jingqu_id=item.id):
            is_like = 1
        else:
            is_like = 0
        tmp.append({
            'id': item.id,
            'sheng': item.sheng,
            'sheng_url': item.sheng_url,
            'city': item.city,
            'city_url': item.city_url,
            'jingqu': item.jingqu,
            'jingqu_url': item.jingqu_url,
            'img': item.img,
            'ever': item.ever,
            'never': item.never,
            'level': item.level,
            'is_like': is_like,
        })
    newlist = tmp
    return render(request, 'my_shoucang.html', locals())



@check_login
def detail(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name


    if request.method == 'GET':
        id_ = int(request.GET.get('id'))
        print(f'景区ID=={id_}')
        infos = JingDian.objects.filter(jingqu_id=int(id_))
        if See.objects.filter(uid_id=uid ,jingqu_id=int(id_)):
            See.objects.filter(uid_id=uid,jingqu_id=int(id_)).update(num=F('num') + 1)
        else:
            See.objects.create(uid_id=uid,jingqu_id=int(id_),num=1)
        comment_list = Comment.objects.filter(jingdian_id=int(id_))
        leng = len(comment_list)
        if leng == 0:
            avg_num = 0
        else:
            avg_num = sum([item.score for item in comment_list]) / leng
        return render(request, 'detail.html', locals())
    else:
        data = request.POST
        score, content, jid = data.get('score'), data.get('content'), data.get('jid')
        print(jid)
        Comment.objects.create(user_id=int(uid), jingdian_id=int(jid), content=content, score=int(float(score) * 2))
        return HttpResponse('post方法')







def scrawl_jingqu(jid):
    """
    如果没有景区数据，那就爬取数据
    :param request:
    :return:
    """
    domain = 'https://www.meet99.com'
    res= {'status':1,'msg':'ok'}
    jid = int(jid)

    drvier = webdriver.Chrome()
    url = 'https://www.meet99.com/jingdian-tiantan.html'  # 爬取景区的首页
    url = JingQu.objects.get(id=int(jid)).jingqu_url   # 爬取景区的首页
    drvier.get(url)
    time.sleep(1)
    one_soup = BeautifulSoup(drvier.page_source, 'lxml')
    drvier.close()
    ## 获取图片地址
    img_url = one_soup.find('div', class_='img')['style'].split('(')[1].split(')')[0]
    img_url = img_url.replace('"', '')
    #更新景区的 图片地址
    JingQu.objects.filter(id=jid).update(img=img_url) #

    ######### 下面遍历下一页
    # 获取下一页
    next = one_soup.find('div', id='jdright').find('a', string='下一页')
    """<a href="/jingdian-ForbiddenCity-1992.html" style="color:#66F;font-weight:bold;" t="前朝区">下一页</a>
    """
    cnt = 0
    while next :
        next_url = domain + next['href']
        drvier = webdriver.Chrome()
        drvier.get(next_url)
        time.sleep(1)
        next_soup = BeautifulSoup(drvier.page_source, 'lxml')
        drvier.close()
        ## 获取图片地址
        img_url = next_soup.find('div', class_='img')['style'].split('(')[1].split(')')[0]
        img_url = img_url.replace('"', '')
        # 获取title
        title = next_soup.find('h1', class_='title').text
        # detail获取介绍
        try:
            detail = next_soup.find('div', class_='spotinfo').text
        except Exception as e:
            detail = ''
        # print(jid,detail,img_url,title)
        if not JingDian.objects.filter(jingqu_id=jid,detail=detail,img=img_url,title=title):
            JingDian.objects.create(jingqu_id=jid, detail=detail, img=img_url, title=title)
        next = next_soup.find('div', id='jdright').find('a', string='下一页')
        cnt += 1
        if cnt >= 3:
            break

    return 'ok'


def scrawlNew(request):
    # 第一步 找到景区中没有图片的
    threadPool = ThreadPoolExecutor(max_workers=5)
    for item in JingQu.objects.filter(img=''):
        threadPool.submit(scrawl_jingqu,item.id)
    return HttpResponse('OKOKOKOK')


def scrawl_ajax(request):
    """
    如果没有景区数据，那就爬取数据
    :param request:
    :return:
    """
    domain = 'https://www.meet99.com'
    res= {'status':1,'msg':'ok'}
    jid = request.POST.get('id') # 景区的id
    jid = int(jid)

    drvier = webdriver.Chrome()
    url = 'https://www.meet99.com/jingdian-tiantan.html'  # 爬取景区的首页
    url = JingQu.objects.get(id=int(jid)).jingqu_url   # 爬取景区的首页
    drvier.get(url)
    time.sleep(1)
    one_soup = BeautifulSoup(drvier.page_source, 'lxml')
    drvier.close()
    ## 获取图片地址
    img_url = one_soup.find('div', class_='img')['style'].split('(')[1].split(')')[0]
    img_url = img_url.replace('"', '')
    #更新景区的 图片地址
    JingQu.objects.filter(id=jid).update(img=img_url) #

    ######### 下面遍历下一页
    # 获取下一页
    next = one_soup.find('div', id='jdright').find('a', string='下一页')
    """<a href="/jingdian-ForbiddenCity-1992.html" style="color:#66F;font-weight:bold;" t="前朝区">下一页</a>
    """
    cnt = 0
    while next :
        next_url = domain + next['href']
        drvier = webdriver.Chrome()
        drvier.get(next_url)
        time.sleep(1)
        next_soup = BeautifulSoup(drvier.page_source, 'lxml')
        drvier.close()
        ## 获取图片地址
        img_url = next_soup.find('div', class_='img')['style'].split('(')[1].split(')')[0]
        img_url = img_url.replace('"', '')
        # 获取title
        title = next_soup.find('h1', class_='title').text
        # detail获取介绍
        try:
            detail = next_soup.find('div', class_='spotinfo').text
        except Exception as e:
            detail = ''
        print(jid,detail,img_url,title)
        if not JingDian.objects.filter(jingqu_id=jid,detail=detail,img=img_url,title=title):
            JingDian.objects.create(jingqu_id=jid, detail=detail, img=img_url, title=title)
        next = next_soup.find('div', id='jdright').find('a', string='下一页')
        cnt += 1
        if cnt >= 3:
            break

    return JsonResponse(res, safe=True)

@check_login
def tuijian(request):

    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name
    train = dict()
    history = Like.objects.all()  # 0.1
    for item in history:
        if item.uid_id not in train.keys():
            train[item.uid_id] = {item.jingqu_id: 10}
        else:
            train[item.uid_id][item.jingqu_id] = train[item.uid_id].get(item.jingqu_id, 0) + 10 # 喜欢加10分
    history = See.objects.all()  # 0.1
    for item in history:
        if item.uid_id not in train.keys():
            train[item.uid_id] = {item.jingqu_id: 0.1 * item.num}
        else:
            train[item.uid_id][item.jingqu_id] = train[item.uid_id].get(item.jingqu_id, 0) + 1 * item.num
    # 声明一个的对象
    newlist = []
    try:
        item = ItemBasedCF(train)
        item.ItemSimilarity()
        recommedDict = item.Recommend(int(uid))  # 字典
        newlist = JingQu.objects.filter(id__in=list(recommedDict.keys()))
    except:
        print("协同过滤异常啦")
        pass
    if len(newlist) == 0:
        msg = "你还没有在该网站有过点赞、浏览行为，请去浏览吧！"
        newlist = JingQu.objects.order_by('-ever')[:10]
    else:
        msg = ""
    tmp = []
    for item in newlist:
        if Like.objects.filter(uid_id=uid, jingqu_id=item.id):
            is_like = 1
        else:
            is_like = 0
        tmp.append({
            'id': item.id,
            'sheng': item.sheng,
            'sheng_url': item.sheng_url,
            'city': item.city,
            'city_url': item.city_url,
            'jingqu': item.jingqu,
            'jingqu_url': item.jingqu_url,
            'img': item.img,
            'ever': item.ever,
            'never': item.never,
            'level': item.level,
            'is_like': is_like,
        })
    newlist = tmp
    return render(request, 'tuijian.html', locals())


def test(request):
    return HttpResponse('测试完成')


@check_login
def search(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name
    newlist = []
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        newlist = []
        for item in JingQu.objects.all():
            if keywords in item.jingqu :
                newlist.append(item)
        tmp = []
        for item in newlist:
            if Like.objects.filter(uid_id=uid, jingqu_id=item.id):
                is_like = 1
            else:
                is_like = 0
            tmp.append({
                'id': item.id,
                'sheng': item.sheng,
                'sheng_url': item.sheng_url,
                'city': item.city,
                'city_url': item.city_url,
                'jingqu': item.jingqu,
                'jingqu_url': item.jingqu_url,
                'img': item.img,
                'ever': item.ever,
                'never': item.never,
                'level': item.level,
                'is_like': is_like,
            })
        newlist = tmp
    else:
        keywords = ''
    return render(request, 'search.html', locals())


def login(request):
    if request.method == "POST":
        tel, pwd = request.POST.get('tel'), request.POST.get('pwd')
        if User.objects.filter(tel=tel, password=pwd):
            obj = redirect('/')
            obj.set_cookie('uid', User.objects.filter(tel=tel, password=pwd)[0].id, max_age=60 * 60 * 24)
            return obj
        else:
            msg = "用户信息错误，请重新输入！！"
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())


def register(request):
    if request.method == "POST":
        name, tel, pwd = request.POST.get('name'), request.POST.get('tel'), request.POST.get('pwd')
        print(name, tel, pwd)
        if User.objects.filter(tel=tel):
            msg = "你已经有账号了，请登录"
        else:
            User.objects.create(name=name, tel=tel, password=pwd)
            msg = "注册成功，请登录！"
        return render(request, 'login.html', locals())
    else:
        msg = ""
        return render(request, 'register.html', locals())


def logout(request):
    obj = redirect('/')
    obj.delete_cookie('uid')
    return obj

def plot(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name

    main1 = Like.objects.values('jingqu').annotate(count=Count('jingqu__jingqu'))
    main1 = list(main1)
    main1 = sorted(main1,key=lambda x:x['count'],reverse=True)
    # print(main1)
    main1_x = [JingQu.objects.get(id=item['jingqu']).jingqu   for item in main1][:10]
    main1_y = [item['count']   for item in main1][:10]



    # main2
    main2 = JingQu.objects.order_by('-ever','never')[:10]
    # for item in main2[:5]:
    #     print(item.ever,item.never)
    main2_x = [item.jingqu for item in main2]
    main2_y1 = [item.ever for item in main2]
    main2_y2 = [item.never for item in main2]

    main3 = JingQu.objects.values('city').annotate(count=Count('city'))
    main3 = sorted(main3,key=lambda  x: x['count'],reverse=True)[:10]
    main3_x = [item['city'] for item in main3]
    main3_y = [{'value': item['count'], 'name': item['city']}
        for item in main3
    ]

    main4 = See.objects.values('jingqu').annotate(count=Sum('num'))
    main4 = sorted(main4,key=lambda  x: x['count'],reverse=True)[:10]
    print(main4)
    main4_x = [JingQu.objects.get(id=item['jingqu']).jingqu for item in main4][:10]
    main4_y = [item['count'] for item in main4][:10]

    # main5 = See.objects.values('jingqu').annotate(count=Sum('num'))

    main5 = [{'name':item['city'], 'value':item['count'] }for item in main3][:20]

    all_sights = Sight.objects.all()

    hot_sights = Sight.objects.order_by('-hot')[:60]

    main5 = [{'name':item.name, 'value':item.comments }for item in hot_sights][:60]
    shuffle(main5)
    main5 = main5[:20]

    love_sights = Sight.objects.order_by('-comments')[:60]
    main6 = [{'name':item.name, 'value':item.comments }for item in love_sights][:60]
    shuffle(main6)
    main6 = main6[:20]

    return  render(request,'plot.html',locals())
