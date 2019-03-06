from apps.account.models import User_Info
from apps.market.models import Commodity
from apps.helps.models import Article
from apps.PTJ.models import PTJInfo
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.check_login import check_login
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json


class UserDashBoardView(APIView):
    ARTICLE_EXCLUDE_FIELDS = [
        'comment', 'create_time'
    ]
    COMMODITY_EXCLUDE_FIELDS = [
        'comment', 'create_time'
    ]

    @check_login
    def get(self, request):
        '''
        用户控制台
        :param request:
        :return:
        '''
        user = User_Info.objects.get(email=request.session.get('login'))
        if user.user_role == '6':
            return JsonResponse({'err': '此账户已被封禁，请联系管理员'}, status=401)
        articles = Article.objects.filter(author=user)
        markets = Commodity.objects.filter(seller=user)
        ptj = PTJInfo.objects.filter(publisher=user)
        artPage = Paginator(articles, 5)
        marPage = Paginator(markets, 5)
        ptjPage = Paginator(ptj, 5)

        apage = request.GET.get('apage')
        mpage = request.GET.get('mpage')
        ppge = request.GET.get('ppage')
        try:
            artList = artPage.page(apage)
        except PageNotAnInteger:
            artList = artPage.page(1)
        except EmptyPage:
            artList = artPage.page(artPage.num_pages)
        try:
            marList = marPage.page(mpage)
        except PageNotAnInteger:
            marList = marPage.page(1)
        except EmptyPage:
            marList = marPage.page(marPage.num_pages)
        try:
            ptjList = ptjPage.page(ppge)
        except PageNotAnInteger:
            ptjList = ptjPage.page(1)
        except EmptyPage:
            ptjList = ptjPage.page(1)
        artResult = [model_to_dict(art, exclude='comment') for art in artList]
        marResult = [model_to_dict(mar, exclude='comment') for mar in marList]
        ptjResult = [model_to_dict(ptjs) for ptjs in ptjList]
        return JsonResponse({
            'status': True,
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

