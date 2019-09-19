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
from pandas import DataFrame as df

genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

dict_genres ={'Action':1, 'Adventure':2, 'Animation':3, "Children's":4, 'Comedy':5, 'Crime':6, 'Documentary':7, 'Drama':8, 'Fantasy':9
    , 'Film-Noir':10, 'Horror':11, 'Musical':12, 'Mystery':13, 'Romance':14, 'Sci-Fi':15, 'Thriller':16, 'War':17, 'Western':18}

@api_view(['GET', 'POST'])
def jwb_view(request):
    if request.method == 'GET':

        # item base로 kNN 구현
        userid = 2

        user = my_sql("user",str(userid)) # 내가 본 영화중 평점 4점 이상의 movieid, genres
        print(user)

        genre_list=[]

        for i in user:
            # print(i[1])
            for genre in genres:
                if genre in i[1]:
                    # print("찾음",genre)
                    genre_list.append([i[0],dict_genres[genre],1])
##########################################
        print(genre_list)

        column_name=['movieid','genre','check']
        df_genre_tmp=pd.DataFrame(genre_list,columns=column_name)

        print(df_genre_tmp)
        

        pv_genre=df_genre_tmp.pivot_table(index="movieid",columns="genre",values="check",fill_value=0)

        print(pv_genre)

        df_genre=pd.DataFrame(pv_genre.to_records())
        print(df_genre)
        ###여기까지 장르 df 완성

        cnx = sqlite3.connect('db.sqlite3')
        query = "select movieid, userid, rating from api_rating where rating>=4 and movieid in (select movieid from api_rating where rating>=4 and userid="+str(userid)+" ) order by movieid asc"
        df_rating = pd.read_sql_query(query, cnx)
        print(df_rating.head())
        ####내가본 영화를 본 다른 유저의 rating 끝

        df_merge=pd.merge(df_rating,df_genre,on='movieid')
        print(df_merge.head())
############

        ##행 추출하고 삭제하기
        predict_x = [] #나중에 예측에 사용할 데이터
        new_df=[]
        for i in range(len(df_merge)):
            if(df_merge.iloc[i]['userid']==userid):
                print(i)
                predict_x = df_merge.iloc[i]
                new_df=df_merge.drop(i)
                break
        print(new_df.head())

        col_list=list(new_df.columns.values)[1:]
        print(col_list)

        item_y=new_df['movieid'].values.reshape(-1,1)
        item_x=new_df.loc[:,col_list]
        # item_x= new_df.drop(['movieid'], axis='columns', inplace=True)
        output = MinMaxScaler().fit_transform(item_x)
        item_x = pd.DataFrame(output)
        print(item_x)
        kNN=KNeighborsClassifier(n_neighbors=5)

        print("예측용 데이터 영화",predict_x)
        pre= list(predict_x)[1:]
        pre=np.array(pre)
        pre=pre.reshape(1,-1)
        test = kNN.fit(item_x,item_y).predict(pre)
        print(test)
        print(item_y[test])
        request_data=[]
        return Response(status=status.HTTP_200_OK,data=request_data)
        # return Response(status=status.HTTP_200_OK,data=json.dumps(request_data), headers=headers)

def my_sql(key, value):
    cursor = connection.cursor()
    if key == 'user':
        query = "select r.movieid, m.genres from api_rating r, api_movie m where r.userid="+value+" and r.rating>=4 and r.movieid=m.id order by m.id asc" 
        cursor.execute(query)
    row = cursor.fetchall()
    return row

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

####KNN알고리즘