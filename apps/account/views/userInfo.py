from apps.account.models import User_Info
from apps.market.models import Commodity
from apps.helps.models import Article
from ALGPackage.dictInfo import model_to_dict
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class UserDashBoardView(APIView):
    ARTICLE_EXCLUDE_FIELDS = [
        'comment', 'create_time'
    ]
    COMMODITY_EXCLUDE_FIELDS = [
        'comment', 'create_time'
    ]
    def get(self, request):
        '''
        用户控制台
        :param request:
        :return:
        '''
        if request.session.get('login') != None:
            user = User_Info.objects.get(username__exact=request.session.get('login'))
            if user.user_role == '6':
                return JsonResponse({'err': '此账户已被封禁，请联系管理员'}, status=401)
            articles = Article.objects.filter(author=user)
            markets = Commodity.objects.filter(seller=user)
            artPage = Paginator(articles, 5)
            marPage = Paginator(markets, 5)

            apage = request.GET.get('apage')
            mpage = request.GET.get('mpage')
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
            artResult = [model_to_dict(art, exclude='comment') for art in artList]
            marResult = [model_to_dict(mar, exclude='comment') for mar in marList]
            return JsonResponse({
                'article': artResult,
                'commodity': marResult,
                'A_has_previous': artList.has_previous(),
                'A_has_next': artList.has_next(),
                'M_has_previous': marList.has_previous(),
                'M_has_next': marList.has_next()
            })
        else:
            return JsonResponse({'err': '你还未登录呢'}, status=401)

    def put(self, request):
        '''
        用户修改信息
        :param request:
        :return:
        '''
        if request.session.get('login') != None:
            user = User_Info.objects.get(username__exact=request.session.get('login'))
            if user.user_role == '6':
                return JsonResponse({'err': '此账户已被封禁，请联系管理员'})
            params = request.POST
            if params.get('password') == None:
                return JsonResponse({'err': '请输入密码'})
            if check_password(params.get('password'), user.password):
                has_change = {}
                if params.get('nickname') != None:
                    user.nickname = params.get('nickname')
                    has_change['nickname'] = params.get('nickname')
                if params.get('age') != None:
                    user.age = params.get('age')
                    has_change['age'] = params.get('age')
                if params.get('studentID') != None:
                    user.student_id = params.get('studentID')
                    has_change['studentID'] = params.get('studentID')
                if request.FILES.get('head_img') != None:
                    user.head_portrait = request.FILES.get('head_img')
                    has_change['head_portrait'] = 'change'
                if params.get('phone_number') != None:
                    user.phone_number = params.get('phone_number')
                    has_change['phone_number'] = params.get('phone_number')
                if params.get('email') != None:
                    try:
                        User_Info.objects.get(email=params.get('email'))
                        return JsonResponse({'err': '邮箱已存在'}, status=401)
                    except:
                        user.email = params.get('email')
                        has_change['email'] = params.get('email')
                user.save()
                return JsonResponse({
                    'id': user.id,
                    'changed': has_change
                })
            else:
                return JsonResponse({'err': '密码错误'}, status=401)
        else:
            return JsonResponse({'err': '你还未登录呢'}, status=401)