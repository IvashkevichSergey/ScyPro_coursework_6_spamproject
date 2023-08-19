from django.urls import path
from spam.apps import SpamConfig
from spam.views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, SpamListView, SpamCreateView, ClientCreateView, ClientListView, ClientDetailView, \
    ClientUpdateView, ClientDeleteView, SpamDetailView, SpamUpdateView, SpamDeleteView

app_name = SpamConfig.name

urlpatterns = [
    path('', SpamListView.as_view(), name='index'),
    path('create_spam/', SpamCreateView.as_view(), name='create_spam'),
    path('spam/<int:pk>/', SpamDetailView.as_view(), name='spam_detail'),
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

]
