from django.apps import AppConfig


class AdminusibrasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminUsibras'
    verbose_name = "Livros"

    def ready(self):
        import adminUsibras.signals
