from rest_framework.views import APIView
from apps.account.models import User_Info, School
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json


class RegisterView(APIView):
    def post(self, request):
        '''注册账户'''
        params = request.body
        jsonParams = json.loads(params)
        try:
            User_Info.objects.get(phone_number__exact=jsonParams['phone_number'])
            return JsonResponse({
                'status':False,
                'err':'手机号已存在'
            }, status=401)
        except:
            try:
                User_Info.objects.get(email__exact=jsonParams['email'])
                return JsonResponse({
                    'status': False,
                    'err': '邮箱已存在'
                }, status=401)
            except:
                try:
                    User_Info.objects.get(nickname__exact=jsonParams['nickname'])
                    return JsonResponse({
                        'status': False,
                        'err': '昵称已被占用，换一个试试看吧'
                    }, status=401)

                except:
                    try:
                        hash_password = make_password(jsonParams.get('password'))
                        school = School.objects.get(abbreviation__exact=jsonParams.get('school'))
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
                            'status':True,
                            'id':newUser.id,
                            'phone_number':newUser.phone_number,
                            'nickname':newUser.nickname,
                        })
                    except:
                        return JsonResponse({
                            'status':False,
                            'err': '出现了预期之外的错误'
                        }, status=403)