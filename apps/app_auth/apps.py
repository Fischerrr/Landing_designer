from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    name = 'apps.app_auth'
    verbose_name = 'Пользователи'

    def ready(self):
        from . import admin
        from . import events
