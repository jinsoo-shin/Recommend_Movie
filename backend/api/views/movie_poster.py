from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Poster
from api.serializers import PosterSerializer
from rest_framework.response import Response
from django.db.models import Avg
from django.db import connection


API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

@api_view(['GET','POST','DELETE'])
def Movie_poster(request):

    if request.method == 'GET':
        posters = Poster.objects.all()
        serializer = PosterSerializer(posters, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    if request.method == 'POST':
        movies = request.data.get('movies_posters', None)
        for movie in movies:
            posterurl = movie.get('posterUrl', None)
            id = movie.get('id', None)
            imdbId = movie.get('imdbId',None)
            Poster(id=id,imdbId=imdbId,posterUrl=posterurl).save()

        return Response(status=status.HTTP_200_OK)

    # if request.method == 'DELETE':
    #     posters = MoviePoster.objects.all()
    #     posters.delete()
    #     return Response(status=status.HTTP_200_OK)