#!/usr/bin/env python
# -*- coding: utf8 -*-
import sqlite3

citys = ["北京","上海","成都","三亚","广州","重庆","深圳"]

def create_table():
    conn = sqlite3.connect('qunar.db')
    c = conn.cursor()
    table_sql = '''CREATE TABLE jingdian
        (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        NAME           CHAR(64),
        DESC           TEXT,
        CITY           CHAR(6),
        LEVEL          CHAR(32),
        ADDRESS        TEXT,
        PRICE          CHAR(8),
        SALES          CHAR(8),
        HOT            CHAR(4),
        COMMENT_HIGH   CHAR(8),
        COMMENT_MID    CHAR(8),
        COMMENT_LOW    CHAR(8),
        COMMENTS       CHAR(16),
        COMMENT_MARK   CHAR(8));'''
    c.execute(table_sql)
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('qunar.db')
    c = conn.cursor()
    data_dt = {}
    with open('./景点数据/景点数据/comments.txt','r',encoding='utf-8') as f:
        datas = f.readlines()
        for data in datas:
            name,high_comment,mid_comment,low_comment,comments,comment_mark = tuple(data.strip().split("|"))
            high_comment = comment_extract(high_comment)
            mid_comment = comment_extract(mid_comment)
            low_comment = comment_extract(low_comment)
            comments = comment_extract(comments)
            #print(name,high_comment,mid_comment,low_comment,comments,comment_mark)
            data_dt[name] = [high_comment,mid_comment,low_comment,comments,comment_mark]
    for city in citys:
        with open('./景点数据/景点数据/{}.txt'.format(city),'r',encoding='utf-8') as f:
            datas = f.readlines()
            for data in datas:
                #print(data.strip().split("|"))
                try:
                    name, level,desc,price,sales,address,hot = tuple(data.strip().split("|"))
                    params = tuple([name, level,desc,city,price,sales,address,hot]+data_dt.get(name,["无","无","无","无","无"]))
                    #print(name, level,desc,price,sales,address,hot,data_dt.get(name,["无","无","无","无","无"]))
                    insert_sql = '''insert into jingdian (name, level, desc,city, price,sales, address,hot, comment_high,comment_mid,comment_low,comments,comment_mark) \
                        values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(*params)
                    c.execute(insert_sql)
                    print(insert_sql)
                except Exception as e:
                    print(e)
                    #print(data)
                #print(name, level,desc,price,sales,address,hot)
                conn.commit()
    conn.close()    



def comment_extract(comment):
    if "(" in comment:
        comment = comment.split("(")[1].split(")")[0]
    return comment

if __name__ == "__main__":
    create_table()
    insert_data()