from django.urls import path

from spam_clients.apps import ClientsConfig
from spam_clients.views import ClientListView, ClientCreateView, \
    ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('', (ClientListView.as_view()), name='list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='detail'),
    path('create_client/', ClientCreateView.as_view(), name='create'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
]
