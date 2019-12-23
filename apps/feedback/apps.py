from django.apps import AppConfig, apps


class FeedbackConfig(AppConfig):
    name = 'apps.feedback'
    verbose_name = 'Формы'

    def ready(self):
        from . import admin
        from . import events
