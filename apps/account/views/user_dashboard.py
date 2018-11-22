from apps.account.models import User_Info
from apps.market.models import Commodity
from apps.helps.models import Article
from ALGPackage.dictInfo import model_to_dict
from rest_framework.views import APIView
from django.http import JsonResponse


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
            nickname = user.nickname
            age = user.age
            studentID = user.student_id
            score = user.credit_score
            articles = Article.objects.filter(author=user)
            commodity = Commodity.objects.filter(seller=user)
            return JsonResponse({'result': {
                'nickname': nickname,
                'age': age,
                'studentID': studentID,
                'score': score,
                'article': [model_to_dict(art, exclude=self.ARTICLE_EXCLUDE_FIELDS) for art in articles],
                'commodity': [model_to_dict(crt, exclude=self.COMMODITY_EXCLUDE_FIELDS) for crt in commodity]
            }})
        else:
            return JsonResponse({'err': '你还未登录呢'})
