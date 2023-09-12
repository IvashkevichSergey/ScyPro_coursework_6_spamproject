from django.db import models
from django.utils import timezone

from users.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='media/', verbose_name='содержимое', **NULLABLE)
    views = models.IntegerField(default=0, verbose_name='количество просмотров')
    publish_date = models.DateField(default=timezone.now, verbose_name='дата публикации')

    def __str__(self):
        return f'Статья на тему "{self.title}"'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
