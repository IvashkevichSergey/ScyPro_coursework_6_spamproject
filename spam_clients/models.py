from django.db import models

from users.models import NULLABLE
from users.models import User


class Client(models.Model):
    """Класс для создания модели Клиентов"""
    full_name = models.CharField(max_length=150, verbose_name='имя клиента')
    email = models.EmailField(verbose_name='электронная почта', unique=True)
    created_by = models.ForeignKey(
        User, **NULLABLE, on_delete=models.CASCADE,
        verbose_name='создатель клиента'
    )

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
