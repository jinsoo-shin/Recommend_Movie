from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Rating, Profile,Movie
from api.serializers import RatingSerializer,ProfileSerializer,MovieSerializer
from rest_framework.response import Response
from django.db.models import Avg,Count
# import operator
from operator import itemgetter

from django.db import connection



@api_view(['GET', 'POST', 'DELETE'])
def ratings(request):

    if request.method == 'GET':
        mode = request.GET.get('mode', None)
        movieid = request.GET.get('movieid', None)
        userid = request.GET.get('userid', None)
        ratings = Rating.objects.all()
        if mode == 'user':
            #영화를 본 유저 뽑기
            if movieid:
                result = user_movieid(movieid)
                return Response(data=result, status=status.HTTP_200_OK)
            if userid:
                movieids = ratings.filter(userid__exact=userid)
                serializer = RatingSerializer(movieids, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        if mode=='usermovie':
            #특정 유저가 본 영화 제목 뽑기
            if userid:
                userid= int(userid)
                result = usermovie_sql(userid)
                return Response(data=result, status=status.HTTP_200_OK)
        if mode=='mostview':
            #특정기준으로 많이 본 영화 리스트 뽑기
            profiles = Profile.objects.all()
            select = request.GET.get('select', None)
            where = request.GET.get('where', None)
            result = mostview_sql(select,where)
            return Response(data=result, status=status.HTTP_200_OK)

        else:
            #평점 구하기
            if movieid:
                ratings = ratings.filter(movieid__exact=movieid)
                query_set = ratings.aggregate(Avg('rating'))
                return Response(data=query_set, status=status.HTTP_200_OK)
            #전체 뽑아오기
            else:
                serializer = RatingSerializer(ratings, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)





    if request.method == 'DELETE':
        userid = request.GET.get('userid', None)
        ratings = Rating.objects.all()
        if userid:
            ratings = ratings.filter(userid__icontains=userid)

        ratings.delete()


        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        ratings = request.data.get('ratings', None)
        for cur_rating in ratings:
            userid = cur_rating.get('userid', None)
            userid=Profile.objects.get(id=userid)
            movieid = cur_rating.get('movieid', None)
            rating = cur_rating.get('rating', None)
            date = cur_rating.get('date', None)

            if not (userid and movieid and rating and date):
                continue
            print(userid,movieid,rating,date)
            Rating(userid=userid, movieid=movieid, rating=rating, date=date).save()

        return Response(status=status.HTTP_200_OK)

def user_movieid(value):
    cursor = connection.cursor()
    cursor.execute("SELECT u.username FROM api_rating r,auth_user u WHERE r.movieid = %s and r.userid=u.id  LIMIT 10",[value])

    row = dictfetchall(cursor)
    return row

def usermovie_sql(value):
    cursor = connection.cursor()
    cursor.execute("SELECT m.title FROM api_rating r,api_movie m WHERE r.movieid=m.id and r.userid = %s",[value])

    row = dictfetchall(cursor)
    return row

def mostview_sql(key,value):
    cursor = connection.cursor()
    if not key:
        cursor.execute("select m.title, Count(r.movieid) movie_count from api_rating r, api_profile p, api_movie m Where r.userid = p.id and m.id=r.movieid Group by movieid Order by movie_count DESC")
    if key=='age':
        cursor.execute("select m.title, Count(r.movieid) movie_count from api_rating r, api_profile p, api_movie m Where r.userid = p.id and m.id=r.movieid and p.age = %s Group by movieid Order by movie_count DESC",[value])
    if key == 'occupation':
        cursor.execute(
            "select m.title, Count(r.movieid) movie_count from api_rating r, api_profile p, api_movie m Where r.userid = p.id and m.id=r.movieid and p.occupation = %s Group by movieid Order by movie_count DESC",[value])
    if key=='gender':
        cursor.execute("select m.title, Count(r.movieid) movie_count from api_rating r, api_profile p, api_movie m Where r.userid = p.id and m.id=r.movieid and p.gender = %s Group by movieid Order by movie_count DESC",[value])

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

