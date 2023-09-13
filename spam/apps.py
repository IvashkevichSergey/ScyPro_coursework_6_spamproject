from django.apps import AppConfig


class SpamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spam'

    def ready(self):
        """Функция, отвечающая за запуск кронтаба при запуске программы"""
        from spam import services
        services.task_schedular()
