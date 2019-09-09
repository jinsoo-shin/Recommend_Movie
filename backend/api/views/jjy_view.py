from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie,Rating
from api.serializers import MovieSerializer,RatingSerializer
from rest_framework.response import Response
from django.core.exceptions import EmptyResultSet
from django.db.models import Avg
from django.db import connection,connections
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from api.views import helper
from sklearn.cluster import AgglomerativeClustering

def to_df(queryset, using=None, compiler=None):
    try:
        if type(queryset) == str:  # SQL이 문자열로 그대로 들어올 경우
            query = queryset
            params = None
        else:
            if using:  # 어떤 DB를 사용할지 지정한다면..
                con = connections[using]
            else:
                con = connections['default']
            if compiler:  # 어떤 SQLCompiler를 사용할지 지정한다면..
                query, params = queryset.query.as_sql(compiler=compiler, connection=con)
            else:
                query, params = queryset.query.sql_with_params()
    except EmptyResultSet:  # 만약 쿼리셋의 결과가 비어있다면 빈 DataFrame 반환
        return pd.DataFrame()
    if using:  # 어떤 DB를 사용할지 지정했다면 해당 DB connection 이용
        df = pd.read_sql_query(query, connections[using], params=params)
    else:
        df = pd.read_sql_query(query, connection, params=params)
    return df


# movie_queryset = Movie.objects.all()
# rating_queryset = Rating.objects.all()

# # rating_limit = len(rating_queryset) * (rating_percent / 100)
# # rating_queryset = rating_queryset[:rating_limit]
# rating_queryset = rating_queryset[:1000]

# movies = to_df(movie_queryset)
# ratings = to_df(rating_queryset)

# # movies = movies.rename(columns={'id': 'movieId'})
# # ratings = ratings.rename(columns={'userid': 'userId', 'movieid': 'movieId'})

# print('The dataset contains: ', len(ratings), ' ratings of ', len(movies), ' movies.')
# print(movies)
# data=movies.iloc[:, 4].values
# print(data)

# cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
# print(cluster.fit_predict(data))

###################################

movie_queryset = Movie.objects.all()
rating_queryset = Rating.objects.all()

# rating_limit = len(rating_queryset) * (rating_percent / 100)
rating_queryset = rating_queryset[:1000]

movies = to_df(movie_queryset)
ratings = to_df(rating_queryset)

movies = movies.rename(columns={'id': 'movieId'})
ratings = ratings.rename(columns={'userid': 'userId', 'movieid': 'movieId'})

print(movies)
# 20 clusters

data=movies.iloc[:, 3:5].values
print(data)

predictions = AgglomerativeClustering(n_clusters=20, affinity='euclidean', linkage='ward')
predictions.fit_predict(data)
# print("predictions")
# print(predictions)

plt.figure(figsize=(10, 7))
plt.scatter(data[:,0], data[:,1], c=predictions.labels_, cmap='rainbow')
# plt.show()
