from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Rating, Profile, Movie
from api.serializers import RatingSerializer, ProfileSerializer, MovieSerializer
from django.db.models import Avg
from django.db import connection
from django.db import connections
from django.core.exceptions import EmptyResultSet
import requests
import json

# python 라이브러리
import random
import matplotlib.pyplot as plt
import pandas as pd

@api_view(['GET'])
def km_algo(request):

    if request.method == 'GET':
        # ratings_origin = Rating.objects.all()[:10] # 확인용

        # K-Means 시작  --- (여기다가 kmeans의 알고리즘 main을 써나가면 됨)
        rating_limit = int(len(Rating.objects.all()) * (10 / 100))
        inputs = mostview_sql(rating_limit) # rating 리스트 [userid, movieid, rating] 모양
        clus = KMeans(20) # 클러스터의 수

        # print(len(clus.train(inputs))) # 데이터 개수
        kmeans_result = clus.train(inputs)
        # print(kmeans_result)[:100]
        result = list(kmeans_result)
        data = dict()
        for i in range(20):
            data[i]=[]

        for i in range(len(result)):
            data[result[i]].append([result[i],i+1]) #group, userid

        request_data = {'series': []}

        for i in range(20):
            name = 'Group'+str(i+1)
            request_data['series'].append({
                'name':name,
                'data':data[i]
            })
        return Response(status=status.HTTP_200_OK,data=request_data)

        # 그래프 출력

        # print("중심: ", clus.means) # 중심 출력
        # print("클러: ", clus.k)

        # axis_x_mean, axis_y_mean, axis_z_mean = clus.make_praph_data(clus.means)
        # axis_x, axis_y, axis_z = clus.make_praph_data(inputs)

        # plt.scatter(axis_x, axis_y, axis_z)
        # plt.scatter(axis_x_mean, axis_y_mean, axis_z_mean, marker='>', c='r')

        # plt.show()

        # serializer = RatingSerializer(ratings_origin, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)

# rating 데이터 가져오는 함수
def mostview_sql(value):
    cursor = connection.cursor()
    query = "select userid, movieid, rating from api_rating limit " + str(value)
    cursor.execute(query)
    # cursor.execute("select userid, movieid, rating from api_rating limit 100")

    row = cursor.fetchall()
    # return row
    return row

# KMeans 알고리즘
class KMeans:

    # __init__ : 생성자
    # classify : 분류메서드
    # train : 훈련메서드

    def __init__(self, k):
        self.k = k
        self.means = None

    # a와 b의 거리를 구함
    def squared_distance(self, a, b):
        return ( (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2 )

    # 군집간(i_point)의 중앙점을 구함
    def vector_mean(self, i_points):
        sum_x = 0
        sum_y = 0
        sum_z = 0
        for i in list(i_points):
            sum_x += i[0]
            sum_y += i[1]
            sum_z += i[2]

        avg_x = (sum_x / len(i_points))
        avg_y = (sum_y / len(i_points))
        avg_z = (sum_z / len(i_points))
        

        return [avg_x, avg_y, avg_z]

    # 군집을 분류함
    def classify(self, input):
        # range(self.k)에 key를 적용해서 min값을 구함
        return min(range(self.k), key=lambda i: self.squared_distance(input, self.means[i]))

    def train(self, inputs):

        self.means = random.sample(inputs, self.k)
        # self.means = inputs
        # print(self.means)
        assignment = None

        while True:
            new_assignment = list(map(self.classify, inputs))

            if assignment == new_assignment:
                return assignment

            assignment = new_assignment

            for i in range(self.k):
                # i_points = [p for p, a in zip(assignment, inputs) if a == i] # 아래 for와 동일

                for p, a in zip(assignment, inputs):
                    i_points = 0
                    # print("p는 {} , a는 {}".format(p,a))
                    if(a == i):
                        # print("a는 {}, i는 {}".format(a,i))
                        i_points = p
                        # print("아포: ",i_points)
                
                # if i_points:
                #     self.means[i] = self.vector_mean(i_points)


    # 그래프를 그리기 함수
    def make_praph_data(self, data):
        axis_x = list()
        axis_y = list()
        axis_z = list()
        for i in list(data):
            axis_x.append(i[0])
            axis_y.append(i[1])
            axis_z.append(i[2])

        return axis_x, axis_y, axis_z
