from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from spam_clients.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка клинетов"""
    model = Client

    def get_queryset(self) -> QuerySet[Client]:
        """Передаём в шаблон либо всех клиентов, если пользователь
        имеет права Менеджера, либо только клиентов,
        созданных текущим пользователем"""
        queryset = super().get_queryset()
        if not self.request.user.has_perm('spam_clients.view_client'):
            queryset = queryset.filter(created_by=self.request.user)
        return queryset


class ClientDetailView(UserPassesTestMixin, DetailView):
    """Контроллер для отображения детальной информации по клиентам"""
    model = Client

    def test_func(self) -> bool:
        """Доступ к детальной информации по клиенту имеет либо пользователь,
        добавивший на сайт клиента, либо модератор
        с соответствующими правами"""
        return \
            self.get_object().created_by == self.request.user \
            or self.request.user.has_perm('spam_clients.view_client')


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для страницы создания нового клиента"""
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('client:list')

    def form_valid(self, form) -> HttpResponseRedirect:
        """Если форма валидна - заполняем поле автора
        клиента текущим пользователем"""
        if form.is_valid():
            client = form.save()
            client.created_by = self.request.user
            client.save()
        return super().form_valid(form)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    """Контроллер для страницы изменения информации о клиенте"""
    model = Client
    fields = ('full_name', 'email')

    def get_success_url(self):
        """Возвращает url страницы для перенаправления
        при успешном заполнении формы"""
        return reverse('client:detail', kwargs={'pk': self.get_object().pk})

    def test_func(self) -> bool:
        """Удалять клиента может только пользователь, добавивший его на сайт"""
        return self.get_object().created_by == self.request.user


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    """Контроллер для страницы удаления клиента"""
    model = Client
    success_url = reverse_lazy('client:list')

    def test_func(self) -> bool:
        """Удалять клиента может только пользователь, добавивший его на сайт"""
        return self.get_object().created_by == self.request.user
