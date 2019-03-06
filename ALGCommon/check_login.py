from django.http import JsonResponse
def check_login(func):
    '''
    用于检查用户是否登录的装饰器
    :param func:
    :return:
    '''
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('login') != None:
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)
    return wrapper