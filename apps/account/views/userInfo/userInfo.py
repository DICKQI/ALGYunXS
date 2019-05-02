from apps.account.models import User_Info
from apps.market.models import Commodity
from apps.helps.models import Article
from apps.PTJ.models import PTJInfo
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login, getUser
from ALGCommon.paginator import paginator
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import json


class UserDashBoardView(APIView):
    ARTICLE_EXCLUDE_FIELDS = [
        'comment', 'create_time'
    ]
    COMMODITY_EXCLUDE_FIELDS = [
        'comment', 'create_time', 'last_mod_time', 'status', 'c_detail', 'commodity_img'
    ]

    @check_login
    def get(self, request, uid=0):
        '''
        用户控制台
        :param request:
        :return:
        '''
        if uid == 0:
            user = User_Info.objects.get(email=request.session.get('login'))
        else:
            user = User_Info.objects.filter(id=uid)
            if not user.exists():
                return JsonResponse({
                    'status': False,
                    'err': '用户不存在'
                }, status=404)
            user = user[0]
        articles = Article.objects.filter(author=user)
        markets = Commodity.objects.filter(seller=user)
        ptj = PTJInfo.objects.filter(publisher=user)

        apage = request.GET.get('apage')
        mpage = request.GET.get('mpage')
        ppge = request.GET.get('ppage')
        artList = paginator(articles, apage)
        marList = paginator(markets, mpage)
        ptjList = paginator(ptj, ppge)
        artResult = [model_to_dict(art, exclude='comment') for art in artList]
        marResult = [model_to_dict(mar, exclude='comment') for mar in marList]
        ptjResult = [model_to_dict(ptjs) for ptjs in ptjList]

        i = 0
        for com in marResult:
            if marList[i].commodity_img.first():
                com['commodity_img'] = 'https://algyunxs.oss-cn-shenzhen.aliyuncs.com/media/' + marList[
                    i].commodity_img.first().img.name + '?x-oss-process=style/head_portrait'
            else:
                com['commodity_img'] = None
            i += 1

        return JsonResponse({
            'status': True,
            'myself': True if getUser(request.session.get('login')).id == user.id else False,
            'article': artResult,
            'commodity': marResult,
            'PTJ': ptjResult,
            'A_has_previous': artList.has_previous(),
            'A_has_next': artList.has_next(),
            'M_has_previous': marList.has_previous(),
            'M_has_next': marList.has_next(),
            'P_has_previous': ptjList.has_previous(),
            'P_has_next': ptjList.has_next()
        })

    @check_login
    def put(self, request):
        '''
        用户修改信息
        :param request:
        :return:
        '''
        user = User_Info.objects.get(email=request.session.get('login'))
        if user.user_role == '6':
            return JsonResponse({
                'status': False,
                'err': '此账户已被封禁，请联系管理员'
            })
        params = request.body
        jsonParams = json.loads(params)
        if jsonParams.get('password') == None:
            return JsonResponse({
                'status': False,
                'err': '请输入密码'
            })
        if check_password(jsonParams.get('password'), user.password):
            has_change = {}
            if jsonParams.get('nickname') != None:
                user.nickname = jsonParams.get('nickname')
                has_change['nickname'] = jsonParams.get('nickname')
            if jsonParams.get('age') != None:
                user.age = jsonParams.get('age')
                has_change['age'] = jsonParams.get('age')
            if request.FILES.get('head_img') != None:
                user.head_portrait = request.FILES.get('head_img')
                has_change['head_portrait'] = 'change'
            if jsonParams.get('email') != None:
                if  User_Info.objects.filter(email=jsonParams.get('email')).exists():
                    return JsonResponse({
                        'status': False,
                        'err': '邮箱已存在'
                    }, status=401)
                user.email = jsonParams.get('email')
                user.user_role = '5' # 将邮箱设置为未验证状态
                has_change['email'] = jsonParams.get('email')
            user.save()
            return JsonResponse({
                'status': True,
                'id': user.id,
                'changed': has_change
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '密码错误'
            }, status=401)

