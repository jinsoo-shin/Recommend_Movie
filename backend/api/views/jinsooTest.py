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

genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']


def cos_sim(v1, v2):
    x = np.array(v1)
    y = np.array(v2)

    x = x.reshape(1, -1)
    y = y.reshape(1, -1)

    return cosine_similarity(x, y)[0][0]


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


def postPredictions_KMeans(input_cluster_num, rating_percent):
    # DB에 KMeans 결과를 저장하자
    print("postKMeansResult 함수 시작")

    if not input_cluster_num or input_cluster_num > 20:
        input_cluster_num = 20
    movie_queryset = Movie.objects.all()

    rating_limit = int(len(Rating.objects.all()) * (rating_percent / 100))
    rating_queryset = Rating.objects.all()[:rating_limit]

    movies = to_df(movie_queryset)
    ratings = to_df(rating_queryset)

    movies = movies.rename(columns={'id': 'movieId'})
    ratings = ratings.rename(columns={'userid': 'userId', 'movieid': 'movieId'})

    print('The dataset contains: ', len(ratings), ' ratings of ', len(movies), ' movies.')

    #####

    # Merge the two tables then pivot so we have Users X Movies dataframe
    ratings_title = pd.merge(ratings, movies[['movieId', 'title']], on='movieId')

    user_movie_ratings = pd.pivot_table(ratings_title, index='userId', columns='title', values='rating')
    most_rated_movies_1k = helper.get_most_rated_movies(user_movie_ratings, 1000)

    sparse_ratings = csr_matrix(pd.SparseDataFrame(most_rated_movies_1k).to_coo())
    # sparse_ratings = csr_matrix(pd.SparseDataFrame(user_movie_ratings).to_coo())

    # 20 clusters
    # predictions = KMeans(n_clusters=input_cluster_num, algorithm='full').fit_predict(sparse_ratings)
    # predictions = GaussianMixture(n_components=4).fit_predict(sparse_ratings.toarray())
    predictions = AgglomerativeClustering(n_clusters=20, affinity='euclidean', linkage='ward').fit_predict(sparse_ratings.toarray())

    print("predictions")
    print(predictions)
    print(predictions[:100])
    print('predictions len ', len(predictions))

    # 여기서 predictions를 db에 저장하면된다.

    return predictions


def get_predictions():
    # DB 에서 클러스터링 결과 받아오기
    kmeans = KmeansResult.objects.all()
    result = to_df(kmeans).ix[0]['clusterlist']
    result = result.split('|')
    for idx, value in enumerate(result):
        result[idx] = int(value)
    return result


def getUsersByMovieId(movieId):
    # movieId 번 영화를 본 유저들 가져오기
    ratings = Rating.objects.all()
    ratings = ratings.filter(movieid=movieId)

    return ratings.values('userid')  # 영화를 본 유저들 아이디 리스트


def getMovieVector(predictions, cluster_num, movieId):
    # cluster_num : 클러스터 개수
    users = getUsersByMovieId(movieId)  # 이건 보류하자

    movie_vector = []
    for _ in range(cluster_num):
        movie_vector.append(0)

    for user in users:
        id = user.get('userid')
        if id >= len(predictions):
            continue
        cluster = predictions[id]
        movie_vector[cluster] = movie_vector[cluster] + 1  # 각 클러스터에 유저가 몇명인지 개수 세기

    return movie_vector


def getMovieVectorByGenres(movieId):
    movie = Movie.objects.get(id=movieId)
    # print('movie', movie.genres_array)
    vector = []
    for _ in range(len(genres)):
        vector.append(0)

    temp_genres = movie.genres_array
    for idx, target_genre in enumerate(genres):
        for movie_genre in temp_genres:
            if movie_genre == target_genre:
                vector[idx] = 1
                break

    return vector


def get_silmilar_users(userId):
    userId = int(userId) - 1  # 실제로는 0부터 시작이여서
    tempLimit = 10

    users = []  # 취향이 비슷한 유저 그룹
    predictions = get_predictions()  # 각 유저가 어떤 클러스터에 속해있는지 나타냄
    cluster_num = predictions[userId]  # 유저가 어떤 클러스터에 있는지 알아내고
    for idx in range(len(predictions)):
        if predictions[idx] == cluster_num and idx != userId:
            users.append(str(idx + 1))
    users = users[:tempLimit]
    userStr = ",".join(users)
    users = my_sql("user", userStr)
    return users  # users 는 본인을 제외하고 같은 클러스터에 있는 유저들이다. ( 취향이 비슷한 유저들 )


def get_silmilar_movies(movieId):
    tempLimit = 10
    movies = []  # 비슷한 영화들
    # predictions = get_predictions() # 각 유저가 어떤 클러스터에 속해있는지 나타냄

    # movieId 영화의 벡터 ( 해당 영화를 본 유저들의 클러스터 기준으로 가중치 줌 )
    # cluster_num = 20

    # base_movie_vector = getMovieVector(predictions, cluster_num, movieId) # movieId번 영화와 비슷한 영화들
    base_movie_vector = getMovieVectorByGenres(movieId)  # movieId번 영화와 비슷한 영화들

    movies = Movie.objects.all().values('id')  # 모든 영화의 id리스트
    cos_sim_list = []

    for movie in movies:
        movie_id = movie.get('id')
        if movie_id == movieId:
            continue
        cos = cos_sim(base_movie_vector, getMovieVectorByGenres(movie_id))
        cos_sim_list.append((cos, movie_id))

    cos_sim_list = sorted(cos_sim_list, key=lambda element: element[0], reverse=True)  # 유사도 기준으로 정렬

    similar_movies_list = []

    for movie in cos_sim_list[:tempLimit]:
        title = Movie.objects.get(id=movie[1]).title
        similar_movies_list.append(title)

    return similar_movies_list


@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':
        movieid = request.GET.get('movieid', None)
        userid = request.GET.get('userid', None)

        if movieid:
            result = get_silmilar_movies(movieid)
            return Response(data=result, status=status.HTTP_200_OK)
        if userid:
            result = get_silmilar_users(userid)
            return Response(data=result, status=status.HTTP_200_OK)

        print('default return')
        result = get_silmilar_movies(1)
        return Response(data=result, status=status.HTTP_200_OK)

    if request.method == 'POST':
        params = request.data.get('params',None)
        cluster_num = params.get('cluster_num', None)
        rating_percent = params.get('rating_percent', None)

        if not cluster_num:
            cluster_num = 20
        if not rating_percent:
            rating_percent = 10

        result = postPredictions_KMeans(cluster_num, rating_percent)

        data = dict()
        for i in range(cluster_num):
            data[i]=[]

        for i in range(len(result)):
            data[result[i]].append([result[i],i+1]) #group, userid

        request_data = {'series': []}

        # for i in range(cluster_num):
        #     name = 'Group'+str(i+1)
        #     request_data['series'].append({
        #         'name':name,
        #         'data':data[i]
        #     })
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
