from rest_framework.views import APIView
from apps.account.models import User_Info, School
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from random import Random
import json


class RegisterView(APIView):
    def post(self, request):
        '''注册账户'''
        params = request.body
        jsonParams = json.loads(params)
        user = User_Info.objects.filter(phone_number__exact=jsonParams.get('phone_number'))
        if user.exists():
            return JsonResponse({
                'status': False,
                'err': '手机号已经被注册'
            }, status=401)
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
        school = School.objects.get(abbreviation__exact=str(jsonParams.get('school')).upper())
        newUser = User_Info.objects.create(
            phone_number=jsonParams.get('phone_number'),
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
            'phone_number': newUser.phone_number,
            'nickname': newUser.nickname,
        })

