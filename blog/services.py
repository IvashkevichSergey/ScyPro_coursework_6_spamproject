from django.core.cache import cache
from django.db.models import QuerySet

from blog.models import Blog
from config import settings


def cache_blog() -> QuerySet[Blog]:
    """Сервисная функция для кеширования получаемых данных
    из БД по модели Блог"""
    if settings.ALLOW_CACHE:
        key = 'blog'
        articles = cache.get(key)
        if articles is None:
            articles = Blog.objects.all()
            cache.set(key, articles)
        return articles
    return Blog.objects.all()
