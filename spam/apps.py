from django.apps import AppConfig


class SpamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spam'

    def ready(self):
        from spam import task_schedular
        task_schedular.task_schedular()
