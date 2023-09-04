from django.conf.urls.static import static
from django.urls import path

from config import settings
from spam.apps import SpamConfig

app_name = SpamConfig.name

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
