from django.urls import path

from spam_messages.apps import SpamMessagesConfig
from spam_messages.views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView

app_name = SpamMessagesConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='detail'),
    path('create_message/', MessageCreateView.as_view(), name='create'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='update'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete'),
]
