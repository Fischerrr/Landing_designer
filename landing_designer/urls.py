from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

urlpatterns = [
    path('admin93745y3294tgnsd98af/', admin.site.urls),
    path('', include('apps.app_auth.urls', namespace='app_auth')),
    path('', include('apps.landing.urls', namespace='landing')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.OVERRIDE_STATIC_URL:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/static/', document_root=settings.STATIC_ROOT)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

if settings.SILK_ENABLED:
    urlpatterns = [path('__silk__/', include('silk.urls', namespace='silk'))] + urlpatterns
