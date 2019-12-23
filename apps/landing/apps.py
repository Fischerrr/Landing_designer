from django.apps import AppConfig


class LandingConfig(AppConfig):
    name = 'apps.landing'
    verbose_name = 'Лендинг'

    def ready(self):
        from . import admin
        from . import events
