import pandas as pd
import numpy as np
from django.db import connection, connections
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
import sqlite3
from sklearn.preprocessing import MinMaxScaler

genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']



@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':

        userid = 2
        user = my_sql("user",str(userid))
        cnx = sqlite3.connect('db.sqlite3')
        sql = "Select user_id,gender,age,occupation from api_profile where gender= '"+ str(user[0])+ "' and age = "+ str(user[1])+" and not user_id= "+str(userid)
        # sql = "Select user_id,gender,age,occupation from api_profile where gender= '"+ str(user[0])+ "' and age = "+ str(user[1])+" and occupation= '"+str(user[2])+"' and not user_id= "+str(userid)

        print(pd.read_sql_query(sql,cnx))

        dict_gender={'F':2,
            'M':1}
        df = pd.read_sql_query(sql,cnx)

        addRownum =[]
        for i in range(len(df)):
            addRownum.append(i+1)

        df['rownum']=addRownum

        df['gender']=df['gender'].map({
            'F':2,
            'M':1
        })

        # print(df.head())
        dict_occupation ={"other":21, "academic/educator":1, "artist":2,"clerical/admin":3, "college/grad student":4,
           "customer service":5,  "doctor/health care":6,"executive/managerial":7,"farmer":8,  "homemaker":9,
             "K-12 student":10, "lawyer":11, "programmer":12, "retired":13, "sales/marketing":14,
             "scientist":15,  "self-employed":16,  "technician/engineer":17, "tradesman/craftsman":18,
             "unemployed":19,  "writer":20}
        df['occupation'] = df['occupation'].map({
            "other":21, "academic/educator":1, "artist":2,"clerical/admin":3, "college/grad student":4,
           "customer service":5,  "doctor/health care":6,"executive/managerial":7,"farmer":8,  "homemaker":9,
             "K-12 student":10, "lawyer":11, "programmer":12, "retired":13, "sales/marketing":14,
             "scientist":15,  "self-employed":16,  "technician/engineer":17, "tradesman/craftsman":18,
             "unemployed":19,  "writer":20
        })

        # df=df.sample(frac=1)
        # df=df.sample(frac=1).reset_index(drop=True)
        print(df.head())

        # output = MinMaxScaler.transform(df)
        # output = pd.DataFrame(output, columns=df.columns, index=list(df.index.values))



        y=df['rownum'].values.reshape(-1,1)
        # y=df['user_id'].values.reshape(-1,1)
        X=df.loc[:,['gender','age','occupation']]

        output = MinMaxScaler().fit_transform(X)
        X= pd.DataFrame(output)
        print(X)


        kNN = KNeighborsClassifier(n_neighbors=5)
        # kNN = KNeighborsRegressor(n_neighbors=5)

        print(kNN.fit(X,y))
        example = np.array([dict_gender[user[0]],user[1],dict_occupation[user[2]]])
        # example = np.array([0,1,10])
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
        # str = 'SELECT username FROM `auth_user` WHERE id IN (' + value + ')'
        query = "Select gender,age,occupation from api_profile where id = "+value
        cursor.execute(query)

    row = cursor.fetchone()
    return row


    #  row = cursor.fetchall()
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
