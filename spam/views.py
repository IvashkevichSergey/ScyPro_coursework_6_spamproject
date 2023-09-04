from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from spam.models import Spam, Message, Client



class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('spam:messages')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body')
    success_url = reverse_lazy('spam:messages')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('spam:messages')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('spam:clients')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('full_name', 'email')
    success_url = reverse_lazy('spam:clients')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('spam:clients')


class SpamListView(ListView):
    model = Spam


class SpamDetailView(DetailView):
    model = Spam


class SpamCreateView(CreateView):
    model = Spam
    fields = ('title', 'spam_time', 'periodicity', 'status', 'clients', 'message')
    success_url = reverse_lazy('spam:index')


class SpamUpdateView(UpdateView):
    model = Spam
    fields = ('title', 'spam_time', 'periodicity', 'status', 'clients', 'message')
    success_url = reverse_lazy('spam:index')


class SpamDeleteView(DeleteView):
    model = Spam
    success_url = reverse_lazy('spam:index')
