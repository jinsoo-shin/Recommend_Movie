import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from api.models import Rating, Profile, Movie, KmeansResult
from django.db import connection, connections
from django.core.exceptions import EmptyResultSet
from scipy.sparse import csr_matrix
from api.views import helper
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import RatingSerializer, ProfileSerializer, MovieSerializer, SimilarMoviesSerializer, \
    SimilarUsersSerializer
from django.db.models import Avg
import math
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.mixture import GaussianMixture

from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import sqlite3
import os
import time
import gc
import argparse

genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']



@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':

        cnx = sqlite3.connect('db.sqlite3')
        df_movies = pd.read_sql_query("SELECT id movieid,title FROM api_movie",cnx)
        df_ratings = pd.read_sql_query("SELECT id userid,movieid,rating FROM api_rating LIMIT 100000",cnx)

        # print(df_movies.head())
        # print(df_ratings.head())
        # 대상 영화와 데이터베이스의 다른 모든 영화 사이의 "거리"를 계산 한 다음 거리를 평가하고
        # 가장 가까운 K 개의 가장 가까운 이웃 영화를 가장 유사한 영화 추천으로 반환


        #######################

        #######################

        df_movie_features= df_ratings.pivot(
            index='movieid',
            columns='userid',
            values='rating'
        ).fillna(0)

        print(df_movie_features)
        # row가 movieid, col이 userid
        # userid    1   2    3   4
        # movieid
        # 1        3    4   2   4.5

        print(df_movie_features.index)
        print(df_movie_features.columns)
        print(df_movie_features.values[0:5])

        #변환 행렬
        mat_movie_features = csr_matrix(df_movie_features.values)
        print(mat_movie_features)

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        print(model_knn.fit(mat_movie_features))

        distances, indices = model_knn.kneighbors(df_movie_features.reshape(1,-1),n_neighbors=20)

        for i in range(len(distances.flatten())):
            print('{0}: {1}, with distance  of {2}'.format(i,df_movie_features.index[indices.flattens()[i]],distances.flattens()[i]))
        #######################
        # sparse_ratings = csr_matrix(pd.SparseDataFrame(mat_movie_features).to_coo())
        # print(sparse_ratings)



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
