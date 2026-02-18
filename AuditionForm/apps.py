from django.apps import AppConfig


class AuditionformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AuditionForm'

    def ready(self):
        pass
