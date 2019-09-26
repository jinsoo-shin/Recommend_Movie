import pandas as pd
import numpy as np
from django.db import connection, connections
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
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
        userid = request.GET.get('userid', None)
        if not userid:
            userid = 2
        # item base로 kNN 구현
        # userid = 2 # 로그인한 유저id를 param으로 가져온다.

        user = my_sql("user",str(userid)) # 내가 본 영화중 평점 4점 이상의 movieid, genres
        print("로그인유저정보: ", user)

        genre_list=[]

        # for문 돌면서 genres list 안에 해당 genre가 있다면 1을 넣는다.
        for i in user:
            # print(i[1])
            for genre in genres:
                if genre in i[1]:
                    # print("찾음",genre)
                    genre_list.append([i[0],dict_genres[genre],1])
##########################################
        print(genre_list)

        # dataframe 형식으로 만든다
        column_name=['movieid','genre','check']
        df_genre_tmp=pd.DataFrame(genre_list,columns=column_name)

        print(df_genre_tmp)
        
        #pivot 테이블로 만들어, 해당 장르가 있다면 1, 없다면 0으로 채운다
        pv_genre=df_genre_tmp.pivot_table(index="movieid",columns="genre",values="check",fill_value=0)

        print(pv_genre)

        # 최종적으로 dataframe 형식으로 만든다
        df_genre=pd.DataFrame(pv_genre.to_records())
        print("df_genre",df_genre)
        ###여기까지 장르 df 완성

        #내가 본 영화(rating>=4)를 본 다른 유저들의 전체 avg(rating)을 가져온다
        cnx = sqlite3.connect('db.sqlite3')
        query = "select movieid, avg(rating) rating from api_rating where userid !="+str(userid)+" and movieid in (select movieid from api_rating where rating>=4 and userid= "+str(userid)+") group by movieid order by movieid asc"
        # query = "select movieid, avg(rating) rating from api_rating where rating>=4 and movieid in (select movieid from api_rating where rating>=4 and userid= "+str(userid)+") group by movieid order by movieid asc"
        # query = "select movieid, userid, rating from api_rating where rating>=4 and movieid in (select movieid from api_rating where rating>=4 and userid="+str(userid)+" ) order by movieid asc"
        df_rating = pd.read_sql_query(query, cnx)
        print("df_rating",df_rating.head())
        ####내가본 영화를 본 다른 유저의 rating 끝

        df_merge=pd.merge(df_rating,df_genre,on='movieid')
        print(df_merge.head())
############
        ## 예측에 사용할 userid 정보 기반의 dataframe을 생성한다
        query = "select movieid,rating from api_rating where rating>=4 and userid="+str(userid)+" order by rating desc,date desc limit 1"
        df_myuser= pd.read_sql_query(query, cnx)
        myuser_X=pd.merge(df_myuser,df_genre, on='movieid')
        print("출력",myuser_X)


        #훈련에 사용할 Y 데이터를 df에서 0번째 column인 movieid를 가져와 만든다
        item_y=df_merge['movieid'].values.reshape(-1,1)


        #훈련에 사용할 X 데이터를 datascaling 하기 위해 columns 리스트를 가져온다
        col_list=list(df_merge.columns.values)[1:]
        print(col_list)
        #훈련에 사용할 X 데이터를 df에서 뽑아온다.
        item_x=df_merge.loc[:,col_list]

        # item_x= new_df.drop(['movieid'], axis='columns', inplace=True)

        # datascaling 작업을 수행하여 dataframe으로 다시 만든다
        output = MinMaxScaler().fit_transform(item_x)
        item_x = pd.DataFrame(output)
        print(item_x)
        # kNN=KNeighborsClassifier(n_neighbors=5)

        # 유클리디안 거리 기반으로 가까운 5개를 가져오도록 훈련한다
        kNN=NearestNeighbors(n_neighbors=10,metric="euclidean").fit(item_x, item_y)

        # 예측에 사용할 userid를 가져와 예측에 사용할 수 있는 형식으로 만든다
        print("예측에 사용할 마이유저df: ",myuser_X)
        pre= list(myuser_X.loc[0])[1:]
        print("마이유저의 df를 array로 변경: ",pre)
        pre=np.array(pre)
        pre=pre.reshape(1,-1)
        print(pre)
        
        # 예측 후 결과를 눈으로 확인할 수 있도록 정제한다
        kNN_pre = kNN.kneighbors_graph(pre).toarray()
        print(kNN_pre[0])
        pre_list=[]
        for i in range(len(kNN_pre[0])):
            if kNN_pre[0][i] == 1:
                pre_list.append(str(item_y[i][0]))
                print(i)

        # 사용자에게 추천할 영화id 5개
        print(pre_list)
        movie_list = ",".join(pre_list)
        print("추천 영화 10개",movie_list)
        # query = "select m.id,m.title,m.genres,m.rating,c.posterUrl from api_movie m Left join api_moviecontent c on m.id=c.id where m.id in ("+movie_list+")"
        query="select m.id,m.title,m.genres,m.rating, p.posterUrl,p.Summary,p.Director,p.Writers,p.ImdbLink from api_movie m left join api_moviecontent p on m.id = p.id where m.id in ("+movie_list+")"
        result = pd.read_sql_query(query, cnx)
        print(result)

        request_data = []
        for i in range(len(result)):
            # print(result['posterUrl'][i])
            src = result['posterUrl'][i]
            ImdbLink = result['ImdbLink'][i]
            Director = result['Director'][i]
            Writers = result['Writers'][i]
            Summary = result['Summary'][i]
            if src is None:
                src = "http://folo.co.kr/img/gm_noimage.png"
            request_data.append(
                {"key": i, "movieid": result['id'][i], "title": result['title'][i], "genres": result['genres'][i],
                 "rating": result['rating'][i], "src": src, "ImdbLink": ImdbLink, "Director": Director,
                 "Writers": Writers, "Summary": Summary})
        return Response(status=status.HTTP_200_OK, data=request_data)
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