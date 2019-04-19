from rest_framework.views import APIView
from apps.account.models import User_Info, School
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import random
import json


class RegisterView(APIView):
    def post(self, request):
        '''注册账户'''
        params = request.body
        jsonParams = json.loads(params)
        user = User_Info.objects.filter(email__exact=jsonParams.get('email'))
        if user.exists():
            return JsonResponse({
                'status': False,
                'err': '邮箱已经被注册'
            }, status=401)
        user = User_Info.objects.filter(nickname__exact=jsonParams.get('nickname'))
        if user.exists():
            return JsonResponse({
                'status': False,
                'err': '昵称已经被人抢先用啦'
            }, status=401)

        hash_password = make_password(jsonParams.get('password'))
        school = School.objects.filter(abbreviation__exact=str(jsonParams.get('school')).upper())
        if not school.exists():
            return JsonResponse({
                'status': False,
                'err': '学校不存在'
            }, status=401)
        school = school[0]
        newid = self.randomID()
        newUser = User_Info.objects.create(
            id=newid,
            password=hash_password,
            email=jsonParams.get('email'),
            nickname=jsonParams.get('nickname'),
            from_school=school
        )
        school.user_number += 1
        school.save()

        return JsonResponse({
            'status': True,
            'id': newUser.id,
            'email': newUser.email,
            'nickname': newUser.nickname,
        })

    def randomID(self):
        '''
        生成随机不重复的id
        :return:
        '''
        newid = random.randint(10000000, 999999999)
        while User_Info.objects.filter(id=newid).exists():
            newid = random.randint(10000000, 999999999)
        return newid
