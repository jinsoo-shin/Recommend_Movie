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



@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':
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
