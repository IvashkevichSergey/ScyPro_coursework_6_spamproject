from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from config import settings
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, verify_email

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_email/<int:pk>', verify_email, name='verify_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
