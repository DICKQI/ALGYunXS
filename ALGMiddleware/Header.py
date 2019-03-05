from django.utils.deprecation import MiddlewareMixin

class ALGHeader(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '127.0.0.1:8080'
        return response