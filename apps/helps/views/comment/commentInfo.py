from apps.helps.models import Article, AComment
from apps.account.models import User_Info
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userCheck import check_login
from ALGCommon.dictInfo import model_to_dict
import json


class CommentInfoView(APIView):

    @check_login
    def post(self, request, aid):
        '''
        新增评论
        :param request:
        :param aid:
        :return:
        '''
        article = Article.objects.filter(id=aid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '未找到该文章'
            }, status=404)
        article = article[0]
        params = json.loads(request.body)
        user = User_Info.objects.get(email=request.session.get("login"))
        try:
            comment = AComment.objects.create(
                from_author=user,
                content=params.get('content')
            )
            article.comment.add(comment)
            return JsonResponse({
                'status': True,
                'id': comment.id
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '新增失败'
            }, status=403)

    @check_login
    def delete(self, request, aid, cid):
        '''
        删除文章评论
        :param request:
        :param aid:
        :param cid:
        :return:
        '''
        article = Article.objects.filter(id=aid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '未找到该文章'
            }, status=404)
        article = article[0]
        comment = AComment.objects.filter(
            Q(id=cid) & Q(article=article)
        )
        if not comment.exists():
            return JsonResponse({
                'status': False,
                'err': '找不到该评论'
            }, status=404)
        comment = comment[0]
        user = User_Info.objects.get(email=request.session.get("login"))
        if comment.from_author != user:
            # 是否是评论来源人
            if user.user_role == '515400' or user.user_role == '123':
                # 是否是总管理员或者helps管理员
                comment.content = '评论已被封禁'
                comment.save()
                return JsonResponse({
                    'status': True,
                    'id': cid
                })
            else:
                return JsonResponse({
                    'status': False,
                    'err': '你没有权限操作'
                }, status=401)
        comment.delete()
        return JsonResponse({
            'status': True,
            'id': cid
        })

    @check_login
    def get(self, request, aid):
        '''
        获取文章所有的评论
        :param request:
        :param aid:
        :return:
        '''
        article = Article.objects.filter(id=aid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '文章不存在'
            }, status=404)
        article = article[0]
        result = []
        user = User_Info.objects.get(email=request.session.get('login'))
        comments = article.comment.all()
        i = 0
        for comment in comments:
            result.append(model_to_dict(comment))
            if comment.from_author == user:
                result[i]['manage'] = True
            else:
                result[i]['manage'] = False
            if comment.from_author.user_role == '515400' or comment.from_author.user_role  == '123':
                result[i]['admin'] = True
            else:
                result[i]['admin'] = False
            i += 1
        return JsonResponse({
            'status': True,
            'comment': result
        })

