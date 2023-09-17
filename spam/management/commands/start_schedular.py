from django.core.management import BaseCommand

from spam.services import send_emails


class Command(BaseCommand):
    """Скрипт для единоразового запуска рассылки сообщений"""
    def handle(self, *args, **options):
        send_emails()
