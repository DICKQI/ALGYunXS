from apps.account.models import User_Info, Notifications
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.dictInfo import model_to_dict


class MeView(APIView):

    USER_INCLUDE_FIELDS = [
        'nickname', 'phone_number', 'student_id', 'age',
        'credit_score', 'last_login_time', 'from_school'
    ]




    def get(self, request):
        '''
        获取当前登录用户信息
        :param request:
        :return:
        '''
        if request.session.get('login') != None:
            user = User_Info.objects.get(phone_number__exact=request.session.get('login'))
            userResult = model_to_dict(user, fields=self.USER_INCLUDE_FIELDS)
            if user.head_portrait:
                userResult['head'] = 'https://algyunxs.oss-cn-shenzhen.aliyuncs.com/media/' + str(
                    user.head_portrait) + '?x-oss-process=style/head_portrait'
            else:
                userResult['head'] = None

            '''检查是否有未读通知'''
            notifications = Notifications.objects.filter(aboutUser=user)
            if notifications.exists():
                cnt = 0
                for no in notifications:
                    if no.isRead == False:
                        cnt += 1
                if cnt == 0:
                    return JsonResponse({
                        'status': True,
                        'myself': userResult,
                        'has_notifications':False
                    })
                return JsonResponse({
                    'status': True,
                    'myself': userResult,
                    'has_notifications': True,
                    'count':cnt
                })
            return JsonResponse({
                'status': True,
                'myself': userResult,
                'has_notifications': False
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '你还没登录'
            }, status=401)
