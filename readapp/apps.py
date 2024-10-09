from django.apps import AppConfig

import pymysql
from pymongo import MongoClient
from datetime import datetime

class ReadappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'readapp'

    def ready(self):
        print("시작하자 마자 한 번만 수행")

        #mysql에 접속
        con = pymysql.connect(host='127.0.0.1',
                              port=3306,
                              user='root',
                              passwd='wnddkd',
                              db='cqrs',
                              charset='utf8')
        #Mongo DB에 접속해서 기존 컬렉션 삭제
        conn = MongoClient('127.0.0.1')
        db=conn.cqrs
        collect = db.books
        collect.delete_many({})

        #MySQL의 테이블 읽기
        cursor = con.cursor()
        cursor.execute("select * from writeapp_book")
        data = cursor.fetchall()
        #데이터 순회하면서 데이터를 읽어서 Mongodb에 삽입
        for imsi in data:
            #문자열을 날짜 형식으로 변환
            date = imsi[6].strftime("%Y-%m-%d")
            #Mongodb 데이터 형태 생성
            doc = {'bid':imsi[0], 'title':imsi[1],
                   'author':imsi[2], 'category':imsi[3],
                   'pages':imsi[4], 'price':imsi[5],
                   'published_date': date, 'description':imsi[7]}
            collect.insert_one(doc)
        con.close()
