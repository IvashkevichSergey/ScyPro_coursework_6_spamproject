import random

from django.views.generic import ListView, DetailView

from blog.models import Blog
from spam.models import Spam, Client


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['spam'] = Spam.objects.all()
        context_data['spam_active'] = Spam.objects.filter(status='started')
        context_data['clients'] = Client.objects.all()
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = random.sample(list(queryset), 3)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.obj = super().get_object(queryset)
        self.obj.views += 1
        self.obj.save()
        return super(BlogDetailView, self).get_object()
