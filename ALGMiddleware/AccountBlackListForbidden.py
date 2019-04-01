from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from apps.account.models import User_Info

class AccountForbidden(MiddlewareMixin):
    def process_request(self, request):
        try:
            user = User_Info.objects.get(email=request.session.get('login'))
            if user.user_role == '6':
                return JsonResponse({
                    'status': False,
                    'err': '账号已被封禁'
                }, status=401)
            else:
                return None
        except:
            return None
