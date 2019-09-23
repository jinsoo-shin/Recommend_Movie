from rest_framework import status
from rest_framework.decorators import api_view
from api.models import MoviePoster
from api.serializers import MoviePosterSerializer
from rest_framework.response import Response
from django.db.models import Avg
from django.db import connection


API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

@api_view(['GET'])
def poster(request):

    if request.method == 'GET':
        posterurl = request.GET.get('posterUrl', None)
        
        serializer = MoviePosterSerializer(posterurl, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
