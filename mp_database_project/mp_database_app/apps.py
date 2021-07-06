from django.apps import AppConfig


class MpDatabaseAppConfig(AppConfig):
    name = 'mp_database_app'

    def ready(self):
        import mp_database_app.signals
