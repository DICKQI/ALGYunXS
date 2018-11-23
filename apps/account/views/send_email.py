from rest_framework.views import APIView
from random import Random
from django.core.mail import send_mail
from django.http import JsonResponse
from apps.account.models import User_Info, EmailVerifyRecord
from ALGXS.settings import EMAIL_FROM
class SendView(APIView):
    def random_str(self, randomInt=20):
        ran_str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomInt):
            ran_str += chars[random.randint(0, length)]
        return ran_str
    def get(self, request, send_type):
        '''
        发送激活邮件
        :param request:
        :param send_type: 发送类型
        :return:
        '''
        try:
            if request.session.get('login') != None:
                email_record = EmailVerifyRecord()
                email = User_Info.objects.get(username__exact=request.session.get('login')).email
                code = self.random_str()
                email_record.code = code
                email_record.email = email
                email_record.send_type = send_type
                email_record.save()
                if send_type == 'active':
                    email_title = '注册激活链接'
                    email_body = '请点击下面的链接激活您的邮箱algyun.cn/users/active/{0}'.format(code)
                    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
                    if send_status:
                        return JsonResponse({'result':{
                            'status':'success',
                            'eid':email_record.id
                        }})
                elif send_type == 'forget':
                    email_title = '注册重置密码链接'
                    email_body = '请点击下面的链接重置你的密码algyun.cn/users/reset/{0}'.format(code)
                    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
                    if send_status:
                        return JsonResponse({'result': {
                            'status': 'success',
                            'eid': email_record.id
                        }})
            else:
                return JsonResponse({'err':'你还未登录'})
        except:
            return JsonResponse({'err':'input error'})
