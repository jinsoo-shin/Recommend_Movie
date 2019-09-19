import pandas as pd
import numpy as np
from django.db import connection, connections
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sklearn.neighbors import KNeighborsRegressor
import sqlite3

genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']


@api_view(['GET', 'POST'])
def jwb_view(request):
    if request.method == 'GET':

        cnx = sqlite3.connect('db.sqlite3')
        df = pd.read_sql_query("SELECT r.userid, r.rating,p.gender,p.age,p.occupation FROM api_profile p,api_rating r WHERE p.id = r.userid and r.movieid=1197 LIMIT 10",cnx)

        print(df.head())

        print(df['gender'].value_counts())

        df['gender']=df['gender'].map({
            'F':0,
            'M':1
        })

        print(df.head())

        df['occupation'] = df['occupation'].map({
            "other":0, "academic/educator":1, "artist":2,"clerical/admin":3, "college/grad student":4,
           "customer service":5,  "doctor/health care":6,"executive/managerial":7,"farmer":8,  "homemaker":9,
             "K-12 student":10, "lawyer":11, "programmer":12, "retired":13, "sales/marketing":14,
             "scientist":15,  "self-employed":16,  "technician/engineer":17, "tradesman/craftsman":18,
             "unemployed":19,  "writer":20
        })
        print(df.head())

        y=df['rating'].values.reshape(-1,1)
        X=df.loc[:,['userid','gender','age','occupation']]

        kNN = KNeighborsRegressor(n_neighbors=2)

        print(kNN.fit(X,y))
        example = np.array([1,0,1,10])
        example = example.reshape(1, -1)
        test = kNN.fit(X,y).predict(example)

        print(test)
        # print("ddd",df.loc[:,['userid','gender','age','occupation']])
        # 대상 영화와 데이터베이스의 다른 모든 영화 사이의 "거리"를 계산 한 다음 거리를 평가하고
        # 가장 가까운 K 개의 가장 가까운 이웃 영화를 가장 유사한 영화 추천으로 반환


        request_data=[]
        return Response(status=status.HTTP_200_OK,data=request_data)
        # return Response(status=status.HTTP_200_OK,data=json.dumps(request_data), headers=headers)



def my_sql(key, value):
    cursor = connection.cursor()
    if key == 'user':
        str = 'SELECT username FROM `auth_user` WHERE id IN (' + value + ')'
        cursor.execute(str)

    # row = cursor.fetchall()
    # return row
    row = dictfetchall(cursor)
    return row


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

####KNN알고리즘