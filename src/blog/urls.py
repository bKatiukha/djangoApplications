from django.urls import path
from django.conf.urls.static import static
from app_config import settings

from .views import *

urlpatterns = [
    path('', BlogHomePage.as_view(), name='blog'),
    path('post/<slug:post_slug>/', BlogPostPage.as_view(), name='post'),
    path('form_view_add_post', AddFormViewPostFormPage.as_view(), name='form_view_add_post'),
    path('add_post', AddPostFormPage.as_view(), name='add_post'),
    path('category/<slug:category_slug>/', BlogCategoryPage.as_view(), name='category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
