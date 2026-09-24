from django.apps import AppConfig


class AppsConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals
