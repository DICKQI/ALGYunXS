from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login, authCheck, studentCheck, getUser
from apps.helps.models import Article, Category, Tag, HelpsStarRecord
from apps.account.models import User_Info
from apps.log.models import HelpsViewLog
import json


class HelpsInfoView(APIView):

    EXCLUDE_FIELDS = [
        'comment'
    ]

    @check_login
    def get(self, request, pid):
        '''
        获取互帮互助信息详情
        :param request:
        :param pid:
        :return:
        '''
        article = Article.objects.filter(id=pid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '找不到该内容'
            }, status=404)
        article = article[0]
        user = User_Info.objects.get(email__exact=request.session.get('login'))
        if user != article.author:
            if article.status == 's':
                # 未发布的文章非作者无法直接查看
                return JsonResponse({
                    'status': False,
                    'err': '找不到该内容'
                }, status=404)
        if user != article.author:
            manage = False
            article.views += 1
        else:
            manage = True
        if not HelpsStarRecord.objects.filter(
                Q(star_man=user) & Q(article=article)
        ).exists():
            can_star = True
        else:
            can_star = False

        HelpsViewLog.objects.create(
            ip=request.META['REMOTE_ADDR'],
            user=user,
            HelpsArticle=article
        )
        return JsonResponse({
            'status': True,
            'article': model_to_dict(article, exclude=self.EXCLUDE_FIELDS),
            'can_star': can_star, # 是否已对其点赞
            'manage': manage # 是否是管理员
        })

    @check_login
    def put(self, request, pid):
        '''
        修改文章信息
        :param request:
        :param pid:
        :return:
        '''
        article = Article.objects.filter(id=pid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '找不到该内容'
            }, status=404)
        article = article[0]
        if not authCheck(['123', '515400'], request.session.get('login'), article):
            return JsonResponse({
                'status': False,
                'err': '你没有权限'
            }, status=401)
        params = request.body
        json_params = json.loads(params)
        try:
            if json_params.get('title') != None:
                article.title = json_params.get('title')
            if json_params.get('content') != None:
                article.content = json_params.get('content')
            if json_params.get('status') != None:
                article.content = json_params.get('status')
            if json_params.get('category') != None:
                category = Category.objects.filter(cid=json_params.get('category'))
                if not category.exists():
                    return JsonResponse({
                        'status': False,
                        'err': '分类不存在',
                    }, status=404)
                article.category = category
            if json_params.get('tags') != None:
                for tag in json_params.get('tags'):
                    t = Tag.objects.filter(name=tag)
                    if not t.exists():
                        t = Tag.objects.create(name=tag)
                        article.tags.add(t)
                    else:
                        if not article.tags.filter(name=tag).exists():
                            t = t[0]
                            article.tags.add(t)
        except:
            return JsonResponse({
                'status': False,
                'err': '未知错误'
            }, status=403)
        article.save()
        return JsonResponse({
            'status': True,
            'id': article.id
        })

    @check_login
    def delete(self, request, pid):
        '''
        删除文章
        :param request:
        :param pid:
        :return:
        '''
        article = Article.objects.filter(id=pid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '找不到该内容'
            }, status=404)
        article = article[0]
        if not authCheck(['123', '515400'], request.session.get('login'), article):
            return JsonResponse({
                        'status': False,
                        'err': '你没有权限'
                    }, status=401)
        article.delete()
        return JsonResponse({
            'status': True,
            'id': pid
        })

    @check_login
    def post(self, request):
        '''
        新建文章
        :param request:
        :return:
        '''
        user = getUser(request.session.get('login'))
        if not studentCheck(user):
            return JsonResponse({
                'status': False,
                'err': '请完成学生认证'
            }, status=403)
        params = json.loads(request.body)
        try:
            title = params['title']
            content = params['content']
            status = params['status']
            category = params['category']
        except:
            return JsonResponse({
                'status': False,
                'err': '输入错误'
            }, status=403)
        if Article.objects.filter(title=title).exists():
            return JsonResponse({
                'status': False,
                'err': '标题重复'
            }, status=401)
        article = Article.objects.create(
            author=user,
            title=title,
            content=content,
            status=status,
            category=Category.objects.get(cid=category),
        )
        if params.get('tags'):
            for tag_name in params.get('tags'):
                t = Tag.objects.filter(name=tag_name)
                if not t.exists():
                    t = Tag.objects.create(name=tag_name)
                    article.tags.add(t)
                else:
                    t = t[0]
                    article.tags.add(t)
        return JsonResponse({
            'status': True,
            'id': article.id
        })
