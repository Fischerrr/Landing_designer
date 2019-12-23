from django.http import Http404
from django.utils.deprecation import MiddlewareMixin

from apps.landing.models import Landing


class CacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # не даем браузеру закешировать ответ от сервера при аякс запросе
        if request and request.is_ajax():
            response['Cache-Control'] = 'no-store'
        return response


# class SubdomainsMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         domain = request.META.get('HTTP_HOST')
#         subdomain = ".".join(domain.split('.')[:-2])
#         if subdomain:
#             try:
#                 Landing.objects.get(slug=subdomain)
#                 request.subdomain = subdomain
#             except Landing.DoesNotExist:
#                 raise Http404
#         else:
#             try:
#                 landing = Landing.objects.get(alt_url_site__contains=domain)
#                 request.subdomain = landing.slug
#             except Landing.DoesNotExist:
#                 raise Http404


