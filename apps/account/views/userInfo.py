from apps.account.models import User_Info
from apps.market.models import Commodity
from apps.helps.models import Article
from ALGPackage.dictInfo import model_to_dict
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password


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
            nickname = user.nickname
            age = user.age
            studentID = user.student_id
            score = user.credit_score
            role = user.user_role
            if user.head_portrait:
                head = '/media/' + str(user.head_portrait)
            else:
                head = None
            articles = Article.objects.filter(author=user)
            commodity = Commodity.objects.filter(seller=user)
            return JsonResponse({'result': {
                'nickname': nickname,
                'age': age,
                'studentID': studentID,
                'score': score,
                'role': role,
                'head_portrait': head,
                'article': [model_to_dict(art, exclude=self.ARTICLE_EXCLUDE_FIELDS) for art in articles],
                'commodity': [model_to_dict(crt, exclude=self.COMMODITY_EXCLUDE_FIELDS) for crt in commodity]
            }})
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
                return JsonResponse({'result': {
                    'status': 'success',
                    'id': user.id,
                    'changed': has_change
                }})
            else:
                return JsonResponse({'err': '密码错误'}, status=401)
        else:
            return JsonResponse({'err': '你还未登录呢'}, status=401)
