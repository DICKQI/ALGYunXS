from django.http import JsonResponse
from apps.account.models import User_Info
from apps.helps.models import Article
from apps.market.models import Commodity
from apps.PTJ.models import PTJInfo


def check_login(func):
    '''
    用于检查用户是否登录的装饰器
    :param func:
    :return:
    '''

    def wrapper(self, request, *args, **kwargs):
        if request.session.get('login') != None:
            user = getUser(request.session.get('login'))
            '''检测是否为黑名单用户，黑名单用户限制一切功能'''
            if user.user_role == '6':
                return JsonResponse({
                    'err': '账号已被封禁，请联系管理员',
                    'status': False
                }, status=401)
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)

    return wrapper


def authCheck(role, email, obj=None):
    '''
    通用权限检测
    :param role:
    :param user:
    :return:
    '''
    user = User_Info.objects.get(email=email)
    if isinstance(obj, Article):
        print(1)
        if obj.author == user:
            return True
    elif isinstance(obj, Commodity):
        if obj.seller == user:
            return True
    elif isinstance(obj, PTJInfo):
        if obj.publisher == user:
            return True

    if isinstance(role, list):
        if user.user_role in role:
            return True
        else:
            return False
    elif isinstance(role, str):
        if user.user_role == role:
            return True
        else:
            return False
    else:
        return False


def getUser(email):
    return User_Info.objects.get(email=email)


def studentCheck(user):
    if user.user_role != '515400':
        if user.student_id == 0:
            return False
    return True
