from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import create_profile
from api.models import Profile
from api.serializers import ProfileSerializer
from django.contrib.auth.models import User
from django.contrib import auth
from operator import itemgetter
from django.db import connection

@api_view(['POST','GET'])
def signup_many(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        profiles = Profile.objects.all()
        if username:
            # profiles = profiles.filter(user_id="1")
            print(username)
            profiles = profiles.filter(user__username=username)
            print(profiles)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

        # serializer = ProfileSerializer(profiles, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # Login

        # Create Data.
        profiles = request.data.get('profiles', None)
        for profile in profiles:
            username = profile.get('username', None)
            password = profile.get('password', None)
            age = profile.get('age', None)
            occupation = profile.get('occupation', None)
            gender = profile.get('gender', None)

            create_profile(username=username, password=password, age=age,
                           occupation=occupation, gender=gender)

        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        params = request.data.get('params',None)
        username = params['username']
        password = params['password']
        user = auth.authenticate(request, username=username, password=password)
        temp = my_custom_sql('signin',username, '','','','')
        flag = False
        if user is not None :
            auth.login(request, user)
            return Response(data=temp, status=status.HTTP_200_OK)
        else:
            return Response(data=flag, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        username = request.GET.get('username')
        print(username)
        print(id)
        temp = my_custom_sql('delete2','', '','','',id)

        flag = False
        if temp is not None :
            temp = my_custom_sql('delete1',username, '','','','')
            return Response(data=temp, status=status.HTTP_200_OK)
        else:
            return Response(data=flag, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update(request):
    if request.method == 'PUT':
        params = request.data.get('params',None)
        id = params['id']
        age = params['age']
        occupation = params['occupation']
        gender = params['gender']
        print(params)
        temp = update_user(age,gender,occupation,id)

        flag = False
        if temp is not None :
            return Response(data=temp, status=status.HTTP_200_OK)
        else:
            return Response(data=flag, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        params = request.data.get('params',None)
        username = params['username']
        email = params['email']
        pw = params['password']
        fn = params['first_name']
        ln = params['last_name']
        age = params['age']
        occupation = params['occupation']
        gender = params['gender']
        # email = request.data.get('email', None)

        # auth_user
        # user = User.objects.create_user(username=username, password=pw, email=email, first_name=fn,last_name=ln)

        user = create_profile(username=username, password=pw, age=age, occupation=occupation, gender=gender)

        flag = False

        if user is not None:
            flag = True
            print(username, fn, ln, email)
            my_custom_sql('signup', username, fn, ln, email,'')
            return Response(data=flag,status=status.HTTP_201_CREATED)
        else:
            return Response(data=flag,status=status.HTTP_200_OK)

def clean(type):
    cursor = connection.cursor()

    if(type == 'auth_user'):
        cursor.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = %s;", [type])
    if(type == 'api_profile'):
        cursor.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = %s;", [type])
    
    row = dictfetchall(cursor)
    return row
def my_custom_sql(type, username, fn, ln, email, id):
    cursor = connection.cursor()
    
    if type == 'signup':
        cursor.execute("UPDATE auth_user SET first_name=%s, last_name=%s, email=%s WHERE username=%s",[fn,ln,email,username])
    if type == 'signin':
        cursor.execute("select * from auth_user where username=%s", [username])
    if type == 'delete1':
        cursor.execute("Delete from auth_user where username=%s", [username])
        clean('auth_user')
        # auto increase remove.
    if type == 'delete2':
        cursor.execute("Delete from api_profile where id=%s", [id])
        clean('api_profile')

    row = dictfetchall(cursor)
    return row

def update_user(age, gender, occupation, id):
    cursor = connection.cursor()
    
    cursor.execute("UPDATE api_profile SET age=%s, gender=%s, occupation=%s WHERE id=%s",[age,gender,occupation,id])

    row = dictfetchall(cursor)
    return row

def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]
