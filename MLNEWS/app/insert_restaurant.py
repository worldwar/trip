#!/usr/bin/env python
# -*- coding: utf8 -*-
import sqlite3
def insert_restaurant():
    conn = sqlite3.connect('../qunar.db')
    c = conn.cursor()
    data_dt = {}
    with open('./restaurant111.txt','r',encoding='utf-8') as f:
        datas = f.readlines()
        for data in datas:
            name,city,address,desc,comments,score = tuple(data.strip().split("|"))
            name = name.replace('\'', '\'\'')
            desc = desc.replace('\'', '\'\'')
            address = address.replace('\'', '\'\'')
            comments = int(comments)
            try:
                score = float(score)
            except ValueError:
                print("{} Not a float".format(score))
                score = 5.0

            # objects_all = Restaurant.objects.all()
            # r = Restaurant(name=name, city=city, address=address, desc=desc, comments=comments, score=score)
            # r.save()

            sql = '''insert into restaurant(name, city, address, desc, comments, score)
            values ('{}','{}','{}','{}',{},{})'''.format(name, city, address, desc, comments, score)
            print(sql)
            c.execute(sql)

            conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_restaurant()