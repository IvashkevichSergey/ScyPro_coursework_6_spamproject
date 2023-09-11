from django.urls import path
from spam.apps import SpamConfig
from spam.views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, SpamListView, ClientCreateView, ClientListView, ClientDetailView, \
    ClientUpdateView, ClientDeleteView, SpamDetailView, SpamUpdateView, SpamDeleteView, SpamCreateView, \
    toggle_spam_status, LogsListView
from users.views import UserListView, toggle_user_status

app_name = SpamConfig.name

urlpatterns = [
    path('', SpamListView.as_view(), name='index'),
    path('spam_list', SpamListView.as_view(), name='spam_list'),
    path('create_spam/', SpamCreateView.as_view(), name='create_spam'),
    path('spam/<int:pk>/', SpamDetailView.as_view(), name='spam_detail'),
    path('spam_toggle_status/<int:pk>/', toggle_spam_status, name='toggle_status'),
    path('change_spam/<int:pk>/', SpamUpdateView.as_view(), name='change_spam'),
    path('delete_spam/<int:pk>/', SpamDeleteView.as_view(), name='delete_spam'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('change_message/<int:pk>/', MessageUpdateView.as_view(), name='change_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('new_client/', ClientCreateView.as_view(), name='create_client'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('change_client/<int:pk>/', ClientUpdateView.as_view(), name='change_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('users_list/', UserListView.as_view(), name='users_list'),
    path('user_toggle_status/<int:pk>/', toggle_user_status, name='user_toggle_status'),

    path('logs_list/<int:pk>', LogsListView.as_view(), name='logs_list')
]
