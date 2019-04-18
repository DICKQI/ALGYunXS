from apps.market.models import Commodity, CComment, CStarRecord
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userCheck import check_login, getUser
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.paginator import paginator
import json


class CommentInfoView(APIView):

    @check_login
    def get(self, request, cid):
        '''
        获取商品评论列表
        :param request:
        :param cid:
        :return:
        '''
        try:
            commodity = Commodity.objects.filter(id=cid)
            if not commodity.exists():
                return JsonResponse({
                    'err': '商品不存在',
                    'status': False
                }, status=404)
            commodity = commodity[0]
            user = getUser(request.session.get('login'))
            result = []
            comments = commodity.comment.all()
            commentList = paginator(comments, request.GET.get('page'))
            i = 0
            for comment in commentList:
                result.append(model_to_dict(comment))
                if comment.fromUser == user:
                    result[i]['manage'] = True
                else:
                    result[i]['manage'] = False
                if user.user_role == '515400' or user.user_role == '12':
                    result[i]['admin'] = True
                else:
                    result[i]['admin'] = False
                if CStarRecord.objects.filter(
                    Q(comment=comment) & Q(star_man=user)
                ).exists():
                    result[i]['stared'] = True
                else:
                    result[i]['stared'] = False
                i += 1
            return JsonResponse({
                'status': True,
                'comment': result,
                'has_previous': commentList.has_previous(),
                'has_next': commentList.has_next()
            })
        except:
            return JsonResponse({
                'err': '出现未知错误',
                'status': False
            }, status=403)

    @check_login
    def post(self, request, cid):
        '''
        新增评论
        :param request:
        :param cid:
        :return:
        '''
        commodity = Commodity.objects.filter(id=cid)
        if not commodity.exists():
            return JsonResponse({
                'err': '商品不存在',
                'status': False
            }, status=404)
        params = json.loads(request.body)
        commodity = commodity[0]
        user = getUser(request.session.get('login'))
        try:
            content = params.get('content')
        except:
            return JsonResponse({
                'err': '输入错误',
                'status': False
            }, status=403)
        comment = CComment.objects.create(
            fromUser=user,
            content=content
        )
        commodity.comment.add(comment)
        return JsonResponse({
            'status': True,
            'id': comment.id
        })

    @check_login
    def delete(self, request, cid, ccid):
        '''
        删除(禁用)商品评论
        :param request:
        :param cid:
        :param ccid:
        :return:
        '''
        commodity = Commodity.objects.filter(id=cid)
        if not commodity.exists():
            return JsonResponse({
                'err': '商品不存在',
                'status': False
            }, status=404)
        commodity = commodity[0]
        comment = CComment.objects.filter(
            Q(id=ccid) & Q(commodity=commodity)
        )
        if not comment.exists():
            return JsonResponse({
                'status': False,
                'err': '评论不存在'
            }, status=404)
        comment = comment[0]
        user = getUser(request.session.get('login'))
        if comment.fromUser != user:
            if user.user_role in ['515400', '12']: # 管理员操作
                comment.content = '评论已被封禁'
                comment.save()
                return JsonResponse({
                    'status': True,
                    'id': ccid
                })
            else:
                # 非评论归属人
                return JsonResponse({
                    'status': False,
                    'err': '你没有权限操作'
                }, status=401)
        comment.delete()
        return JsonResponse({
            'status': True,
            'id': ccid
        })
