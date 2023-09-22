from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from spam_messages.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для страницы просмотра списка сообщений"""
    model = Message

    def get_queryset(self) -> QuerySet[Message]:
        """Передаём в шаблон либо все сообщения, если пользователь
        имеет права Менеджера, либо только сообщения, созданные
        текущим пользователем"""
        queryset = super().get_queryset()
        if not self.request.user.has_perm('spam_messages.view_message'):
            queryset = queryset.filter(created_by=self.request.user)
        queryset = queryset.order_by('-pk')
        return queryset


class MessageDetailView(UserPassesTestMixin, DetailView):
    """Контроллер для страницы отображения детальной информации по сообщению"""
    model = Message

    def test_func(self) -> bool:
        """Доступ к детальной информации по сообщениям
        имеет либо автор сообщения, либо модератор
        с соответствующими правами"""
        return \
            self.get_object().created_by == self.request.user \
            or self.request.user.has_perm('spam_messages.view_message')


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для страницы создания нового сообщения"""
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('message:list')

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        """Если форма валидна - заполняем поле автора
        сообщения текущим пользователем"""
        if form.is_valid():
            message = form.save()
            message.created_by = self.request.user
            message.save()
        return super().form_valid(form)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    """Контроллер для страницы изменения сообщения"""
    model = Message
    fields = ('subject', 'body')

    def get_success_url(self):
        return reverse('message:detail', kwargs={'pk': self.get_object().pk})

    def test_func(self) -> bool:
        """Изменять сообщение может только его автор"""
        return self.get_object().created_by == self.request.user


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    """Контроллер для страницы удаления сообщения"""
    model = Message
    success_url = reverse_lazy('message:list')

    def test_func(self) -> bool:
        """Удалять сообщение может только его автор"""
        return self.get_object().created_by == self.request.user
