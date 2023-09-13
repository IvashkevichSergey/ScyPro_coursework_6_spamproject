from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam.forms import SpamForm
from spam.models import Spam, Message, Client, Logs
from users.models import User


class SpamListView(LoginRequiredMixin, ListView):
    """Контроллер для страницы со списком рассылок"""
    model = Spam

    def get_queryset(self) -> QuerySet[Spam]:
        """Передаём в шаблон либо все рассылки, если пользователь имеет права Менеджера, либо
        только рассылки, созданные текущим пользователем"""
        queryset = super().get_queryset()
        if not self.request.user.has_perm('spam.view_spam'):
            queryset = queryset.filter(owner=self.request.user)
        # Применяем сортировку по id рассылки от новых к старым
        queryset = queryset.order_by('-pk')
        return queryset


class SpamDetailView(UserPassesTestMixin, DetailView):
    """Контроллер для страницы отображения детальной информации по рассылке"""
    model = Spam

    def test_func(self) -> bool:
        """Доступ к рассылке имеет либо её автор, либо модератор с соответствующими правами"""
        return self.get_object().owner == self.request.user or self.request.user.has_perm('spam.view_spam')


def toggle_spam_status(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Контроллер для изменения статуса рассылки"""
    spam = get_object_or_404(Spam, pk=pk)
    # Если рассылка только создана - переводим её в состояние запущена
    if spam.status == 'created':
        spam.status = 'started'
    # Если рассылка запущена - переводим её в состояние завершена
    elif spam.status == 'started':
        spam.status = 'completed'
    spam.save()
    return redirect(reverse('spam:spam_detail', args=[spam.pk]))


class SpamCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для страницы создания новой рассылки"""
    model = Spam
    form_class = SpamForm
    success_url = reverse_lazy('spam:spam_list')

    def get_form_kwargs(self) -> dict[str, User]:
        """Добавляем к аргументам, передаваемым в форму объект текущего пользователя
        для кастомной настройки отображения полей формы"""
        kwargs = super(SpamCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: SpamForm) -> HttpResponseRedirect:
        """Если форма валидна - заполняем у модели рассылки владельца текущим пользователем"""
        self.object = form.save()
        if form.is_valid():
            spam = form.save()
            spam.owner = self.request.user
            spam.save()
        return super(SpamCreateView, self).form_valid(form)


class SpamUpdateView(UserPassesTestMixin, UpdateView):
    """Контроллер для страницы изменения рассылки"""
    model = Spam
    form_class = SpamForm
    success_url = reverse_lazy('spam:spam_list')

    def get_form_kwargs(self) -> dict[str, User]:
        """Добавляем к аргументам, передаваемым в форму объект текущего пользователя
        для кастомной настройки отображения полей формы"""
        kwargs = super(SpamUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self) -> bool:
        """Изменять рассылку может только её автор"""
        return self.get_object().owner == self.request.user


class SpamDeleteView(UserPassesTestMixin, DeleteView):
    """Контроллер для страницы удаления рассылки"""
    model = Spam
    success_url = reverse_lazy('spam:spam_list')

    def test_func(self) -> bool:
        """Удалять рассылку может только её автор"""
        return self.get_object().owner == self.request.user


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для страницы просмотра списка сообщений"""
    model = Message

    def get_queryset(self) -> QuerySet[Message]:
        """Передаём в шаблон либо все сообщения, если пользователь имеет права Менеджера, либо
        только сообщения, созданные текущим пользователем"""
        queryset = super().get_queryset()
        if not self.request.user.has_perm('spam.view_message'):
            queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.order_by('-pk')
        return queryset


class MessageDetailView(UserPassesTestMixin, DetailView):
    """Контроллер для страницы отображения детальной информации по сообщению"""
    model = Message

    def test_func(self) -> bool:
        """Доступ к детальной информации по сообщениям имеет либо автор сообщения,
        либо модератор с соответствующими правами"""
        return self.get_object().owner == self.request.user or self.request.user.has_perm('spam.view_message')


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для страницы создания нового сообщения"""
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('spam:messages')

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        """Если форма валидна - заполняем поле автора сообщения текущим пользователем"""
        if form.is_valid():
            message = form.save()
            message.owner = self.request.user
            message.save()
        return super().form_valid(form)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    """Контроллер для страницы изменения сообщения"""
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('spam:messages')

    def test_func(self) -> bool:
        """Изменять сообщение может только его автор"""
        return self.get_object().owner == self.request.user


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    """Контроллер для страницы удаления сообщения"""
    model = Message
    success_url = reverse_lazy('spam:messages')

    def test_func(self) -> bool:
        """Удалять сообщение может только его автор"""
        return self.get_object().owner == self.request.user


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка клинетов"""
    model = Client

    def get_queryset(self) -> QuerySet[Client]:
        """Передаём в шаблон либо всех клиентов, если пользователь имеет права Менеджера, либо
        только клиентов, созданных текущим пользователем"""
        queryset = super().get_queryset()
        if not self.request.user.has_perm('spam.view_client'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(UserPassesTestMixin, DetailView):
    """Контроллер для отображения детальной информации по клиентам"""
    model = Client

    def test_func(self) -> bool:
        """Доступ к детальной информации по клиенту имеет либо пользователь, добавивший
        на сайт клиента, либо модератор с соответствующими правами"""
        return self.get_object().owner == self.request.user or self.request.user.has_perm('spam.view_client')


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для страницы создания нового клиента"""
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('spam:clients')

    def form_valid(self, form) -> HttpResponseRedirect:
        """Если форма валидна - заполняем поле автора клиента текущим пользователем"""
        if form.is_valid():
            client = form.save()
            client.owner = self.request.user
            client.save()
        return super().form_valid(form)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    """Контроллер для страницы изменения информации о клиенте"""
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('spam:clients')

    def test_func(self) -> bool:
        """Удалять клиента может только пользователь, добавивший его на сайт"""
        return self.get_object().owner == self.request.user


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    """Контроллер для страницы удаления клиента"""
    model = Client
    success_url = reverse_lazy('spam:clients')

    def test_func(self) -> bool:
        """Удалять клиента может только пользователь, добавивший его на сайт"""
        return self.get_object().owner == self.request.user


class LogsListView(PermissionRequiredMixin, ListView):
    """Контроллер для просмотра списка логов по конкретной рассылке"""
    model = Logs
    permission_required = 'spam.view_logs'

    def get_queryset(self) -> QuerySet[Logs]:
        """Получаем логи по конкретной рассылке, добавляем сортировку по дате создания лога"""
        queryset = super().get_queryset()
        queryset = queryset.filter(spam=self.kwargs.get('pk'))
        queryset = queryset.order_by('-last_send')
        return queryset
