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
        # print(params)
        period = params.get("period", None)
        user_id = params.get("user_id",None)
        # print(user_id)
        expiration = datetime

        subscribes = Subscribe.objects.all()

        now = datetime.datetime.now().strftime('%Y-%m-%d')
        print("나우",now)

        #TODO: now랑 구독날짜 비교해서 if문 완성해야함!

        if(period == '1mon'): # 1개월 구독
            # 해당유저의 첫 구독이거나 날짜가 지났으면 아래 실행
            if(check_duplicate(subscribes, user_id) == 0): # 오늘기준으로 날짜 지난거 체크해야함
                expiration = datetime.datetime.now() + datetime.timedelta(days=30)
                expiration = expiration.strftime('%Y-%m-%d')

             # TODO: else추가 -> Get으로 해당유저 이미 db에 있으면 db에있는 기간 + 30일

        # print(expiration)

        Subscribe(user_id=user_id, expiration=str(expiration)).save() # db에 적용

        result={"status":"구독 1개월","만료일":expiration}
        return Response(data=result, status=status.HTTP_200_OK)


def check_duplicate(subscribes, user_id):
    duplicate_id = 0
    for cur in subscribes:
        if(int(user_id) == cur.user_id):
            duplicate_id = int(user_id)
            break
    
    return duplicate_id

    
