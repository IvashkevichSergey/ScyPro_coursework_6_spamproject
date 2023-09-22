from django.db import models

from users.models import User, NULLABLE


class Message(models.Model):
    """Класс для создания модели Сообщений"""
    subject = models.CharField(max_length=50, verbose_name='тема сообщения')
    body = models.TextField(verbose_name='тело сообщения')
    created_by = models.ForeignKey(
        User, **NULLABLE, on_delete=models.CASCADE,
        verbose_name='автор сообщения')

    def __str__(self):
        return f'Сообщение на тему "{self.subject}"'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
