from django.urls import path
from spam.apps import SpamConfig
from spam.views import SpamListView, SpamDetailView, SpamUpdateView, \
    SpamDeleteView, SpamCreateView, toggle_spam_status, LogsListView
from users.views import UserListView, toggle_user_status

app_name = SpamConfig.name

urlpatterns = [
    path('', SpamListView.as_view(), name='list'),
    path('spam/<int:pk>/', SpamDetailView.as_view(), name='detail'),
    path('create_spam/', SpamCreateView.as_view(), name='create'),
    path('spam_toggle_status/<int:pk>/', toggle_spam_status,
         name='toggle_status'),
    path('update_spam/<int:pk>/', SpamUpdateView.as_view(), name='update'),
    path('delete_spam/<int:pk>/', SpamDeleteView.as_view(), name='delete'),

    path('users_list/', UserListView.as_view(), name='users_list'),
    path('user_toggle_status/<int:pk>/', toggle_user_status,
         name='user_toggle_status'),

    path('logs_list/<int:pk>', LogsListView.as_view(), name='logs_list')
]
