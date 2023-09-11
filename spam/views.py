from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from spam.forms import SpamForm
from spam.models import Spam, Message, Client, Logs


class SpamListView(LoginRequiredMixin, ListView):
    model = Spam

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.order_by('-pk')
        return queryset


class SpamDetailView(UserPassesTestMixin, DetailView):
    model = Spam

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_staff


def toggle_spam_status(request, pk):
    spam = get_object_or_404(Spam, pk=pk)
    if spam.status == 'created':
        spam.status = 'started'
    elif spam.status == 'started':
        spam.status = 'completed'
    spam.save()
    return redirect(reverse('spam:spam_detail', args=[spam.pk]))


class SpamCreateView(LoginRequiredMixin, CreateView):
    model = Spam
    form_class = SpamForm
    success_url = reverse_lazy('spam:spam_list')

    def get_form_kwargs(self):
        kwargs = super(SpamCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            spam = form.save()
            spam.owner = self.request.user
            spam.save()
        return super(SpamCreateView, self).form_valid(form)


class SpamUpdateView(UserPassesTestMixin, UpdateView):
    model = Spam
    form_class = SpamForm
    success_url = reverse_lazy('spam:spam_list')

    def get_form_kwargs(self):
        kwargs = super(SpamUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().owner == self.request.user


class SpamDeleteView(UserPassesTestMixin, DeleteView):
    model = Spam
    success_url = reverse_lazy('spam:spam_list')

    def test_func(self):
        return self.get_object().owner == self.request.user


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.order_by('-pk')
        return queryset


class MessageDetailView(UserPassesTestMixin, DetailView):
    model = Message

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_staff


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('spam:messages')

    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.owner = self.request.user
            message.save()
        return super().form_valid(form)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('spam:messages')

    def test_func(self):
        return self.get_object().owner == self.request.user


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('spam:messages')

    def test_func(self):
        return self.get_object().owner == self.request.user


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(UserPassesTestMixin, DetailView):
    model = Client

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_staff


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('spam:clients')

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            client.owner = self.request.user
            client.save()
        return super().form_valid(form)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('spam:clients')

    def test_func(self):
        return self.get_object().owner == self.request.user


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('spam:clients')

    def test_func(self):
        return self.get_object().owner == self.request.user


class LogsListView(PermissionRequiredMixin, ListView):
    model = Logs
    permission_required = 'spam.view_logs'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(spam=self.kwargs.get('pk'))
        queryset = queryset.order_by('-last_send')
        return queryset
