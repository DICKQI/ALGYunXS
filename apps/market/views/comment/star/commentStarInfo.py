from apps.market.models import Commodity, CComment, CStarRecord
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userCheck import check_login, getUser


class CommentStarView(APIView):

    @check_login
    def get(self, request, cid, ccid):
        '''
        给评论点赞
        :param request:
        :param cid:
        :param ccid:
        :return:
        '''
        try:
            comment = self.getComment(cid, ccid)
            if not isinstance(comment, CComment):
                return JsonResponse({
                    'status': False,
                    'err': '未找到该评论'
                }, status=404)
            user = getUser(request.session.get('login'))
            if CStarRecord.objects.filter(
                    Q(star_man=user) & Q(comment=comment)
            ).exists():
                return JsonResponse({
                    'status': False,
                    'err': '已经点过赞了'
                }, status=401)
            CStarRecord.objects.create(
                star_man=user,
                comment=comment
            )
            comment.star += 1
            comment.save()
            return JsonResponse({
                'status': True,
                'id': ccid
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)

    @check_login
    def delete(self, request, cid, ccid):
        '''
        取消赞
        :param request:
        :param cid:
        :param ccid:
        :return:
        '''
        try:
            comment = self.getComment(cid, ccid)
            if not isinstance(comment, CComment):
                return JsonResponse({
                    'status': False,
                    'err': '未找到该评论'
                }, status=404)
            user = getUser(request.session.get('login'))
            record = CStarRecord.objects.filter(
                Q(star_man=user) & Q(comment=comment)
            )
            if not record.exists():
                return JsonResponse({
                    'status': False,
                    'err': '你还没点赞呢'
                }, status=401)
            record[0].delete()
            comment.star -= 1
            comment.save()
            return JsonResponse({
                'status': True,
                'id': ccid
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)

    def getComment(self, cid, ccid):
        '''
        获取评论实例
        :param cid:
        :param ccid:
        :return:
        '''
        commodity = Commodity.objects.filter(id=cid)
        if not commodity.exists():
            return False
        comment = CComment.objects.filter(
            Q(commodity=commodity[0]) & Q(id=ccid)
        )
        if not comment.exists():
            return False
        return comment[0]
