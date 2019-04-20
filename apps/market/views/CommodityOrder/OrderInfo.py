from apps.market.models import Commodity, CommodityOrder
from apps.account.models import User_Info, OrderNotification
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from django.core.mail import send_mail
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login, getUser, studentCheck
from datetime import datetime as da
from datetime import timedelta
import json
from ALGXS.settings import EMAIL_FROM



class OrderView(APIView):

    @check_login
    def post(self, request, cid):
        '''
        创建新订单(下单)
        :param request:
        :param cid:
        :return:
        '''
        try:
            user = getUser(email=request.session.get('login'))
            if not studentCheck(user):
                return JsonResponse({
                    'status': False,
                    'err': '你还未进行学生认证，请前往学生认证后再下单'
                })
            commodity = Commodity.objects.filter(id=cid)
            if not commodity.exists():
                return JsonResponse({
                    'err': '商品不存在',
                    'status': False
                }, status=404)
            commodity = commodity[0]
            if commodity.status == 'o':
                return JsonResponse({
                    'status': False,
                    'err': '商品已售出'
                }, status=401)

            if commodity.seller == user:
                return JsonResponse({
                    'status': False,
                    'err': '不能购买自己的商品'
                }, status=401)
            params = json.loads(request.body)
            try:
                address = params.get('address')
                time = params.get('time')
            except:
                return JsonResponse({
                    'err': '输入错误',
                    'status': False
                }, status=403)
            # 新建订单
            orderID = self.generateID()
            '''创建一个"未确认"订单'''
            order = CommodityOrder.objects.create(
                id=orderID,
                commodity=commodity,
                buyer=user,
                address=address,
                unConfirmDeadline=da.now() + timedelta(minutes=time)
            )
            # 商品状态修改
            commodity.status = 'o'
            commodity.save()
            # 通知商品所有者
            '''站内通知'''
            OrderNotification.send(user, order, commodity)
            '''邮件通知'''

            email_title = '您的商品被下单啦，请尽快处理噢'
            email_body = '您的商品已被下单，请尽快处理，感谢您使用ALGYun智慧校园~'
            send_mail(email_title, email_body, EMAIL_FROM, [request.session.get('login')])
            return JsonResponse({
                'status': True,
                'id': order.id
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)

    @check_login
    def delete(self, request, cid, ocid):
        '''
        取消订单（未确认情况下）
        :param request:
        :param cid:
        :param ocid:
        :return:
        '''
        try:
            order = self.getOrder(cid, ocid)
            if not isinstance(order, CommodityOrder) or order.status == '未确认':
                return JsonResponse({
                    'status': False,
                    'err': '订单未找到'
                }, status=404)

            commodity = order.commodity
            user = User_Info.objects.get(email=request.session.get('login'))
            if user != commodity.seller or user != order.buyer:
                if not user.user_role in ['12', '515400']:
                    return JsonResponse({
                        'status': False,
                        'err': '你没有权限'
                    }, status=401)
            order.delete()
            commodity.status = 'p'
            return JsonResponse({
                'status': True,
                'cid': cid,
                'ocid': ocid
            })

        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)

    @check_login
    def put(self, request, cid, ocid):
        '''
        订单完成（购买人）
        :param request:
        :param cid:
        :param ocid:
        :return:
        '''
        try:
            order = self.getOrder(cid, ocid)
            if not isinstance(order, CommodityOrder):
                return JsonResponse({
                    'status': False,
                    'err': '订单未找到'
                }, status=404)

            user = getUser(email=request.session.get('login'))
            if order.status == '已完成':
                return JsonResponse({
                    'status': False,
                    'err': '订单已完成，请勿重复操作'
                }, status=401)
            if user == order.buyer:
                order.status = '已完成'
                order.end_time = da.now()
                order.save()
                return JsonResponse({
                    'status': True,
                    'id': order.id
                })
            else:
                return JsonResponse({
                    'status': False,
                    'err': '你不可以进行此操作'
                }, status=401)

        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)

    @check_login
    def get(self, request, cid, ocid):
        '''
        查看订单信息
        :param request:
        :param cid:
        :param ocid:
        :return:
        '''
        order = self.getOrder(cid, ocid)
        if not isinstance(order, CommodityOrder):
            return JsonResponse({
                'status': False,
                'err': '订单未找到'
            }, status=404)
        user =  getUser(request.session.get('login'))
        if user != order.commodity.seller or user != order.buyer:
            if user.user_role not in ['515400', '12']:
                return JsonResponse({
                    'err': '你没有权限查看',
                    'status': False
                }, status=401)
        return JsonResponse({
            'status': True,
            'order': model_to_dict(order)
        })

    def generateID(self):
        '''
        生成订单号
        :return:
        '''
        year, month, day = da.now().year, da.now().month, da.now().day
        datetime = str(year) + str(month) + str(day)
        oldOrder = CommodityOrder.objects.first()
        oldTime = str(oldOrder.id)[:len(str(oldOrder.id)) - 4]
        if oldTime == datetime:
            newID = str(int(str(oldOrder.id)[-4:]) + 1)
        else:
            newID = '0000'
        for i in range(4 - len(newID)):
            newID = '0' + newID
        orderID = datetime + newID
        return orderID

    def getOrder(self, cid, ocid):
        '''
        获取订单
        :param cid:
        :param ocid:
        :return:
        '''
        commodity = Commodity.objects.filter(id=cid)
        if not commodity.exists():
            return False
        commodity = commodity[0]
        order = CommodityOrder.objects.filter(
            Q(id=ocid) & Q(commodity=commodity)
        )
        if not order.exists():
            return False
        return order[0]