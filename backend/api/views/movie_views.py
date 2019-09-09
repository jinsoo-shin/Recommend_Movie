from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie,Rating
from api.serializers import MovieSerializer
from rest_framework.response import Response
from django.db.models import Avg
from django.db import connection


API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

@api_view(['GET', 'POST', 'DELETE','PUT'])
def movies(request):

    if request.method == 'GET':
        id = request.GET.get('id', request.GET.get('movie_id', None))
        title = request.GET.get('title', None)
        viewcnt = request.GET.get('viewcnt',None)
        rating = request.GET.get('rating',None)
        genres = request.GET.get('select',None)


        movies = Movie.objects.all()
        if id:
            movies = movies.filter(pk=id)
        if title:
            movies = movies.filter(title__icontains=title)
        if genres:
            genres=genres.split(',')
            for genre in genres:
                movies= movies.filter(genres__icontains=genre)
        #     movies = movies.filter(genre__icontains=genre)

        if viewcnt:
            if viewcnt=="asc":
                viewcnt = 'viewCnt'
            elif viewcnt=='desc':
                viewcnt = '-viewCnt'
        if rating:
            if rating=="asc":
                rating = 'rating'
            elif rating=='desc':
                rating = '-rating'
        if viewcnt or rating:
            if viewcnt and rating:
              movies =movies.order_by(viewcnt,rating)
            elif viewcnt:
                movies = movies.order_by(viewcnt)
            elif rating :
                movies = movies.order_by(rating)
        
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        movie = Movie.objects.all()
        movie.delete()
        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        movies = request.data.get('movies', None)
        for movie in movies:
            id = movie.get('id', None)
            title = movie.get('title', None)
            genres = movie.get('genres', None)
            if not (id and title and genres):
                continue
            if Movie.objects.filter(id=id).count() > 0 or Movie.objects.filter(title=title).count() > 0:
                continue

            ratings = Rating.objects.all()
            ratings = ratings.filter(movieid__exact=id)
            query_set = ratings.aggregate(Avg('rating'))
            rating = query_set['rating__avg']
            if not rating:
                rating=0
            if rating:
              rating = round(rating,1)
            Movie(id=id, title=title, genres='|'.join(genres), rating=rating).save()

        return Response(status=status.HTTP_200_OK)

    if request.method == 'PUT':
        movieid = request.GET.get('movieid', None)
        movie = Movie.objects.get(id=movieid)
        movie.viewCnt = movie.viewCnt+ 1
        movie.save()

        return Response(data=movie.viewCnt, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete(request):
    if request.method == 'DELETE':
        movieid = request.GET.get('movieid',None)
        temp = delete_movie(movieid)

        flag = False
        if temp is not None :
            return Response(data=temp, status=status.HTTP_200_OK)
        else:
            return Response(data=flag, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update(request):
    if request.method == 'PUT':
        params = request.data.get('params',None)
        print(params)
        movieid = params['movieid']
        title = params['title']
        viewCnt = params['viewCnt']

        temp = update_movie(title,viewCnt,movieid)

        flag = False
        if temp is not None :
            return Response(data=temp, status=status.HTTP_200_OK)
        else:
            return Response(data=flag, status=status.HTTP_200_OK)

def delete_movie(id):
    cursor = connection.cursor()
    
    cursor.execute("Delete from api_movie WHERE id=%s",[id])

    row = dictfetchall(cursor)
    return row

def update_movie(title, viewCnt, id):
    cursor = connection.cursor()
    
    cursor.execute("UPDATE api_movie SET title=%s, viewCnt=%s WHERE id=%s",[title,viewCnt,id])

    row = dictfetchall(cursor)
    return row

def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]
