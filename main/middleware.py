from django.utils.deprecation import MiddlewareMixin
from main.models import AllowedOrigin

class CorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        origin = request.META.get('HTTP_ORIGIN')
        
        if origin:
            allowed_origins = AllowedOrigin.objects.values_list('domain', flat=True)
            if origin in allowed_origins:
                response['Access-Control-Allow-Origin'] = origin
        
        return response
