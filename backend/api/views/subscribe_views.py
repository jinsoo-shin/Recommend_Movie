from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Subscribe
from api.serializers import SubscribeSerializer
from rest_framework.response import Response
from django.db.models import Avg,Count
from django.db import connection
import datetime

@api_view(['GET', 'POST'])
def subscribe(request):

    if request.method == 'GET':
        subscribes = Subscribe.objects.all()
        # print(subscribes[0].user_id)
        user_id = request.GET.get('user_id', None)

        user_expiration = ""
        for cur in subscribes:
            if(int(user_id) == cur.user_id):
                # print("expiration: ",cur.expiration)
                user_expiration = cur.expiration # 유저 id에 맞는 사람의 expiration(만료일)을 반환
                break

        print(user_expiration)

        return Response(data=user_expiration, status=status.HTTP_200_OK)

    if request.method == 'POST':
        params = request.data.get('params', None)
        period = params.get("period", None)
        user_id = params.get("user_id",None)
        subscribes = Subscribe.objects.all()

        now = datetime.datetime.now().strftime('%Y-%m-%d')
        expiration = now
        # expiration = datetime.datetime.strptime(expiration,'%Y-%m-%d %H:%M:%S.%f')
        db_expiration = my_sql(str(user_id))
        # print("하나아아ㅏ",datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f')-datetime.datetime.now())
        # print(db_expiration[1])
        #TODO: now랑 구독날짜 비교해서 if문 완성해야함!
        if period == '1mon': # 1개월 구독
            # 해당유저의 첫 구독이거나 날짜가 지났으면 아래 실행
            if db_expiration is None or (datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f')<datetime.datetime.now()):
                expiration = datetime.datetime.now() + datetime.timedelta(days=30)
                # expiration = expiration.strftime('%Y-%m-%d')
            else:
                expiration = datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=30)
        if period == '3mon': # 1개월 구독
            # 해당유저의 첫 구독이거나 날짜가 지났으면 아래 실행
            if db_expiration is None or (datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f')<datetime.datetime.now()):
                expiration = datetime.datetime.now() + datetime.timedelta(days=90)
                # expiration = expiration.strftime('%Y-%m-%d')
            else:
                expiration = datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=90)
        
        if period == '1year': # 1개월 구독
            # 해당유저의 첫 구독이거나 날짜가 지났으면 아래 실행
            if db_expiration is None or (datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f')<datetime.datetime.now()):
                expiration = datetime.datetime.now() + datetime.timedelta(days=365)
                # expiration = expiration.strftime('%Y-%m-%d')
            else:
                expiration = datetime.datetime.strptime(db_expiration[1],'%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=365)
        Subscribe(user_id=user_id, expiration=str(expiration)).save() # db에 적용

        result={"status":"구독 1개월","expiration":expiration}
        return Response(data=result, status=status.HTTP_200_OK)


def check_duplicate(subscribes, user_id):
    duplicate_id = 0
    for cur in subscribes:
        if(int(user_id) == cur.user_id):
            duplicate_id = int(user_id)
            break
    
    return duplicate_id

def my_sql(user_id):
    cursor = connection.cursor()
    query = "Select user_id,expiration from api_subscribe where user_id = "+user_id
    cursor.execute(query)
    row = cursor.fetchone()
    return row
