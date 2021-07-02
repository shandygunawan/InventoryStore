from django.apps import AppConfig


class IgogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'igog'

    def ready(self):
        import igog.signals
