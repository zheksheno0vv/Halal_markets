from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seller'

    def ready(self):
       from seller import signals  # Инициализация сигналов

