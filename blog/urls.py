from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView
from config import settings

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(template_name='blog/index.html'), name='index'),
    path('article/<int:pk>/', BlogDetailView.as_view(), name='article_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
