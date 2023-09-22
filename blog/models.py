from django.core.cache import cache
from django.db import models
from django.utils import timezone

from users.models import NULLABLE


class Blog(models.Model):
    """Класс для создания модели Блога"""
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(
        upload_to='media/', verbose_name='содержимое', **NULLABLE
    )
    views = models.IntegerField(
        default=0, verbose_name='количество просмотров'
    )
    publish_date = models.DateField(
        default=timezone.now, verbose_name='дата публикации'
    )

    def __str__(self):
        return f'Статья на тему "{self.title}"'

    def save(self, *args, **kwargs):
        """Переопределение метода save для очистки кеша блога
        при внесении каких-либо изменений в блог"""
        key = 'blog'
        if cache.get(key):
            cache.delete(key)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Переопределение метода delete для очистки кеша блога
         при удалении какой-либо статьи из блога"""
        key = 'blog'
        if cache.get(key):
            cache.delete(key)
        super(Blog, self).delete()

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
