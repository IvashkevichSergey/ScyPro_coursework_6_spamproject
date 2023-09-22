import random
from typing import Optional

from django.views.generic import ListView, DetailView

from blog.models import Blog
from blog.services import cache_blog
from spam.models import Spam
from spam_clients.models import Client


class BlogListView(ListView):
    """Контроллер для вывода списка статей на главную страницу сайта"""
    model = Blog

    def get_context_data(self, **kwargs) -> dict[str, str]:
        """Добавляем дополнительный контекст к шаблону"""
        context_data = super().get_context_data(**kwargs)
        # Добавляем к контексту список всех рассылок
        context_data['spam'] = Spam.objects.all()
        # Добавляем к контексту список активных рассылок
        context_data['spam_active'] = Spam.objects.filter(status='started')
        # Добавляем к контексту список всех уникальных клиентов
        context_data['spam_clients'] = Client.objects.distinct()
        return context_data

    def get_queryset(self) -> list[Blog]:
        """Выбираем рандомные статьи (не более 3-х) из модели Blog"""
        # queryset = super().get_queryset()
        queryset = cache_blog()
        queryset = random.sample(list(queryset), min(len(queryset), 3))
        return queryset


class BlogDetailView(DetailView):
    """Контроллер для просмотра отдельной статьи"""
    model = Blog

    def get_object(self, queryset=None) -> Optional[Blog]:
        """Увеличиваем счётчик просмотров для просматриваемой статьи"""
        self.obj = super().get_object(cache_blog())
        self.obj.views += 1
        self.obj.save()
        return super(BlogDetailView, self).get_object()
