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
from sklearn.preprocessing import MinMaxScaler,Normalizer
from sklearn.decomposition import NMF

#  X = np.array([[1, 1], [2, 1], [3, 1.2], [4, 1], [5, 0.8], [6, 1]])
# >>> from sklearn.decomposition import NMF
# >>> model = NMF(n_components=2, init='random', random_state=0)
# >>> W = model.fit_transform(X)
# >>> H = model.components_


genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

dict_occupation ={"other":0, "academic/educator":1, "artist":2,"clerical/admin":3, "college/grad student":4,
   "customer service":5,  "doctor/health care":6,"executive/managerial":7,"farmer":8,  "homemaker":9,
     "K-12 student":10, "lawyer":11, "programmer":12, "retired":13, "sales/marketing":14,
     "scientist":15,  "self-employed":16,  "technician/engineer":17, "tradesman/craftsman":18,
     "unemployed":19,  "writer":20}

dict_gender={'F':0,
    'M':1}

@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':
        userid = request.GET.get('userid', None)
        if not userid:
            userid=1
        cnx = sqlite3.connect('db.sqlite3')
        query = "select distinct(userid), p.gender, p.age from api_rating r,api_profile p where r.userid= p.id and rating>=4 and userid !=  "+str(userid)+" and movieid in (select movieid from api_rating where rating>=4 and userid= "+str(userid)+" ) order by movieid asc"
        df_user = pd.read_sql_query(query, cnx)
        df_user['gender']=df_user['gender'].map({
            'F':0,
            'M':1
        })
        # print(df_user.head())

        query = "select userid, movieid, rating from api_rating where rating>=4 and userid != "+str(userid)+" and movieid in (select movieid from api_rating where rating>=4 and userid="+str(userid)+" ) order by movieid asc"
        df_rating = pd.read_sql_query(query, cnx)
        # print(df_rating.head())
        #각각의 영화를 본 유저들의 rating을 가져오기


        dfdf = df_rating.pivot_table(index="userid",columns="movieid",values="rating",fill_value=0)
        # print(dfdf.head())

        df_rating_flat = pd.DataFrame(dfdf.to_records())

        df_new = pd.merge(df_user,df_rating_flat,on="userid")

        print("rating이랑 유저정보 합체",df_new.head())

        col_list = list(df_new.columns.values)[1:]  #정규화를 위해 사용합니다

        y = df_new['userid'].values.reshape(-1, 1)
        X=df_new.loc[:,col_list]

        ####################
        vector_array = X.as_matrix()
        nmf = NMF(n_components=20)
        features=nmf.fit_transform(vector_array)



        normalizer = Normalizer()
        norm_features = normalizer.fit_transform(features)
        df_features = pd.DataFrame(norm_features)
        print(df_features.head())

        ##유사도

        #####################
        output = Normalizer().fit_transform(X)
        X= pd.DataFrame(output)
        print(X.head())
        #gender, age, 봤던 영화 리스트~~~~~
        user = my_sql("user",str(userid))

        movie_list_tmp = my_sql("movie",str(userid))

        my_user_list =[dict_gender[user[0]], user[1]]
        for i in range(len(movie_list_tmp)):
            my_user_list.append(movie_list_tmp[i][0])

        # print(my_user_list)

        example = np.array(my_user_list)
        example = example.reshape(1, -1)
################################
        ##유사도
        similar = df_features.dot(example)
        top = similar.nlargest()
        print("결과",top)
################################
        # kNN = KNeighborsClassifier(n_neighbors=5)
        # test = kNN.fit(X,y).predict(example)
        # print(test)
        # print(y[test])

        nN= NearestNeighbors(n_neighbors=5,metric="euclidean").fit(X,y)
        nN_predict =nN.kneighbors_graph(example).toarray()

        similar_user= []
        for i in range(len(nN_predict[0])):
            if nN_predict[0][i] == 1.0:
                similar_user.append(str(y[i][0]))
        print("유사한 유저 id",similar_user)

        user_list=",".join(similar_user)
        query="select id movieid,title,genres,rating from api_movie where movieid in (select movieid from api_rating where userid in ("+user_list+") and movieid not in ( select movieid from api_rating where userid=" + str(userid)+") group by movieid having avg(rating) order by avg(rating) desc limit 10)"
        result = pd.read_sql_query(query, cnx)
        print(result.head())


        # df_test = pd.DataFrame(index=df_user,columns=df_movie)
        # print(df_test)
        # sql = "Select user_id,gender,age,occupation from api_profile where gender= '"+ str(user[0])+ "' and age = "+ str(user[1])+" and not user_id= "+str(userid)

#################################

        # # 대상 영화와 데이터베이스의 다른 모든 영화 사이의 "거리"를 계산 한 다음 거리를 평가하고
        # # 가장 가까운 K 개의 가장 가까운 이웃 영화를 가장 유사한 영화 추천으로 반환

#################################

        request_data=[]
        for i in range(len(result)):
            request_data.append({"key":i,"movieid":result['movieid'][i],"title":result['title'][i],"genres":result['genres'][i],"rating":result['rating'][i],"src":"https://images-na.ssl-images-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_UX182_CR0,0,182,268_AL_.jpg"})
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
    if key == "movie":
        query="select movieid from api_rating where rating>=4 and userid="+value+" order by movieid asc"
        cursor.execute(query)
        row=cursor.fetchall()
        # row = dictfetchall(cursor)
        return row
    if key == "rating":
        query="select movieid from api_rating where rating>=4 and userid="+value+" order by movieid asc"
        cursor.execute(query)
        row = dictfetchall(cursor)
        return row



    #  row = cursor.fetchall()
    # return row


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

####KNN알고리즘
