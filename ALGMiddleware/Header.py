from django.utils.deprecation import MiddlewareMixin

class ALGHeader(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = 'https://algyun.cn:83'
        return response